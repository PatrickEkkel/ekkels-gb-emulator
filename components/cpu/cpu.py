from ..mmu import MMU
from ..debugger import Debugger

import instructionset
from . import opcodes

class Registers:

    ZERO = 0x80
    SUBSTRACT = 0x40
    HALFCARRY = 0x20
    CARRY = 0x10
    def __init__(self):
        self.SET_SP(0x0000)
        self.SET_AF(0x0000)
        self.SET_BC(0x0000)
        self.SET_DE(0x0000)
        self.SET_HL(0x0000)


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
        sp -= 1
        self.mmu.write(sp, value)
        self.cpu.reg.SET_SP(sp)

    def pop(self):
        sp = self.cpu.reg.GET_SP()
        return_val = self.mmu.read(sp)
        sp += 1
        self.cpu.reg.SET_SP(sp)
        return return_val


class CPU:
    def __init__(self, mmu):
        self.pc = 0x00
        self._mmu = mmu
        self.debug_opcode = True
        self.stack = Stack(self, mmu)
        self.reg = Registers()
        self.debugger = Debugger(self, mmu)
        self.opcodes = instructionset.create_instructionset()
        self.cb_opcodes = [None] * 255
        self.opcodes[0x31] = opcodes.LDSP16d
        self.opcodes[0xC5] = opcodes.PUSHBC
        self.opcodes[0x11] = opcodes.LDnn16d
        self.opcodes[0x32] = opcodes.LDDHL8A
        self.opcodes[0x22] = opcodes.LDDHL8A
        self.opcodes[0x20] = opcodes.JRNZn
        self.opcodes[0x28] = opcodes.JRZn
        self.opcodes[0x18] = opcodes.JRn
        self.opcodes[0x4f] = opcodes.LDnA
        self.opcodes[0x67] = opcodes.LDnA
        self.opcodes[0x57] = opcodes.LDnA
        self.opcodes[0x7b] = opcodes.LDnn
        self.opcodes[0x1E] = opcodes.LDn8d
        self.opcodes[0x2E] = opcodes.LDn8d
        self.opcodes[0x06] = opcodes.LDn8d
        self.opcodes[0x3E] = opcodes.LDn8d
        self.opcodes[0xE2] = opcodes.LDCA
        self.opcodes[0x17] = opcodes.RLA
        self.opcodes[0xC] = opcodes.INCn
        self.opcodes[0x04] = opcodes.INCn
        self.opcodes[0x23] = opcodes.INCnn
        self.opcodes[0x13] = opcodes.INCnn
        self.opcodes[0x77] = opcodes.LDHL8A
        self.opcodes[0xE0] = opcodes.LDHnA
        #self.opcodes[0xF0] = opcodes.LDHAn
        self.opcodes[0x1A] = opcodes.LDAn
        self.opcodes[0xCD] = opcodes.CALLnn
        self.opcodes[0xC1] = opcodes.POPBC
        self.opcodes[0x3D] = opcodes.DECn
        self.opcodes[0xc9] = opcodes.RET
        self.opcodes[0xFE] = opcodes.CPn
        self.opcodes[0xEA] = opcodes.LDnn16a
        self.cb_opcodes[0xcb] = opcodes.CB
        self.cb_opcodes[0x7c] = opcodes.BIT7H
        self.cb_opcodes[0x11] = opcodes.RLC




    def read_opcode(self):
        return self._mmu.read(self.pc)

    def read_lower_opcode_parameter(self):
        return self._mmu.read(self.pc) << 4 & 0xFF

    def read_upper_opcode_parameter(self):
        return self._mmu.read(self.pc) >> 4 & 0xFF

    def step(self):
        success = False
        opcode = self.read_opcode()

        hex = self.debugger.format_hex(opcode)
        hex_pc = self.debugger.format_hex(self.pc)

        if opcode == 0xcb:
            instruction = self.cb_opcodes[opcode]
        else:
            instruction = self.opcodes[opcode]
        if instruction:
            self.debugger.print_state(opcode)

            if self.debugger.debug(self.pc, opcode):
                if self.debugger.exit_at_breakpoint:
                    # stop execution by returning False
                    return False
            success = instruction(self._mmu,self)
            self.debugger.print_cpu_flags()
            self.debugger.end()
            if not success:
                print(f'Opcode failed {hex} at {hex_pc}')
        else:
            print(f'Unknown opcode {hex} at {hex_pc}')
        self.pc += 1
        return success
