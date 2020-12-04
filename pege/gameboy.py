from bootrom import BootRom
from components.cpu.cpu import CPU
from components.ppu import PPU
from components.clock import CPUClock,GPUCLock
from components.screen import Screen
from components.mmu import MMU
class GameBoy:
    CPU_SPEED = 4194304 # 4.1Mhz
    GPU_SPEED = 1048576 # 1.04Mhz
    def __init__(self, cartridge):
        self.bootrom = BootRom()
        self.cartridge = cartridge
        self.mmu = MMU()
        self.mmu.set_bios(self.bootrom)
        self.mmu.set_rom(cartridge)
        self.screen = Screen(self.mmu)
        self.CPU = CPU(self.mmu,  CPUClock(GameBoy.CPU_SPEED))
        #self.GPU = GPU(self.mmu, self.screen)
        self.PPU = PPU(self.mmu, self.screen, GPUCLock(GameBoy.GPU_SPEED))
        #self.PPU.render_nintento_logo()



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
            #self.PPU.step()
