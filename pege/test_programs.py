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
        gb = GameBoy(game,testmode=True)
        if run:
            gb.power_on(skipbios=True)
        return gb

    def test_JRNZ_label_parser(self):
        gbasm = GBA_ASM()
        test_program = ['loop:', 'JRNZ loop:']
        encoded_program = gbasm.parse(test_program)
        gb = self.create_gameboy(encoded_program,run=False)
        

        assert encoded_program[0] == 0x20
        #print(gb.CPU.debugger.format_hex(encoded_program[1]))
        assert encoded_program[1] == 0x02


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


    def test_LD_D_A_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD D A']
        bitstream = gbasm.parse(test_program)
        for b in bitstream:
            self.print_hex(b)

        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0x10)
        gb._run()
        assert gb.CPU.reg.GET_D() == 0x10


    def test_CPL_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['CPL']
        bitstream = gbasm.parse(test_program)

        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0xEF)
        gb._run()
        print(gb.CPU.debugger.format_hex(gb.CPU.reg.GET_A()))
        assert gb.CPU.reg.GET_A() == 0x10
        assert gb.CPU.reg.GET_SUBSTRACT() == True
        assert gb.CPU.reg.GET_HALF_CARRY() == True


    def test_LD_H_A_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD H A']
        bitstream = gbasm.parse(test_program)
        for b in bitstream:
            self.print_hex(b)

        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0x10)
        gb._run()
        assert gb.CPU.reg.GET_H() == 0x10

    def test_LD_B_A_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD B A']
        bitstream = gbasm.parse(test_program)
        for b in bitstream:
            self.print_hex(b)

        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0x10)
        gb._run()
        assert gb.CPU.reg.GET_B() == 0x10
        
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
    
    def test_LD_A_C_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD A C']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_C(0x10)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x10
        
    def test_LD_A_E_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD A E']
        bitstream = gbasm.parse(test_program)
        #for b in bitstream:
        #    self.print_hex(b)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_E(0x10)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x10

    def test_RST_28H_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['RST 28H']
        bitstream = gbasm.parse(test_program)
        #for b in bitstream:
        #    self.print_hex(b)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_E(0x10)
        # TODO: in order to get this test to work we have to limit the amount of cycles that is possible
        #gb._run()
        

    def test_SUB_B_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['SUB B']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0x0A)
        gb.CPU.reg.SET_B(0x05)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x05
        assert gb.CPU.reg.GET_SUBSTRACT() == True

    def test_LD_A_H_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD A H']
        bitstream = gbasm.parse(test_program)
        #for b in bitstream:
        #    self.print_hex(b)

        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_H(0xAF)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0xAF

    def test_LD_A_B_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD A B']
        bitstream = gbasm.parse(test_program)
        #for b in bitstream:
        #    self.print_hex(b)

        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_B(0x10)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x10

    def test_LD_A_nnnn_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD A DF7F']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.mmu.write(0xDF7F,0xFFAA)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0xFF

    # This opcode does not exist lol
    #def test_LD_DEnn_opcode(self):
    #    gbasm = GBA_ASM()
    #    test_program = ['LD (DE) 32']
    #    bitstream = gbasm.parse(test_program)
    #    gb = self.create_gameboy(bitstream,run=False)
    #    gb.power_on(skipbios=True,standby=True)
    #    gb.CPU.reg.SET_DE(0x8000)
    #    gb._run()
    #    assert gb.mmu.read(0x8000) == 0x32


    def test_LDHLnn_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD (HL) 32']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_HL(0x8000)
        gb._run()
        assert gb.mmu.read(0x8000) == 0x32

    def test_XOR_A_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['XOR A']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0xDD)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x00
        assert gb.CPU.reg.GET_CARRY() == False
        assert gb.CPU.reg.GET_SUBSTRACT() == False
        assert gb.CPU.reg.GET_HALF_CARRY() == False
        assert gb.CPU.reg.GET_ZERO() == True

    def test_XOR_C_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['XOR C']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0xFF)
        gb.CPU.reg.SET_C(0x22)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0xDD
        assert gb.CPU.reg.GET_CARRY() == False
        assert gb.CPU.reg.GET_SUBSTRACT() == False
        assert gb.CPU.reg.GET_HALF_CARRY() == False
        assert gb.CPU.reg.GET_ZERO() == False
        
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
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_C(0x20)
        gb.CPU.reg.SET_A(0x80)
        gb._run()
        assert gb.mmu.read(0xFF20) == 0x80

    
    def test_INC_A_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['INC A']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0x01)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x02

    def test_INC_E_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['INC E']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_E(0x01)
        gb._run()
        assert gb.CPU.reg.GET_E() == 0x02

    def test_INC_C_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['INC C']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_C(0x01)
        gb._run()
        assert gb.CPU.reg.GET_C() == 0x02

    def test_OR_B_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['OR B']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_B(0xFF)
        gb.CPU.reg.SET_A(0x03)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0xFF

    def test_OR_C_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['OR C']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_C(0xFF)
        gb.CPU.reg.SET_A(0x03)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0xFF

    def test_dec_bc_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['DEC BC']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_BC(0xFFFF)
        gb._run()
        assert gb.CPU.reg.GET_BC() == 0xFFFE

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

    def test_push_pop_hl_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD HL AFBF', 'PUSH HL', 'LD HL 0000', 'POP HL']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb._run()
        assert gb.CPU.reg.GET_HL() == 0xAFBF

    def test_push_pop_af_opcode(self):
        gbasm = GBA_ASM()
        #test_program = ['LD AF AFBF', 'PUSH AF', 'LD AF 0000','POP AF']
        test_program = ['PUSH AF','LD A 00','CLRFL','POP AF']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0x10)
        gb.CPU.reg.SET_F(0x20)
        
        gb._run()
        assert gb.CPU.reg.GET_AF() == 0x1020

    def test_push_pop_de_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD DE AFBF', 'PUSH DE', 'LD DE 0000','POP DE']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb._run()
        assert gb.CPU.reg.GET_DE() == 0xAFBF

    def test_push_pop_bc_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD BC AFBF', 'PUSH BC', 'LD BC 0000','POP BC']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb._run()
        assert gb.CPU.reg.GET_BC() == 0xAFBF


    def test_inc_hl_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['INC (HL)']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_HL(0x8000)
        gb.mmu.write(0x8000,0xFFFD)
        gb._run()
        assert gb.mmu.read(0x8000) == 0xFFFE

    def test_dec_hl_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['DEC (HL)']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_HL(0x8000)
        gb.mmu.write(0x8000,0xFFFF)
        gb._run()
        assert gb.mmu.read(0x8000) == 0xFFFE

    
    def test_LD_DE_nnnn_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD DE 1234']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb._run()
        assert gb.CPU.reg.GET_DE() == 0x1234

    def test_LD_SP_nnnn_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD SP 8080']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb._run()
        assert gb.CPU.reg.GET_SP() == 0x8080

    def test_LD_BC_nnnn_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD BC 8080']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb._run()
        assert gb.CPU.reg.GET_BC() == 0x8080

    def test_LD_HL_nnnn_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD HL 8080']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb._run()
        assert gb.CPU.reg.GET_HL() == 0x8080

    def test_jp_hl_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['JP (HL)','LD DE 1234']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_HL(0x104)
        gb.CPU.reg.SET_DE(0x8080)
        gb._run()
        assert gb.CPU.reg.GET_DE() == 0x8080

    def test_RES_A_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['CB RES 0 A']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0xFF)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0xFE

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

    
    def test_ld_de_a(self):
        gbasm = GBA_ASM()
        test_program = ['LD (DE) A']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_DE(0x8000)
        gb.CPU.reg.SET_A(0xFF)
        gb._run()
        assert gb.mmu.read(0x8000) == 0xFF



    def test_ld_d_hl_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD D (HL)']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_HL(0x8000)
        gb.mmu.write(0x8000,0xFA)
        gb._run()

        assert gb.CPU.reg.GET_D() == 0xFA

    def test_swap_a_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['CB SWAP A']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0xAF)
        gb._run()
        #print(gb.CPU.debugger.format_hex(gb.CPU.reg.GET_A()))   
        assert gb.CPU.reg.GET_A() == 0xFA

    def test_ld_e_hl_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD E (HL)']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_HL(0x8000)
        gb.mmu.write(0x8000,0xFA)
        gb._run()

        assert gb.CPU.reg.GET_E() == 0xFA
    def test_ld_a_de_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD A (DE)']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_DE(0x8000)
        gb.mmu.write(0x8000,0xFA)
        gb._run()

        assert gb.CPU.reg.GET_A() == 0xFA

    def test_ld_a_hl_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD A (HL)']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_HL(0x8000)
        gb.mmu.write(0x8000,0xFA)
        gb._run()
        
        assert gb.CPU.reg.GET_A() == 0xFA

    def test_LD_E_d8_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD E 80']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb._run()
        assert gb.CPU.reg.GET_E() == 0x80

    def test_LD_B_d8_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD B 80']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb._run()
        assert gb.CPU.reg.GET_B() == 0x80

    def test_LD_C_d8_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD C 80']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb._run()
        assert gb.CPU.reg.GET_C() == 0x80

    def test_LD_A_d8_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD A 80']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x80

    def test_RETZ_opcode_non_zero(self):
        gbasm = GBA_ASM()
        test_program = ['RETZ','LD A 10','NOP']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0x20)
        gb.CPU.reg.CLEAR_ZERO()
        gb.CPU.stack.push_u16bit(0x0110)
        #for b in bitstream:
        #    self.print_hex(b)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x10

    def test_RETNZ_opcode_non_zero(self):
        gbasm = GBA_ASM()
        test_program = ['RETNZ','LD A 10','NOP']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0x20)
        gb.CPU.reg.SET_ZERO()
        gb.CPU.stack.push_u16bit(0x0110)
        #for b in bitstream:
        #    self.print_hex(b)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x10

    def test_RETZ_opcode_with_zero(self):
        gbasm = GBA_ASM()
        test_program = ['RETZ','LD A 10','NOP']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0x20)
        gb.CPU.reg.SET_ZERO()
        gb.CPU.stack.push_u16bit(0x0110)
        #for b in bitstream:
        #    self.print_hex(b)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x20

    def test_LD_L_d8_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD L 80']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb._run()
        assert gb.CPU.reg.GET_L() == 0x80

    def test_JP_Z_nnnn_opcode_zero_flag(self):
        gbasm = GBA_ASM()
        # skip over 0x0104 0x0105
        test_program = ['JPZ 0105','LD A 80 ','NOP','CB SWAP A']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_ZERO()
        gb.CPU.reg.SET_A(0x20)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x02

    def test_JP_nnnn_opcode(self):
        gbasm = GBA_ASM()
        # skip over 0x0104 0x0105
        test_program = ['JP label: ','LD A 80 ','NOP','CB SWAP A','NOP','NOP','label:','NOP']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_ZERO()
        gb.CPU.reg.SET_A(0x20)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x20

    def test_JP_Z_nnnn_opcode_non_zero_flag(self):
        gbasm = GBA_ASM()
        # don't skip over 0x0104 0x0105
        test_program = ['JPZ 0105','LD A 80 ','NOP','CB SWAP A']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.CLEAR_ZERO()
        gb.CPU.reg.SET_A(0x20)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x08
        
    def test_LD_D_d8_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD D 80']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb._run()
        assert gb.CPU.reg.GET_D() == 0x80

    def test_BIT7H_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['CB BIT 7 H']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.CPU.reg.SET_H(0xF0)
        gb.CPU.reg.CLEAR_ZERO()
        gb.power_on(skipbios=True,standby=True)
        gb._run()
        assert gb.CPU.reg.GET_ZERO() == True
        

    def test_ADD_HL_DE_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['ADD HL DE']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_DE(0x02)
        gb.CPU.reg.SET_HL(0x09)
        gb._run()
        assert gb.CPU.reg.GET_HL() == 0x0B
        
    def test_ADD_A_A_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['ADD A A']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0x24)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x48
        assert gb.CPU.reg.GET_HALF_CARRY() == False

    def test_ld_e_a(self):
        gbasm = GBA_ASM()
        test_program = ['LD E A']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0xFA)
        gb._run()
        assert gb.CPU.reg.GET_E() == 0xFA

    
    def test_LD_nnnn_A_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LD 8000 A']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0xAB)
        gb._run()
        assert gb.mmu.read(0x8000) == 0xAB

    
    def test_CP_nn_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['CP 90']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0x90)
        gb._run()

        assert gb.CPU.reg.GET_ZERO()
        assert gb.CPU.reg.GET_SUBSTRACT()
        assert gb.CPU.reg.GET_HALF_CARRY() == False
        assert gb.CPU.reg.GET_CARRY() == False


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
    # RLC opcode is still a bit 'shitty' 
    #def test_RLC_opcode(self):
    #    gbasm = GBA_ASM()
    #    test_program = ['CB RL C']
    #    bitstream = gbasm.parse(test_program)
    #    gb = self.create_gameboy(bitstream,run=False)
    #    gb.power_on(skipbios=True,standby=True)
    #    gb.CPU.reg.SET_C(0xF0)
    #    gb._run()
    #    input(gb.CPU.reg.GET_C())
        #assert gb.CPU.reg.GET_C() == 0x78
    
    def test_EI_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['EI']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.mmu.write(0xFFFF,0x0000)
        gb._run()
        assert gb.mmu.read(0xFFFF) == 0xFFFF

    def test_DI_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['DI']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.mmu.write(0xFFFF,0xFFFF)
        gb._run()
        assert gb.mmu.read(0xFFFF) == 0x0000
        
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

    def test_INC_L_opcode(self):
        gbasm = GBA_ASM()
        test_program  = ['INC L']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_L(0x02)
        gb.CPU.reg.SET_SUBSTRACT()
        gb._run()
        assert gb.CPU.reg.GET_L() == 0x03
        assert gb.CPU.reg.GET_SUBSTRACT() == False

    def test_INC_B_opcode(self):
        gbasm = GBA_ASM()
        test_program  = ['INC B']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_B(0x02)
        gb.CPU.reg.SET_SUBSTRACT()
        gb._run()
        assert gb.CPU.reg.GET_B() == 0x03
        assert gb.CPU.reg.GET_SUBSTRACT() == False

    def test_INC_D_opcode(self):
        gbasm = GBA_ASM()
        test_program  = ['INC D']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_D(0x02)
        gb.CPU.reg.SET_SUBSTRACT()
        gb._run()
        assert gb.CPU.reg.GET_D() == 0x03
        assert gb.CPU.reg.GET_SUBSTRACT() == False

    def test_INC_C_opcode(self):
        gbasm = GBA_ASM()
        test_program  = ['INC C']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_C(0x02)
        gb.CPU.reg.SET_SUBSTRACT()
        gb._run()
        assert gb.CPU.reg.GET_C() == 0x03
        assert gb.CPU.reg.GET_SUBSTRACT() == False

    def test_INC_H_opcode(self):
        gbasm = GBA_ASM()
        test_program  = ['INC H']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_H(0x02)
        gb._run()
        assert gb.CPU.reg.GET_H() == 0x03
        assert gb.CPU.reg.GET_SUBSTRACT() == False

    def test_INC_HL_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['INC HL']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_HL(0x1000)
        gb._run()

        assert gb.CPU.reg.GET_HL() == 0x1001

    def test_DEC_A_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['DEC A']

        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0xFF)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0xFE
        assert gb.CPU.reg.GET_HALF_CARRY() == True
        assert gb.CPU.reg.GET_SUBSTRACT() == True

    def test_DEC_C_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['DEC C']

        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_C(0x01)
        gb._run()
        assert gb.CPU.reg.GET_C() == 0x00
        assert gb.CPU.reg.GET_HALF_CARRY() == False
        assert gb.CPU.reg.GET_SUBSTRACT() == True
        assert gb.CPU.reg.GET_ZERO() == True

    def test_DEC_D_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['DEC D']

        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_D(0xFF)
        gb._run()
        assert gb.CPU.reg.GET_D() == 0xFE
        assert gb.CPU.reg.GET_HALF_CARRY() == True
        assert gb.CPU.reg.GET_SUBSTRACT() == True

    def test_DEC_B_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['DEC B']

        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_B(0xFF)
        gb._run()
        assert gb.CPU.reg.GET_B() == 0xFE
        assert gb.CPU.reg.GET_HALF_CARRY() == True
        assert gb.CPU.reg.GET_SUBSTRACT() == True

    def test_INC_DE_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['INC DE']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_DE(0x1000)
        gb._run()

        assert gb.CPU.reg.GET_DE() == 0x1001
    
    def test_AND_A_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['AND A']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0xFF)
        gb.CPU.reg.SET_C(0xFF)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0xFF

    def test_AND_C_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['AND C']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0xFF)
        gb.CPU.reg.SET_C(0x22)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x22

    def test_AND_nn_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['AND 0F']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_AF(0x10E0)
        for b in bitstream:
            self.print_hex(b)

        gb._run()

        print(gb.CPU.debugger.format_hex(gb.CPU.reg.GET_AF()))
       
        assert gb.CPU.reg.GET_A() == 0x00
        assert gb.CPU.reg.GET_ZERO() == True
        assert gb.CPU.reg.GET_HALF_CARRY() == True
        assert gb.CPU.reg.GET_SUBSTRACT() == False
        assert gb.CPU.reg.GET_CARRY() == False

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
    
    def test_JR_nnnn_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['JR 0104','INC A','INC A','INC A','INC A']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0x00)
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x01

    def test_LDHAn_opcode(self):
        gbasm = GBA_ASM()
        test_prgram = ['LDH 20 A']
        targeted_memory_address = 0xFF00 + 0x20
        expected_value = 0xBC
        bitstream = gbasm.parse(test_prgram)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(expected_value)
        gb._run()
        value =  gb.mmu.read(targeted_memory_address)
        assert value == expected_value

    
    def test_LDD_HL_A_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['LDD (HL-) A']
        bitstream = gbasm.parse(test_program)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_HL(0x8000)
        gb.CPU.reg.SET_A(0x80)
        gb._run()

        assert gb.CPU.reg.GET_HL() == 0x7FFF
        assert gb.mmu.read(0x8000) == 0x80

    def test_LDHAn_parse(self):
        gbasm = GBA_ASM()
        test_program = ['LDH 10 A']
        bitstream = gbasm.parse(test_program)
        #for b in bitstream:
        #    self.print_hex(b)
        assert bitstream[0] == self._get_instruction('LDH nn A')
        assert bitstream[1] == 0x10
        
    def test_LDH_r_nn_opcode(self):
        gbasm = GBA_ASM()
        test_prgram = ['LDHA 20']
        targeted_memory_address = 0xFF00 + 0x20
        expected_value = 0xABBA
        bitstream = gbasm.parse(test_prgram)
        for b in bitstream:
            self.print_hex(b)

        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.mmu.write(targeted_memory_address,0xABBA)
        gb._run()
        value =  gb.CPU.reg.GET_A()
        assert value == expected_value
    

    def test_JRNZ_r8_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['JRNZ loop:','INC A','INC A','INC A','loop:']
        bitstream = gbasm.parse(test_program)
        for b in bitstream:
            self.print_hex(b)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0x00)
        gb.CPU.reg.CLEAR_ZERO()
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x00

    def test_JRZ_r8_opcode(self):
        gbasm = GBA_ASM()
        test_program = ['JRZ loop:','INC A','INC A','INC A','loop:']
        bitstream = gbasm.parse(test_program)
        for b in bitstream:
            self.print_hex(b)
        gb = self.create_gameboy(bitstream,run=False)
        gb.power_on(skipbios=True,standby=True)
        gb.CPU.reg.SET_A(0x00)
        gb.CPU.reg.SET_ZERO()
        gb._run()
        assert gb.CPU.reg.GET_A() == 0x00

if __name__ == '__main__':
    unittest.main()
