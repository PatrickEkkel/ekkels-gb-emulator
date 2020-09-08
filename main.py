import config
from gameboy import GameBoy
from cartridges.tetris import Tetris

game = Tetris()
game.print_cartridge_info()
gb = GameBoy(game)
gb.power_on(skipbios=True)


#header = game.dump_header()
#print('[')
#for byte in header:
#    hex = "0x{:x}".format(byte)
#    print(hex + ',', end='')

#print(']')

