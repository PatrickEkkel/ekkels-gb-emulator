import config
from gameboy import GameBoy
from cartridges.tetris import Tetris
import testdata

game = Tetris()
game.print_cartridge_info()

gb = GameBoy(game)
testdata.load_testdata(gb.mmu)
gb.power_on(skipbios=True)

while True:
    pass
