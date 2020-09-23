import config
import unittest 
import instructionset
from gameboy import GameBoy
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
        gb = GameBoy(game)
        gb.power_on(skipbios=True)


    # test the flags register after XOR and DEC opcodes
    def test_program1(self):
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
        'loop:',
        'LDD (HL) A',
        'DEC B',
        'JRNZ loop:']
        bitstream = instructionset.create_bitstream(test_program)
        #for b in bitstream:
        #    self.print_hex(b)
        
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
        




