from bootrom import BootRom
from components.cpu.cpu import CPU
from components.screen import Screen
from components.mmu import MMU
class GameBoy:
    
    def __init__(self, cartridge):
        self.bootrom = BootRom()
        self.cartridge = cartridge
        self.mmu = MMU()
        self.mmu.set_bios(self.bootrom)
        self.mmu.set_rom(cartridge)

        self.CPU = CPU(self.mmu)
        self.Screen = Screen()

    def power_on(self,skipbios=True):

        if skipbios:
            self.mmu.disable_bootrom()
            self.CPU.pc = 0x100
            self.CPU.reg.initialize_without_bootrom()

        cont = True
        while(cont):
            cont = self.CPU.step()
