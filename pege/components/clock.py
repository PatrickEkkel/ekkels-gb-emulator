import time, datetime

class Clock:
    def __init__(self,speed):
        self._clock = 0
        self._current = 0
        self._speed = speed
        self.debug = True

    def tick(self):
        if self._clock == self._speed:
            # we need to carry ticks over to the new cycle
            if self.wait():
                self._current = self._current - self._clock
            else:
                self._current = 0     
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