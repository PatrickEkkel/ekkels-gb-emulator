import time
import unittest
from gameboy import GameBoy
from cartridges.tetris import Tetris




class PerformanceTests(unittest.TestCase):

    def test_20second_tetris_runtime(self):
        start_time = time.time()
        game = Tetris()
        game.print_cartridge_info()
        gb = GameBoy(game)
        gb.CPU.debugger.instr_stop = 710000
        gb.power_on(skipbios=True)
        
        print(time.time() - start_time, "seconds")
        assert True


if __name__ == '__main__':
    unittest.main()
