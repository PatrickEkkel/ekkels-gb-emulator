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

    def create_gameboy(self, program):

        romdata = [0x0000] * 65535
        pc = 0x0100
        for instruction in program:
            romdata[pc] = instruction
            pc += 1

        game = TestRom(romdata)
        game.print_cartridge_info()
        #print(game)
        gb = GameBoy(game)
        gb.power_on(skipbios=True)


    def test_JRNZ_label_parser(self):
        gbasm = GBA_ASM()
        test_program = ['loop:', 'JRNZ loop:']
        encoded_program = gbasm.parse(test_program)

        #gb = self.create_gameboy(encoded_program)

        assert encoded_program[0] == 0x20
        assert encoded_program[1] == 0x00

    def test_predefined_label(self):
        gbasm = GBA_ASM()
        test_program = ['JP start:','start:']

        encoded_program = gbasm.parse(test_program)

        assert encoded_program[0] == 0xC3
        assert encoded_program[1] == 0x01

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
        gb = self.create_gameboy(bitstream)
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
        gb = self.create_gameboy(bitstream)
        assert True

    def test_program7(self):
        gbasm = GBA_ASM()

        test_program = ['start:','LDD (HL-) A','DEC B','JRNZ start:']
        bitstream = gbasm.parse(test_program)



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

        gb = self.create_gameboy(bitstream)

        #gb.power_on()


        return True

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

if __name__ == '__main__':
    unittest.main()
