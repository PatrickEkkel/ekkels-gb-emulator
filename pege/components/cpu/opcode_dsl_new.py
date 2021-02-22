from constants import *

class NewOpcodeContext:
    def __init__(self, cpu, mmu, meta):
        self._mmu = mmu
        self._cpu = cpu
        self._meta = meta
        #self.value_a = 0
        self.value_b = 0

    def init(self):
        pass
    def bitwise(self, register=None, operation=None, position=0, value=None,transient_load=False):
        return self
    
    def add(self, register=None):
        return self

    def sub(self, register=None):
        return self

    def dec(self, register=None):
        return self

    def branch(self, flag, invert=False):
        return self

    def flags(self, zero, substract, halfcarry, carry):
        return self
    
    def inc(self, register=None):
        return self

    def load(self, register=None, addressing_mode=0, transient_store=False, value=None):
        return self
    
    def reset(self, position):
        return self

    def set(self, address):
        return self

    def push(self):
        return self
    
    def pop(self):
        return self

    def merge(self):
        return self

    def store(self, register=None, addressing_mode=None,transient_store=False, value=None):
        return self
    