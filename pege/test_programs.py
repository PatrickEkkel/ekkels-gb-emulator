import config
import unittest
import instructionset
from gameboy import GameBoy
from parser import Tokenizer, GBA_ASM
from cartridges.testrom import TestRom


class ProgramTests(unittest.TestCase):

    def print_hex(self, value):
        print("0x{:x}".format(value))


    def _get_instruction(self, mnemonic, register='x'):
        instructions = instructionset.create_mnemonic_dictionary()

        return instructions[mnemonic]['register_options'][register]

    def create_gameboy(self, program,run=True):

        romdata = [0x0000] * 65535
        pc = 0x0100
        for instruction in program:
            romdata[pc] = instruction
            pc += 1

        game = TestRom(romdata)
        game.print_cartridge_info()
        #print(game)
        gb = GameBoy(game,testmode=True)
        if run:
            gb.power_on(skipbios=True)
        return gb


    def test_JRNZ_label_parser(self):
        gbasm = GBA_ASM()
        test_program = ['loop:', 'JRNZ loop:']
        encoded_program = gbasm.parse(test_program)

        #gb = self.create_gameboy(encoded_program)

        assert encoded_program[0] == 0x20
        assert encoded_program[1] == 0x00

    def test_JRNZ_label_tokenizer(self):
        tokenizer = Tokenizer()
        line = 'JRNZ loop:'
        opcode = tokenizer.tokenize(line)

        assert opcode.label == 'loop:'
        assert opcode.mnemonic == 'JRNZ'

    # test the flags register after XOR and DEC opcodes
    def test_program1(self):
        gbasm = GBA_ASM()
        instructions = instructionset.create_mnemonic_dictionary()
        test_program = [
        'NOP',
        'JP start:',
        'start:',
        'JP init:',
        'NOP',
        'init:',
        'LD HL DFFF',
        'LD C 10',
        'LD B 00',
        'loop:',]

        bitstream = gbasm.parse(test_program)
        for b in bitstream:
            self.print_hex(b)
       # gb = self.create_gameboy(bitstream)
        assert bitstream[0] == self._get_instruction('NOP')
        assert bitstream[1] == self._get_instruction('JP nnnn')
        assert bitstream[2] == 0x4
        assert bitstream[3] == 0x1
        assert bitstream[4] == self._get_instruction('JP nnnn')
        assert bitstream[5] == 0x8
        assert bitstream[6] == 0x1
        assert bitstream[7] == self._get_instruction('NOP')
        assert bitstream[8] == self._get_instruction('LD rr nnnn',register='HL')
        assert bitstream[9] == 0xFF
        assert bitstream[10] == 0xDF
        assert bitstream[11] == self._get_instruction('LD r nn',register='C')
        assert bitstream[12] == 0x10
        assert bitstream[13] ==  self._get_instruction('LD r nn',register='B')

    def test_program5(self):
        gbasm = GBA_ASM()
        test_program = ['LD HL DFFF','LD C 10','LD B 00']
        bitstream = gbasm.parse(test_program)

        assert bitstream[0] == self._get_instruction('LD rr nnnn', register='HL')
        assert bitstream[1] == 0xFF
        assert bitstream[2] == 0xDF
        assert bitstream[3] == self._get_instruction('LD r nn', register='C')
        assert bitstream[4] == 0x10
        assert bitstream[5] == self._get_instruction('LD r nn', register='B')

    def test_program4(self):
        gbasm = GBA_ASM()
        test_program = ['LD HL DFFF','LD C 10']
        bitstream = gbasm.parse(test_program)

        assert bitstream[0] == self._get_instruction('LD rr nnnn', register='HL')
        assert bitstream[1] == 0xFF
        assert bitstream[2] == 0xDF
        assert bitstream[3] == self._get_instruction('LD r nn', register='C')
        assert bitstream[4] == 0x10
    # TODO, add asserts

    def test_program3(self):
        gbasm = GBA_ASM()
        test_program = [
        'NOP',
        'JP start:',
        'start:',
        'JP init:',
        'init:',
        'JP blurp:',
        'blurp:']

        bitstream = gbasm.parse(test_program)
        for b in bitstream:
            self.print_hex(b)
        #gb = self.create_gameboy(bitstream)
        assert True
    # TODO, add asserts
    def test_program7(self):
        gbasm = GBA_ASM()

        test_program = ['start:','LDD (HL-) A','DEC B','JRNZ start:']
        bitstream = gbasm.parse(test_program)


    # TODO, add asserts
    def test_program6(self):
        gbasm = GBA_ASM()

        test_program = [
        'XOR A',
        'LD HL DFFF',
        'LD C 10',
        'LD B 00',
        'start:',
        'LDD (HL-) A',
        'DEC B',
        'JRNZ start:',
        'DEC C',
        'JRNZ start:']
        bitstream = gbasm.parse(test_program)
        for b in bitstream:
            self.print_hex(b)

        return True

    # TODO, add asserts
    def test_program8(self):
        gbasm = GBA_ASM()
        test_program = ['LD C 00']
        bitstream = gbasm.parse(test_program)
        for b in bitstream:
            self.print_hex(b)

    def test_program2(self):
        gbasm = GBA_ASM()
        test_program = ['LD C 10']
        bitstream = gbasm.parse(test_program)

        assert bitstream[0] == self._get_instruction('LD r nn', register='C')
        assert bitstream[1] == 0x10


    def test_LD_C_A_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD C A']
        bitstream = gbasm.parse(test_program)
        for b in bitstream:
            self.print_hex(b)

        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0x10)
        gb._run()
        assert gb.CPU.reg.GET_C() == 0x10

    def test_LD_A_B_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD A B']
        bitstream = gbasm.parse(test_program)
        for b in bitstream:
            self.print_hex(b)

        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_B(0x10)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x10

    def test_LDHLnn_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD HL 32']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream)
        assert gb.CPU.reg.GET_HL() == 0x32

    def test_LDSP16d_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD SP 1111']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream)
        assert gb.CPU.reg.GET_SP() == 0x1111
        assert bitstream[0] == 0x31
        assert bitstream[1] == 0x11
        assert bitstream[2] == 0x11

    def test_LDCA_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD (C) A']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream)

    def test_INCn_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['INC C']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_C(0x01)
        gb._run()
        assert gb.CPU.reg.GET_C() == 0x02

    def test_or_c_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['OR C']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_C(0xFF)
        gb.CPU.reg.SET_A(0x03)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0xFF

    def test_push_bc_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['PUSH BC']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_BC(0xAFAF)
        #input(gb.CPU.debugger.format_hex(gb.CPU.reg.GET_SP()))

        gb._run()
        assert gb.mmu.read(0xFFFE) == 0xAF
        assert gb.mmu.read(0xFFFD) == 0xAF
        #input(gb.CPU.debugger.format_hex(gb.CPU.reg.GET_SP()))

    def test_push_pop_bc_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD BC AFBF', 'PUSH BC', 'LD BC 0000','POP BC']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb._run()
        assert gb.CPU.reg.GET_BC() == 0xAFBF

    def test_ld_hl_a(self):
        gbasm = GBA_ASM()
        test_program = ['LD (HL) A']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_HL(0x8000)
        gb.CPU.reg.SET_A(0xFF)
        gb._run()
        assert gb.mmu.read(0x8000) == 0xFF

    def test_ld_a_de(self):
        gbasm = GBA_ASM()
        test_program = ['LD A (DE)']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_DE(0x8000)
        gb.mmu.write(0x8000,0xFA)
        gb._run()

        assert gb.CPU.reg.GET_A() == 0xFA


    def test_CALLnn_opcode(self):
        gbasm = GBA_ASM()

        test_program = ['CALL func:', 'INC C','func:','INC B']
        bitstream = gbasm.parse(test_program)
        for b in bitstream:
            self.print_hex(b)

        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_B(0x01)
        gb.CPU.reg.SET_C(0x00)
        gb._run()
        assert gb.CPU.reg.GET_B() == 0x02
        assert gb.CPU.reg.GET_C() == 0x00

        assert bitstream[0] == 0xCD
        assert bitstream[1] == 0x04
        assert bitstream[2] == 0x01
        assert bitstream[3] == 0x0C
        assert bitstream[4] == 0x04


    # Put A into memory address HL. Increment HL.
    def test_LDI_HL_A_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LDI (HL+) A']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0x10)
        gb.mmu.write(0x8000,0xFFFF)
        gb.CPU.reg.SET_HL(0x8000)
        gb._run()
        assert gb.CPU.reg.GET_HL() == 0x8001
        assert gb.mmu.read(0x8000) == 0x10

    # Put value at address HL into A. Increment HL.
    def test_LDI_A_HL_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LDI A (HL+)']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.mmu.write(0x8000,0x100)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_HL(0x8000)
        gb._run()
        assert gb.CPU.reg.GET_HL() == 0x8001
        assert gb.CPU.reg.GET_A() == 0x100

    # TODO: finish up
    #def test_LDHLnn_parse(self):
    #    gbasm = GBA_ASM()
    #    test_program = ['LD HL 32', 'LD A C']
        #test_program = ['LD A C']
    #    bitstream = gbasm.parse(test_program)

        #for b in bitstream:
        #    self.print_hex(b)

        #assert bitstream[0] == self._get_instruction('LD rr nn', register='HL')
        #assert bitstream[1] == 0x32
        #assert bitstream[2] == self._get_instruction('LD r r', register='A C')

    def test_LDHAn_parse(self):
        gbasm = GBA_ASM()
        test_program = ['LDH 10 A']
        bitstream = gbasm.parse(test_program)
        #for b in bitstream:
        #    self.print_hex(b)
        assert bitstream[0] == self._get_instruction('LDH nn A')
        assert bitstream[1] == 0x10

if __name__ == '__main__':
    unittest.main()
