import config
from gameboy import GameBoy
from cartridges.tetris import Tetris
from cartridges.empty import Empty
#import testdata

game = Empty()
game.print_cartridge_info()

gb = GameBoy(game)
#testdata.load_testdata(gb.mmu)
gb.power_on(skipbios=False)

while True:
    pass
