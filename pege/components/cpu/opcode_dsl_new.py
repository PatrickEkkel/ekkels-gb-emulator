from constants import *
from components.cpu.opcode_dsl import Opcode

class NewOpcodeContext:
    def __init__(self, cpu, mmu, meta):
        self._mmu = mmu
        self._cpu = cpu
        self._meta = meta
        self.value = 0x00
        if meta:
            self.opcode = Opcode(self._meta)


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

    def load_FFOO(self, r1, r2):
        reg_value_a = self._cpu.reg.reg_read_dict[r1]()
        reg_value_b = self._cpu.reg.reg_read_dict[r2]()
        address = 0xFF00 + reg_value_a
        self.address = address
        self.value   = reg_value_b
        return self

    def load_d16(self):
        self._cpu.pc += 1
        self.value = self._mmu.read_u16(self._cpu.pc)
        self._cpu.pc += 1
        return self

    def load(self):
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

    # store 8 bit data into address
    def store_a8(self):
        self._cpu._mmu.write(self.address, self.value)
        return self
    
    # store 16 data into register BC,DE,HL,SP,PC
    def store_d16(self, r1):
        self._cpu.reg.reg_write_dict[r1](self.value)

    def store(self):
        return self
    