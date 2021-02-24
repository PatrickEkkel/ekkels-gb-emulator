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

    def _check_carry(self):
        pass
    
    def _check_substract(self):
        pass

    def _check_half_carry(self):
        pass

    def _check_zero(self):
        value = self._get_value()
        if value == 0x00:
            self._cpu.reg.SET_ZERO()
        else:
            self._cpu.reg.CLEAR_ZERO()
        
    def init(self):
        pass
    
    # set a value to the stack TODO: rename to push
    def _set_value(self, value):
        self.values[self.pointer] = value
        self.pointer += 1

    # get a value from the stack TODO: rename to pop
    def _get_value(self):
        self.pointer -= 1
        return self.values[self.pointer]
    
    # read a value from the stack without modifying the stackpointer
    def _read_value(self):
        pointer = self.pointer - 1
        return self.values[pointer]
        
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
        I = '-'
        E = 0
        S = 1
        Z = 2
        N = 3
        H = 4
        C = 5

        if zero == Z:
            self._check_zero()
        elif zero == S:
            self._cpu.reg.SET_ZERO()
        elif zero == E:
            self._cpu.reg.CLEAR_ZERO()

        if substract == N:
            self._check_substract()
        elif substract == S:
            self._cpu.reg.SET_SUBSTRACT()
        elif substract == E:
            self._cpu.reg.CLEAR_SUBSTRACT()

        if halfcarry == H:
            self._check_half_carry()
        elif halfcarry == S:
            self._cpu.reg.SET_HALF_CARRY()
        elif halfcarry == E:
            self._cpu.reg.CLEAR_HALF_CARRY()

        if carry == C:
            self._check_carry()
        elif carry == S:
            self._cpu.reg.SET_CARRY()
        elif carry == E:
            self._cpu.reg.CLEAR_CARRY()

        return self

    def inc(self, register=None):
        return self

    def shift_right(self, position):
        value = self._get_value()
        self._set_value(value >> position)
        return self
    
    def bitwise_and(self):
        value_b = self._get_value()
        value_a = self._get_value()
        self._set_value(value_a & value_b)
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

    # load a hardcoded value into the buffer
    def load_v8(self, value):
        self._set_value(value)
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

    def load_a16(self):
        self._cpu.pc += 1
        self.address = self._mmu.read_u16(self._cpu.pc)
        self._cpu.pc += 1
        return self
        
    def load_ra16(self, r1):
        self.address = self._cpu.reg.reg_read_dict[r1]()
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

    def store_rd8(self, r1):
        value = self._get_value()
        self._cpu.reg.reg_write_dict[r1](value)
        
    def store_rd16(self, r1):
        value = self._get_value()
        self._cpu.reg.reg_write_dict[r1](value)

    # store 8 bit data into address
    def store_a8(self):
        value = self._get_value()
        self._cpu._mmu.write(self.address, value)
        return 
    
    # store value in the loaded memory address
    def store_a16(self):
        value = self._get_value()
        self._cpu._mmu.write(self.address, value)
        self._set_value(self.address)
        return self
    
    # store 16 data into register BC,DE,HL,SP,PC
    def store_d16(self, r1):
        value = self._get_value()
        self._cpu.reg.reg_write_dict[r1](value)
        return self

    def store(self):
        return self
    