import config
from gameboy import GameBoy
from cartridges.tetris import Tetris
from cartridges.empty import Empty
#import testdata

game = Tetris()
game.print_cartridge_info()

gb = GameBoy(game)
gb.power_on(skipbios=False)

while True:
    pass
