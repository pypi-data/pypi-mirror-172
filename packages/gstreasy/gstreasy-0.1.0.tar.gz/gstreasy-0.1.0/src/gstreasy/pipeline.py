"""This module provides the GstPipeline class."""

import logging
import queue
import sys
import threading
import time
import typing
from fractions import Fraction

import gi
import numpy as np

from .utils import GstBuffer, LeakyQueue, WrappedCaps, gst_buffer_to_ndarray, make_caps

gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")
gi.require_version("GstVideo", "1.0")
from gi.repository import GLib, GObject, Gst, GstApp  # noqa: E402

Gst.init(sys.argv)

Framerate = typing.Union[int, Fraction, str]


class AppSink:
    """Wraps `GstApp.AppSink` to simplify extracting samples/buffers.

    Attributes:
        sink (GstApp.AppSink): the appsink element.
        queue (queue.Queue, LeakyQueue): The queue buffers are held in.
    """

    def __init__(self, sink: GstApp.AppSink, leaky: bool, qsize: int):
        """Initialize the AppSink class.

        Args:
            sink (GstApp.AppSink): the appsink element.
            leaky (bool): Whether the appsink should put buffers in a
                leaky Queue (oldest buffers dropped if full) or a
                normal Queue (block on `Queue.put` if full).
            qsize (int): Max number of buffers to keep in the Queue.
        """
        self.sink = sink
        self.sink.connect("new-sample", self._on_buffer, None)
        self.queue: typing.Union[queue.Queue, LeakyQueue]
        self.queue = LeakyQueue(qsize) if leaky else queue.Queue(qsize)
        self._caps: typing.Optional[WrappedCaps] = None
        self._log = logging.getLogger("AppSink")
        self._log.addHandler(logging.NullHandler())

    @property
    def caps(self) -> typing.Optional[WrappedCaps]:
        """`WrappedCaps` being used to map `Gst.Buffer`'s to `np.ndarray.`'s."""
        if self._caps:
            return self._caps

        caps = self.sink.get_caps()
        if not caps:
            self._log.warning("AppSink has no caps. Will check again on first sample")
            return self._caps

        self._caps = WrappedCaps.wrap(caps)
        return self._caps

    def _on_buffer(self, sink: GstApp.AppSink, data: typing.Any) -> Gst.FlowReturn:
        """Callback for 'new-sample' signal."""
        sample = sink.emit("pull-sample")
        if not sample:
            self._log.error("Bad sample: type = %s" % type(sample))
            return Gst.FlowReturn.ERROR

        self._log.debug("Got Sample")
        self.queue.put(self._extract_buffer(sample))
        return Gst.FlowReturn.OK

    def _extract_buffer(self, sample: Gst.Sample) -> typing.Optional[GstBuffer]:
        buffer = sample.get_buffer()
        if not self._caps:
            self._log.debug("Getting caps from first sample")
            try:
                self._caps = WrappedCaps.wrap(sample.get_caps())
            except AttributeError:
                return None

        # Use the cached Caps so don't have to re-calc every sample
        if self._caps:
            array = gst_buffer_to_ndarray(buffer, self._caps)
            return GstBuffer(
                data=array,
                pts=buffer.pts,
                dts=buffer.dts,
                duration=buffer.duration,
                offset=buffer.offset,
            )
        return None

    @property
    def queue_size(self) -> int:
        """Return number of buffers in the `queue`."""
        return self.queue.qsize()


class AppSrc:
    """Wraps `GstApp.AppSrc` to simplify inserting samples/buffers.

    Attributes:
        src (GstApp.AppSrc): the appsrc element.
    """

    def __init__(self, src: GstApp.AppSrc):
        """Initialize the AppSrc class.

        Args:
            src (GstApp.AppSrc): the appsrc element.
        """
        self.src = src
        self._caps: typing.Optional[Gst.Caps] = src.get_caps()

        self.pts: typing.Union[int, float] = 0
        self.dts: int = GLib.MAXUINT64

        self.log = logging.getLogger("AppSrc")
        self.log.addHandler(logging.NullHandler())

        self._duration: typing.Union[int, float] = 0

    @property
    def duration(self) -> typing.Union[int, float]:
        """This is not well understood."""
        if not self._duration:
            self._duration = self._calc_duration()
        return self._duration

    def _calc_duration(self) -> typing.Union[int, float]:
        """Return duration estimate based on the framerate of the src Caps."""
        duration: typing.Union[int, float] = 0
        if not self.caps:
            return duration
        caps_string = self.caps.to_string()
        fps = caps_string.split("(fraction)")[1].split(",")[0]
        if fps:
            framerate = Fraction(fps)
            duration = 10**9 / (framerate.numerator / framerate.denominator)
        return duration

    @property
    def caps(self) -> typing.Optional[Gst.Caps]:
        """Return the `Gst.Caps` being set on pushed samples."""
        return self._caps

    @caps.setter
    def caps(self, new_caps: Gst.Caps):
        self._caps = new_caps

    def push(self, data: np.ndarray):
        """Create a `Gst.Sample` from `np.ndarray` and push it into the pipeline."""
        self.pts += self.duration
        offset = self.pts / self.duration
        gst_buffer = Gst.Buffer.new_wrapped(bytes(data))
        gst_buffer.pts = self.pts
        gst_buffer.dts = self.dts
        gst_buffer.offset = offset
        gst_buffer.duration = self.duration
        sample = Gst.Sample.new(buffer=gst_buffer, caps=self.caps)
        self.log.debug("Push Sample")
        self.src.emit("push-sample", sample)


class GstPipeline:
    """A Simple and efficient interface for running GStreamer Pipelines.

    Designed to be used as a ContextManager, GstPipeline takes care of the setup
    and teardown of the GLib.MainLoop thread to handle messages from the event bus.
    Any appsink or appsrc elements present in the provided command are automatically
    configured. You can `pull` buffers from an `appsink` and `push` buffers to
    an `appsrc`.

    The attributes `pipeline`, `bus`, and `elements` are uninitialized until
    `startup` is called manually are upon entering the context manager.
    """

    def __init__(
        self,
        command: str,
    ):
        """Create a GstPipeline instance but don't start it yet."""
        self.command: str = command
        """A pipeline definition that can be run by gst-launch-1.0"""

        self.pipeline: typing.Optional[Gst.Pipeline] = None
        """The actual Pipeline created by calling
            [`Gst.parse_launch`](https://lazka.github.io/pgi-docs/index.html#Gst-1.0/functions.html#Gst.parse_launch)
            on the provided `command`. Defaults to `None`."""

        self.bus: typing.Optional[Gst.Bus] = None
        """The message bus attached to `pipeline`. Defaults to `None`."""

        self.elements: typing.List[Gst.Element] = []
        """A list of all `Gst.Element`'s in the `pipeline`."""

        self._main_loop = GLib.MainLoop.new(None, is_running=False)
        self._main_loop_thread = threading.Thread(
            target=self._main_loop_run, name="MainLoop"
        )
        self._end_stream_event = threading.Event()

        self._appsink: typing.Optional[AppSink] = None
        self._appsink_setup: bool = False

        self._appsrc: typing.Optional[AppSrc] = None
        self._appsrc_setup: bool = False

        self._log = logging.getLogger("GstPipeline")
        self._log.addHandler(logging.NullHandler())

    def __bool__(self) -> bool:
        """Return whether or not pipeline is active or there are buffers to process."""
        if self.appsink:
            return not self.is_done or self.appsink.queue_size > 0
        return not self.is_done

    def __str__(self) -> str:
        """Return string representing the pipelines current state."""
        return f"GstPipeline({self.state})"

    def __repr__(self) -> str:
        """Return string representing GstPipeline object."""
        return f"<{self}>"

    def __enter__(self) -> "GstPipeline":
        """Perform all required setup before running pipeline."""
        self.startup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup all pipeline resources."""
        self.shutdown()

    def _main_loop_run(self):
        try:
            self._main_loop.run()
        except Exception as ex:
            self._log.warning("%s" % ex)
            pass

    def _init_elements(self):
        if self.pipeline:
            elements = self.pipeline.iterate_elements()
            out = []
            while True:
                ret, elem = elements.next()
                if ret == Gst.IteratorResult.DONE:
                    break
                if ret != Gst.IteratorResult.OK:
                    break
                out.append(elem)
        return out

    def get_by_cls(self, cls: GObject.GType) -> typing.List[Gst.Element]:
        """Return a `list[Gst.Element]` of all matching pipeline elements.

        Args:
            cls (GObject.GType): The Element class to match against.
        """
        if not self.elements:
            # FIXME
            return []
        return [e for e in self.elements if isinstance(e, cls)]

    def get_by_name(self, name: str) -> typing.Optional[Gst.Element]:
        """Return Gst.Element from pipeline by name lookup.

        Args:
            name (str): `name` property of the element.
        """
        if self.pipeline:
            return self.pipeline.get_by_name(name)
        return None

    @property
    def state(self) -> Gst.State:
        """Return current state of the pipeline."""
        if self.pipeline:
            return self.pipeline.get_state(timeout=1)[1]
        return Gst.State.NULL

    def _shutdown_pipeline(self, eos: bool = False, timeout: int = 1):
        if not self.pipeline:
            if self._end_stream_event.is_set():
                return
            self._log.warning("Pipeline is not running")
            return

        self._end_stream_event.set()

        if eos and self.state == Gst.State.PLAYING:
            thread = threading.Thread(
                target=self.pipeline.send_event, args=(Gst.Event.new_eos(),)
            )
            thread.start()
            thread.join(timeout=timeout)

        time.sleep(timeout)

        try:
            self.pipeline.set_state(Gst.State.NULL)
            self.pipeline = None
        except AttributeError:
            pass

    def _shutdown_main_loop(self, eos: bool = False, timeout: int = 1):
        if self._main_loop.is_running():
            self._main_loop.quit()

    def shutdown(self, eos: bool = False, timeout: int = 1):
        """Shutdown the mainloop thread and pipeline.

        Args:
            eos (bool, optional): Whether to send an EOS event to the running
                pipeline. Defaults to False.
            timeout: (int, optional): Timeout in seconds to wait for running
                threads to finish/return. Defaults to 1.
        """
        self._log.info("Shutdown requested ...")
        self._shutdown_pipeline(eos, timeout)
        self._shutdown_main_loop()
        self._log.info("Shutdown Success")

    def startup(self):
        """Start the mainloop thread and pipeline."""
        self._log.info("Starting pipeline")
        if self._main_loop_thread.is_alive():
            self._log.warning("Pipeline already running")
            return

        self._main_loop_thread.start()

        if self.pipeline:
            self._log.warning("Pipeline already running")
            return
        self.pipeline = Gst.parse_launch(self.command)
        self.elements = self._init_elements()

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message::error", self.on_error)
        self.bus.connect("message::eos", self.on_eos)
        self.bus.connect("message::warning", self.on_warning)
        self.bus.connect("message::element", self.on_element)
        self.bus.connect("message::STATE_CHANGED", self.on_state_change)

        self.pipeline.set_state(Gst.State.READY)
        self._log.debug("Set pipeline to READY")
        self._end_stream_event.clear()

        # Allow pipeline to PREROLL by setting in PAUSED state so caps
        # negotiation happens before configuring appsink/appsrc
        self.pipeline.set_state(Gst.State.PAUSED)
        self._log.debug("Set pipeline to PAUSED")

        if not self._appsrc_setup:
            self._appsrc_setup = self.setup_appsrc()

        if not self._appsink_setup:
            self._appsink_setup = self.setup_appsink()

        self.pipeline.set_state(Gst.State.PLAYING)
        self._log.debug("Set pipeline to PLAYING")

    @property
    def is_active(self) -> bool:
        """Return whether or not pipeline is active."""
        return self.pipeline is not None and not self.is_done

    @property
    def is_done(self) -> bool:
        """Return whether or not EOS event has triggered."""
        return self._end_stream_event.is_set()

    @property
    def appsink(self) -> typing.Optional[AppSink]:
        """Return appsink if configured or None."""
        return self._appsink

    @property
    def appsrc(self) -> typing.Optional[AppSrc]:
        """Return appsrc if configured or None."""
        return self._appsrc

    def setup_appsink(self, leaky: bool = False, qsize: int = 100) -> bool:
        """Initialize _AppSink helper class if there's an appsink element in pipeline.

        Args:
            leaky (bool, optional): Whether the appsink should put buffers in
                a leaky Queue (oldest buffers dropped if full) or a normal Queue
                (block on `Queue.put` if full). Defaults to False.
            qsize: (int, optional): The maxsize of the appsink queue. Defaults to 100
        Returns:
            bool: Whether the appsink was setup.
        """
        # bail early if already setup
        if self._appsink_setup:
            self._log.warning("Appsink already setup")
            return True
        try:
            appsink_element = self.get_by_cls(GstApp.AppSink)[0]
            self._log.debug("appsink element detected")
        except IndexError:
            self._log.debug("No appsink element to setup")
            return False
        self._log.debug("Setting up AppSink ...")
        self._appsink = AppSink(appsink_element, leaky, qsize)
        self._log.debug("Successfully setup AppSink")
        return True

    def pop(self, timeout: float = 0.1) -> typing.Optional[GstBuffer]:
        """Return a `GstBuffer` from the `appsink` queue."""
        if not self._appsink:
            self._log.warning("No appsink to pop from")
            raise RuntimeError

        buf: typing.Optional[GstBuffer] = None
        while (self.is_active or not self._appsink.queue.empty()) and not buf:
            try:
                buf = self._appsink.queue.get(timeout=timeout)
            except queue.Empty:
                pass
        return buf

    def set_appsrc_caps(
        self,
        *,
        width: int,
        height: int,
        framerate: Framerate,
        format: str,
    ) -> bool:
        """Set appsrc caps if not already set.

        Args:
            width (int): a positive integer corresponding to buffer width
            height (int): a positive integer corresponding to buffer height
            framerate (int, Fraction, str): A positive integer, `fractions.Fraction`,
                or string that can be mapped to a Fraction.
                Ex. 1 -> 10/1, "25/1" -> Fraction(25, 1)
            format (str): A string that can be mapped to a `GstVideo.VideoFormat`.
                Ex. "RGB", "GRAY8", "I420"
        Raises:
            ValueError: If Gst.Caps cannot be created from arguments
        """
        if not self._appsrc:
            self._log.warning("No appsrc element")
            return False
        if self._appsrc.caps:
            self._log.warning("Caps already set")
            return False

        self._log.debug("Building caps from args ...")
        self._appsrc.caps = make_caps(width, height, framerate, format)
        self._log.debug("Caps successfully set")
        return True

    def setup_appsrc(self) -> bool:
        """Initialize _AppSrc helper class if there's an appsrc element in pipeline.

        Returns:
            bool: Whether setup was successful
        """
        if self._appsrc_setup:
            self._log.warning("Appsource already setup")
            return True
        try:
            appsrc_element = self.get_by_cls(GstApp.AppSrc)[0]
        except IndexError:
            self._log.debug("No appsrc element to setup")
            return False

        appsrc_element.set_property("format", Gst.Format.TIME)
        appsrc_element.set_property("block", True)
        self._appsrc = AppSrc(appsrc_element)
        return True

    def push(self, data: np.ndarray):
        """Map the ndarray to a Gst.Sample and push it into the pipeline."""
        if not self._appsrc:
            self._log.warning("No appsrc to push to")
            raise RuntimeError
        self._appsrc.push(data)

    def on_error(self, bus: Gst.Bus, msg: Gst.Message):
        """Log `ERROR` message and shutdown."""
        err, debug = msg.parse_error()
        self._log.error("Error %d %s: %s" % (err.code, err.message, debug))
        self.shutdown()

    def on_eos(self, bus: Gst.Bus, msg: Gst.Message):
        """Log `EOS` messages and shutdown pipeline."""
        self._log.debug("Received EOS message")
        self._shutdown_pipeline(eos=True)

    def on_warning(self, bus: Gst.Bus, msg: Gst.Message):
        """Log `WARNING` messages."""
        warn, debug = msg.parse_warning()
        self._log.warning("%s %s" % (warn, debug))

    def on_element(self, bus: Gst.Bus, msg: Gst.Message):
        """Log `ELEMENT` messages.

        Typically you would override this method.
        """
        msg_struct = msg.get_structure()
        name = msg_struct.get_name()
        self._log.debug("Element message %s" % name)

    def on_state_change(self, bus: Gst.Bus, msg: Gst.Message):
        """Log `STATE_CHANGED` messages.

        `STATE_CHANGED` events can be triggered by dynamic pipelines.
        (Ex. updating a sinks Caps)
        """
        old, new, pending = msg.parse_state_changed()
        self._log.debug("State changed from %s -> %s" % (old, new))
