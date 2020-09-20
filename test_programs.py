import config
import unittest 
import instructionset
from gameboy import GameBoy
from cartridges.testrom import TestRom


class ProgramTests(unittest.TestCase):

    def print_hex(self, value):
        print("0x{:x}".format(value))

    def create_gameboy(self, program):
        game = TestRom(program)
        game.print_cartridge_info()
        gb = GameBoy(game)
        gb.power_on(skipbios=True)


    # test the flags register after XOR and DEC opcodes
    def test_program1(self):
        test_program = ['NOP','JP 0150', 'JP 020C', 'LD HL DFFF','LD C 10', 'DEC B']
        bitstream = instructionset.create_bitstream(test_program)
        for b in bitstream:
            #print(b)
            self.print_hex(b)

        #gb = self.create_gameboy(test_program)
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
        




