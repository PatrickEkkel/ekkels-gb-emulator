from bootrom import BootRom
from cpu import CPU
class GameBoy:
    cpu = CPU()
    def __init__(self, cartridge):
        
        self.bootrom = BootRom()
        self.cartridge = cartridge
    def power_on(self):
        pass
        #print(self.bootrom.data)
        