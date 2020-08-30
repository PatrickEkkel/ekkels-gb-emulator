from bootrom import BootRom
from emulator import CPU, MMU
class GameBoy:
    def __init__(self, cartridge):
        self.bootrom = BootRom()
        self.cartridge = cartridge
        self.mmu = MMU()
        self.mmu.set_bios(self.bootrom)
        self.mmu.set_rom(cartridge)

        self.CPU = CPU(self.mmu)

    def power_on(self):
        cont = True
        while(cont):
            cont = self.CPU.step()
        