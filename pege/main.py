import config
from gameboy import GameBoy
from cartridges.tetris import Tetris
from cartridges.blargh_interrupts import BlarghInterrupts
from cartridges.empty import Empty
#import testdata

game = BlarghInterrupts()
game.print_cartridge_info()

gb = GameBoy(game)
gb.power_on(skipbios=True)