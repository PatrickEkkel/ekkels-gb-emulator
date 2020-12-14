from bootrom import BootRom
from components.cpu.cpu import CPU
from components.ppu import PPU
from components.clock import CPUClock
from components.screen import Screen
from components.mmu import MMU
class GameBoy:
    CPU_SPEED = 4194304 # 4.1Mhz # 1.04Mhz
    def __init__(self, cartridge,testmode=False):
        self.bootrom = BootRom()
        self.cartridge = cartridge
        self.mmu = MMU()
        self.mmu.set_bios(self.bootrom)
        self.mmu.set_rom(cartridge)
        self.screen = Screen(self.mmu)
        self._clock = CPUClock(GameBoy.CPU_SPEED)

        self.CPU = CPU(self.mmu,  self._clock)
        if testmode:
            # just stop at 0x200, so we can test most small programs
            self.CPU.test_mode = True
            self.CPU.stop_at = 0x200
        self.PPU = PPU(self.mmu, self.screen, self._clock)

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
            self.PPU.step()
