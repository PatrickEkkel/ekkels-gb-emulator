import time, datetime

class Clock:
    def __init__(self,speed):
        self._clock = 0
        self._current = 0
        self._speed = speed

    def tick(self):
        if self._clock == self._speed:
            self._clock = 0
        self._clock += 1

    def wait(self):
        return self._current > self._clock

    def start_of_cycle(self):
        return self._clock == 0

    def update(self, cycle):
        self._current = self._clock + cycle

class CPUClock(Clock):

    def __init__(self,speed):
        super(CPUClock, self).__init__(speed)

class GPUCLock(Clock):
    CLOCKS_PER_LINE = 114
    CLOCKS_PER_SCREEN = 17556
    def __init__(self,speed):
        super(GPUCLock, self).__init__(speed)
        self.line_counter = 0
        self.screen_counter = 0
        self.framecounter = 0
        self.lines_drawn = 0

    def wait(self):
        return self._current > self._clock

    def _count_line(self):
        if GPUCLock.CLOCKS_PER_LINE == self.line_counter:
            self.line_counter = 0
            self.lines_drawn += 1
        else:
            self.line_counter += 1

    def _framecounter(self):
        if self.framecounter == 60:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            #print(self.lines_drawn)
            #print(st)
            #print(self.framecounter)
            self.framecounter = 0
    def _count_screen(self):
        if GPUCLock.CLOCKS_PER_SCREEN == self.screen_counter:
            self.screen_counter = 0
            self.framecounter += 1
            #print(self.lines_drawn)
            self.lines_drawn = 0
        else:
            self.screen_counter += 1

    def tick(self):
        if self._clock == self._speed:
            self._clock = 0
        self._clock += 1
        self._count_line()
        self._count_screen()
        self._framecounter()
