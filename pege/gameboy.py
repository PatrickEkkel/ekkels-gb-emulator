from bootrom import BootRom
from components.cpu.cpu import CPU
from components.ppu import PPU
from components.clock import CPUClock
from components.screen import Screen
from components.joypad import JoyPad
from components.mmu import MMU
from constants import *
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
        self.joypad = JoyPad(self.mmu)
        if testmode:
            # just stop at 0x150, so we can test most small programs
            self.CPU.test_mode = True
            self.CPU.stop_at = 0x150
        self.PPU = PPU(self.mmu, self.screen, self._clock)

    def _init(self, skipbios):
        # disable interrupts
        #self.mmu.write(IE_REGISTER,0xFFFF)
        if skipbios:
            self.mmu.disable_bootrom()
            self.CPU.pc = 0x100
            self.CPU.reg.initialize_without_bootrom()
            
    def _run(self):
        cont = True
        while(cont):
                cont = self.CPU.step()
                self.PPU.step()

    def power_on(self,skipbios=True, standby=False):
        self._init(skipbios)
        if not standby:
            self._run()            