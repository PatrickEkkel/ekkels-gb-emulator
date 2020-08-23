import config
from gameboy import GameBoy
from cartridges.supermario2 import SuperMario2

game = SuperMario2()
game.print_cartridge_info()
gb = GameBoy(game)
gb.power_on()

