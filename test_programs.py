import config
import unittest
import instructionset
from gameboy import GameBoy
from parser import Tokenizer, GBA_ASM
from cartridges.testrom import TestRom


class ProgramTests(unittest.TestCase):

    def print_hex(self, value):
        print("0x{:x}".format(value))

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
        assert True

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

    def test_program2(self):
        test_program = ['LD C 10']
        bitstream = instructionset.create_bitstream(test_program)
        for b in bitstream:
            #print(b)
            self.print_hex(b)
        assert True




if __name__ == '__main__':
    unittest.main()
