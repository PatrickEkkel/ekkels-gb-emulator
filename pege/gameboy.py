from bootrom import BootRom
from components.cpu.cpu import CPU
from components.gpu import GPU
from components.screen import Screen
from components.mmu import MMU
class GameBoy:
    
    def __init__(self, cartridge):
        self.bootrom = BootRom()
        self.cartridge = cartridge
        self.mmu = MMU()
        self.mmu.set_bios(self.bootrom)
        self.mmu.set_rom(cartridge)

        #self.screen = Screen(self.mmu)
        self.CPU = CPU(self.mmu)
        #self.GPU = GPU(self.mmu, self.screen)
        

    def _init(self, skipbios):
        if skipbios:
            self.mmu.disable_bootrom()
            self.CPU.pc = 0x100
            self.CPU.reg.initialize_without_bootrom()

        

    def power_on(self,skipbios=True):
        self._init(skipbios)
        cont = True
        while(cont):
            cont = self.CPU.step()
