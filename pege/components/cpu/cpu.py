from ..mmu import MMU
from ..debugger import Debugger
from .opcode_dsl import OpcodeContext
from .opcode_dsl_new import NewOpcodeContext
from .interrupt_handler import InterruptHandler
import time
import instructionset
from instructionset import opcode_descriptions
from constants import *
from . import opcodes


class Registers:

    ZERO = 0x80
    SUBSTRACT = 0x40
    HALFCARRY = 0x20
    CARRY = 0x10
    def __init__(self, _cpu):
        self._cpu = _cpu
        self.SET_SP(0x0000)
        self.SET_AF(0x0000)
        self.SET_BC(0x0000)
        self.SET_DE(0x0000)
        self.SET_HL(0x0000)
        self.reg_read_dict = {r_AF: self.GET_AF,
                              r_A: self.GET_A,
                              r_C: self.GET_C,
                              r_H: self.GET_H,
                              r_PC: self.GET_PC }

        self.reg_write_dict = {r_AF: self.SET_AF,
                               r_DE: self.SET_DE,
                               r_SP: self.SET_SP,
                               r_HL: self.SET_HL,
                               r_BC: self.SET_BC,
                               r_A:  self.SET_A,
                               r_C:  self.SET_C,
                               r_PC: self.SET_PC }


    def _set_flag(self, flag):
        F = self.GET_F()
        F = flag | F
        self.SET_F(F)

    def _clear_flag(self, flag):
        F = self.GET_F()
        F = ~flag & F
        self.SET_F(F)

    def _get_flag(self, flag):
        return (self.GET_F() & flag) > 0

    def _write_register(self,value):
        if value < 0x00:
            return 0xff
        else:
            return value
    def SET_CARRY(self):
        self._set_flag(Registers.CARRY)

    def GET_CARRY(self):
        return self._get_flag(Registers.CARRY)

    def CLEAR_CARRY(self):
        return self._clear_flag(Registers.CARRY)

    def SET_HALF_CARRY(self):
        self._set_flag(Registers.HALFCARRY)

    def GET_HALF_CARRY(self):
        return self._get_flag(Registers.HALFCARRY)

    def CLEAR_HALF_CARRY(self):
        return self._clear_flag(Registers.HALFCARRY)

    def CLEAR_ZERO(self):
        self._clear_flag(Registers.ZERO)

    def SET_ZERO(self):
        self._set_flag(Registers.ZERO)

    def GET_ZERO(self):
        return self._get_flag(Registers.ZERO)

    def CLEAR_SUBSTRACT(self):
        self._clear_flag(Registers.SUBSTRACT)

    def SET_SUBSTRACT(self):
        self._set_flag(Registers.SUBSTRACT)

    def GET_SUBSTRACT(self):
        return self._get_flag(Registers.SUBSTRACT)

    def SET_SP(self, value):
        self.sp = value

    def GET_SP(self):
        return self.sp

    def SET_AF(self, value):
        self.A = MMU.get_high_byte(value)
        self.F = MMU.get_low_byte(value)
        self.AF = value

    def SET_B(self, value):
        self.B = self._write_register(value)

    def SET_C(self, value):
        self.C = self._write_register(value)

    def SET_D(self, value):
        self.D = self._write_register(value)

    def SET_E(self, value):
        self.E = self._write_register(value)

    def SET_DE(self, value):
        self.D = MMU.get_high_byte(value)
        self.E = MMU.get_low_byte(value)
        self.DE = value

    def SET_HL(self, value):
        self.H = MMU.get_high_byte(value)
        self.L = MMU.get_low_byte(value)
        self.HL = value


    def GET_A(self):
        return self.A

    def GET_F(self):
        return self.F

    def SET_A(self, value):
        self.A = self._write_register(value)

    def SET_F(self, value):
        self.F = self._write_register(value)

    def SET_L(self, value):
        self.L = self._write_register(value)

    def SET_H(self, value):
        self.H = self._write_register(value)

    def GET_AF(self):
        return (self.GET_A() << 8) | self.GET_F()

    def GET_B(self):
        return self.B

    def GET_C(self):
        return self.C
    
    def SET_PC(self, value):
        self._cpu.pc = value

    def SET_BC(self, value):
        self.B = MMU.get_high_byte(value)
        self.C = MMU.get_low_byte(value)
        self.BC = value

    def GET_BC(self):
        return (self.GET_B() << 8) | self.GET_C()

    def GET_DE(self):
        return (self.GET_D() << 8) | self.GET_E()


    def GET_D(self):
        return self.D

    def GET_E(self):
        return self.E

    def GET_H(self):
        return self.H

    def GET_L(self):
        return self.L

    def GET_HL(self):
        return (self.GET_H() << 8) | self.GET_L()
        #return self.hl
    def GET_PC(self):
        return self._cpu.pc

    def initialize_without_bootrom(self):
        self.SET_BC(0x0013)
        #self.SET_AF(0x01B0)
        self.SET_AF(0x0000)
        self.SET_DE(0x00D8)
        self.SET_HL(0x014D)
        self.SET_SP(0xFFFE)

class Stack:

    def __init__(self, cpu, mmu):
        self.mmu = mmu
        self.cpu = cpu

    def push_u16bit(self, value):
        lowbyte = MMU.get_high_byte(value)
        highbyte = MMU.get_low_byte(value)
        self.push(lowbyte)
        self.push(highbyte)
        

    def push(self, value):
        sp = self.cpu.reg.GET_SP()
        self.mmu.write(sp, value)
        sp -= 1
        self.cpu.reg.SET_SP(sp)

    def pop(self):
        sp = self.cpu.reg.GET_SP()
        sp += 1
        return_val = self.mmu.read(sp)
        self.cpu.reg.SET_SP(sp)
        return return_val


class CPU:
    def __init__(self, mmu, clock):
        self.pc = 0x00
        self.print_counter = 0
        self._mmu = mmu
        self._clock = clock
        self.disable_cpu = False
        self.test_mode = False
        self.stop_at = None
        self.stack = Stack(self, mmu)
        self.interrupt_handler = InterruptHandler(mmu, self)
        self.reg = Registers(self)
        self.debugger = Debugger(self, mmu)
        self.opcodes = instructionset.create_opcode_map('opcode')
        self.opcode_cycles = instructionset.create_opcode_map('cycles')
        self.opcode_meta = instructionset.create_opcode_metamap()
        self.cb_opcode_meta = instructionset.create_cb_opcode_metamap()
        self.opcode_contexts = instructionset.create_opcode_contexts(self, self._mmu)
        self.cb_opcode_contexts = instructionset.create_cb_opcode_contexts(self, self._mmu)
        self.cb_opcodes = instructionset.create_cb_opcode_map('opcode')

        self.opcodes[0x20] = opcodes.JRNZn
        self.opcodes[0x28] = opcodes.JRZn
        self.opcodes[0x06] = opcodes.LD_r_nn

    def read_opcode(self):
        # PUT CPU in execute NOP forever, very handy when working on GPU
        if self.disable_cpu:
            return 0x00
        else:
            return self._mmu.read(self.pc)

    def read_lower_opcode_parameter(self):
        return self._mmu.read(self.pc) << 4 & 0xFF

    def read_upper_opcode_parameter(self):
        return self._mmu.read(self.pc) >> 4 & 0xFF
    
    def _handle_opcode_failure(self, opcode):
         hex = self.debugger.format_hex(opcode)
         hex_pc = self.debugger.format_hex(self.pc)
         print(f'Opcode failed {hex} at {hex_pc}')
    
    def _handle_unknown_opcode(self, opcode):
        hex = self.debugger.format_hex(opcode)
        hex_pc = self.debugger.format_hex(self.pc)
        print(f'Unknown opcode {hex} at {hex_pc}')

    def debug(self, context, opcode):
        result = True
        self.debugger.print_state(opcode)
        if self.debugger.debug(self.pc, opcode):
            if self.debugger.exit_at_breakpoint:
                # stop execution by returning False
                result = True
        self.debugger.print_opcode(context.opcode)
        return result
        

    def step(self):
        if self.test_mode and self.pc == self.stop_at:
            return False
        
        # handle interrupts 
        self.interrupt_handler.step()
        success = False
        opcode = self.read_opcode()
        opcode_meta = None
        if opcode == 0xcb:
            instruction = self.cb_opcodes[opcode]
            opcode_meta = self.cb_opcode_meta[opcode]
            context  =   self.cb_opcode_contexts[opcode]
        else:
            instruction = self.opcodes[opcode]
            opcode_meta = self.opcode_meta[opcode]
            context = self.opcode_contexts[opcode]
        if instruction:
            context.init()
            success = self.debug(context, opcode)
            instruction(self._mmu,self, opcode_meta, context)
            cycle = context.opcode.get_cycles()
            self.debugger.print_cpu_flags()
            self.debugger.end()
            if cycle == -1:
                self._handle_opcode_failure(opcode)
                success = False
            else:
                self._clock.update(cycle)
                success = True
        else:
            self._handle_unknown_opcode(opcode)
        self.pc += 1
        return success
        