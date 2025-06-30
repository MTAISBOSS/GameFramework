import time
class Time:
    def __init__(self):
        self.frame_rate = 60
        self.delta_time = 0.0
        self.fixed_delta_time = 1 / self.frame_rate

        self.time = 0.0
        self.unscaled_time = 0.0
        self.frame_count = 0

        self.time_scale = 1.0
        self.max_delta_time = 0.1

        self.fps = 0
        self._last_time = time.time()
        self._fps_accumulator = 0
        self._fps_frames = 0
    
    def update(self):
        current_time = time.time()
        raw_delta = current_time - self._last_time

        self.delta_time = min(raw_delta,self.max_delta_time) * self.time_scale

        self._last_time = current_time
        self.time += self.delta_time
        self.unscaled_time += raw_delta
        self.frame_count += 1

        self._fps_accumulator += raw_delta
        self._fps_frames +=1
        if self._fps_accumulator >= 1.0:
            self.fps = self._fps_frames / self._fps_accumulator
            self._fps_accumulator = 0
            self._fps_frames = 0
    
    def sleep_for_framerate(self,target_frame_rate):
        new_time = 1 / target_frame_rate
        current_time = time.time()
        elapsed_time = current_time - self._last_time

        if  elapsed_time < new_time:
            time.sleep(new_time - elapsed_time)
    
    def get_fps(self):
        return self.fps

    def reset_timer_settings(self):
        self.__init__()