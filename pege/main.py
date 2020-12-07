import config
from gameboy import GameBoy
from cartridges.tetris import Tetris
import testdata

game = Tetris()
game.print_cartridge_info()

gb = GameBoy(game)
testdata.load_testdata(gb.mmu)

#gb._init(skipbios=False)
gb.power_on(skipbios=True)
#gb.PPU.render_nintento_logo()

while True:
    pass
