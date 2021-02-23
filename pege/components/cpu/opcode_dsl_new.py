from constants import *
from components.cpu.opcode_dsl import Opcode

class NewOpcodeContext:
    def __init__(self, cpu, mmu, meta):
        self._mmu = mmu
        self._cpu = cpu
        self._meta = meta
        #self.value = 0x00
        self.values = [0x00,0x00]
        self.pointer = 0
        if meta:
            self.opcode = Opcode(self._meta)


    def init(self):
        pass

    def _set_value(self, value):
        self.values[self.pointer] = value
        self.pointer += 1

    def _get_value(self):
        self.pointer -= 1
        return self.values[self.pointer]
        
    def bitwise(self, register=None, operation=None, position=0, value=None,transient_load=False):
        return self
    
    def add(self, register=None):
        return self

    def sub(self, register=None):
        return self

    def dec(self):
        value = self._get_value()
        #value -= 0x1
        self._set_value(value - 0x01)
        return self

    def branch(self, flag, invert=False):
        return self

    def flags(self, zero, substract, halfcarry, carry):
        return self
    
    def inc(self, register=None):
        return self

    def shift_right(self, position):
        value = self._get_value()
        self._set_value(value >> position)
        return self
    
    def bitwise_and(self, value):
        value = self._get_value()
        value &= value
        self._set_value(value)
        return self

    def load_FFOO(self, r1, r2):
        reg_value_a = self._cpu.reg.reg_read_dict[r1]()
        reg_value_b = self._cpu.reg.reg_read_dict[r2]()
        address = 0xFF00 + reg_value_a
        self.address = address
        self._set_value(reg_value_b)
        return self

    # load 8 bit register into buffer
    def load_rd8(self, r1):
        self._set_value(self._cpu.reg.reg_read_dict[r1]())
        return self

    # load 16 bit direct data into buffer
    def load_d16(self):
        self._cpu.pc += 1
        self._set_value(self._mmu.read_u16(self._cpu.pc))
        self._cpu.pc += 1
        return self

    # load 16 bit register into buffer
    def load_rd16(self, r1):
        reg = self._cpu.reg.reg_read_dict[r1]()
        self._set_value(reg)
        return self

    def load(self):
        return self
    
    def reset(self, position):
        return self

    def set(self, address):
        return self

    # push current value as a 16bit value on the stack 
    def push_d16(self):
        value = self._get_value()
        self._cpu.stack.push_u16bit(value)
        return self
    
    def pop(self):
        return self

    def merge(self):
        return self

    # store 8 bit data into address
    def store_a8(self):
        value = self._get_value()
        self._cpu._mmu.write(self.address, value)
        return self
    
    # store 16 data into register BC,DE,HL,SP,PC
    def store_d16(self, r1):
        value = self._get_value()
        self._cpu.reg.reg_write_dict[r1](value)
        return self

    def store(self):
        return self
    