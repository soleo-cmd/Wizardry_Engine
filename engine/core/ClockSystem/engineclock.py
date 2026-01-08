import time

class EngineClock:
    """
    A simple engine-wide clock.
    Can be used for benchmarking, FPS counting, or general timing.
    """

    def __init__(self):
        self.start_time = None
        self.last_frame_time = None
        self.delta = 0.0
        self.elapsed = 0.0
        self.frame_count = 0

    def start(self):
        """Start the clock."""
        self.start_time = time.perf_counter()
        self.last_frame_time = self.start_time
        self.elapsed = 0.0
        self.frame_count = 0

    def tick(self):
        """
        Call once per frame or per tick.
        Updates delta time and frame count.
        """
        now = time.perf_counter()
        self.delta = now - self.last_frame_time
        self.last_frame_time = now
        self.elapsed = now - self.start_time
        self.frame_count += 1

    def get_delta(self) -> float:
        """Return time since last tick in seconds."""
        return self.delta

    def get_elapsed(self) -> float:
        """Return total elapsed time since start in seconds."""
        return self.elapsed

    def get_fps(self) -> float:
        """Return current average FPS since start."""
        if self.elapsed == 0:
            return 0.0
        return self.frame_count / self.elapsed
