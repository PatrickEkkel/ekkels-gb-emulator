import config
from gameboy import GameBoy
from cartridges.tetris import Tetris

game = Tetris()
game.print_cartridge_info()
gb = GameBoy(game)

gb._init(skipbios=False)
#gb.power_on(skipbios=True)
gb.GPU.render_nintento_logo()

while(True):
    pass

