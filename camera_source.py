# Note: This code is based *heavily* upon (there's more original than modified)
#   the code taken from the "Flask Video Streaming Revisited" blog post
#   by Miguel Grinberg.  The bulk of the modification is to change the Camera
#   classes to be used as instances rather than as classes.  This allows first
#   of all for multiple cameras of the same type. It also allows for the
#   emulated camera to be constructed with an arbitrary list of images.

import time
import threading
try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident


class CameraEvent(object):
    """An Event-like class that signals all active clients when a new frame is
    available.
    """
    def __init__(self):
        self.events = {}

    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 5 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()][0].clear()


class BaseCamera(object):
    def __init__(self):
        """Start the background camera thread if it isn't running yet."""
        self.__event = CameraEvent()
        self.__frame = None
        self.__last_access = time.time()
        self.__thread = threading.Thread(target=self.__thread)

    def start(self):
        self.__thread.start()

    def get_frame(self):
        """Return the current camera frame."""
        self.__last_access = time.time()

        # wait for a signal from the camera thread
        self.__event.wait()
        self.__event.clear()

        return self.__frame

    def frames(self):
        """Generator that returns frames from the camera."""
        raise RuntimeError('Must be implmented by subclass.')

    def __thread(self):
        """Camera background thread."""
        frames_iterator = self.frames()
        for frame in frames_iterator:
            self.__frame = frame
            self.__event.set()
            time.sleep(0) # Allow for async with gevent and eventlet

            # if there have been any clients asking for frames in
            #   the last 10 seconds then stop the thread
            if (time.time()-self.__last_access) > 10:
                frames_iterator.close()
                break
        self.__thread = None

# Much of the modification of this code arrives in the treatment of the Emulated
#   camera.  This is able to receive aa list of
class EmulatedCamera(BaseCamera):
    """An emulated camera implementation that streams a repeated sequence of
    files at a configurable rate"""

    def __init__(self, files, dt=1.0):
        BaseCamera.__init__(self)
        self.__files = files
        self.__images = [open(file, 'rb').read() for file in self.__files]
        self.__dt = dt
        self.start()

    def frames(self):
        dt = self.__dt
        images = self.__images
        N = len(images)
        while True:
            time.sleep(dt)
            yield images[int(time.time()) % N]
