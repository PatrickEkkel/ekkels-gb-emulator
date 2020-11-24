from bootrom import BootRom
from components.cpu.cpu import CPU
from components.gpu import GPU
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
        self._clock = CPUClock(GameBoy.CPU_SPEED)
        self.screen = Screen(self.mmu)
        self.CPU = CPU(self.mmu, self._clock)
        #self.GPU = GPU(self.mmu, self.screen)
        self.GPU = GPU(self.mmu, self.screen, GPUCLock(GameBoy.GPU_SPEED))
        self.GPU.render_nintento_logo()



    def _init(self, skipbios):
        if skipbios:
            self.mmu.disable_bootrom()
            self.CPU.pc = 0x100
            self.CPU.reg.initialize_without_bootrom()



    def power_on(self,skipbios=True):
        self._init(skipbios)
        cont = True
        while(cont):
            #cont = self.CPU.step()
            self.GPU.step()
            #self._clock.tick()
