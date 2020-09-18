import config
import unittest 

from gameboy import GameBoy
from cartridges.testrom import TestRom


class ProgramTests(unittest.TestCase):


    def create_gameboy(self, program):
        game = TestRom(program)
        game.print_cartridge_info()
        gb = GameBoy(game)
        gb.power_on(skipbios=True)


    # test the flags register after XOR and DEC opcodes
    def test_program1(self):
        test_program = []
        gb = self.create_gameboy(test_program)
        assert False



if __name__ == '__main__':
    unittest.main()
        




