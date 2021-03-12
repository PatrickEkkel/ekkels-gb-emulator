import time
import unittest
import cProfile
from gameboy import GameBoy
from cartridges.tetris import Tetris



def run_tetris():
    game = Tetris()
    game.print_cartridge_info()
    gb = GameBoy(game)
    gb.CPU.debugger.instr_stop = 3000000
    gb.power_on(skipbios=True)

class PerformanceTests(unittest.TestCase):

    def test_20second_tetris_runtime(self):
        start_time = time.time()
        
        cProfile.run('run_tetris()')
        #run_tetris()
        #gb.power_on(skipbios=True)
        
        print(time.time() - start_time, "seconds")
        assert True
    
  
if __name__ == '__main__':
    unittest.main()
