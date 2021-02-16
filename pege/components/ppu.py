import time
from .mmu import MMU
from .cpu.interrupt_handler import InterruptHandler
from .fetcher import Fetcher
from .screen import Screen

class FIFO:

    def __init__(self, _screen, _ppu):
        self.pixels = []
        self._screen = _screen
        self._ppu = _ppu
        self.shift_counter = 0

    def push_block(self, pixels):
        pixels.reverse()
        for pixel in pixels:
            self.pixels.append(pixel)

    def clear(self):
        self.pixels = []

    def shift(self):
        pixel = self.pixels.pop()
        self._screen.render_pixel(self._ppu.get_LY(), pixel)

    def is_filled(self):
        return len(self.pixels) > 8

    def is_ready(self):
        return len(self.pixels) <= 8

class PPU:

    OAM_SEARCH = 0
    PIXEL_TRANSFER = 1
    VBLANK = 2
    HBLANK = 3

    LY_REGISTER = 0xFF44

    def __init__(self, _mmu, _screen, _clock):
        self._mmu = _mmu
        self._screen = _screen
        self._clock = _clock
        self.current_mode = PPU.OAM_SEARCH
        self._fetcher = Fetcher(_mmu, self)
        self._pixel_fifo = FIFO(_screen, self)
        self.ticks = 0
        self.x = 0
        self.tile_index = 0
        self.tc = 0

    def format_hex(self, opcode):
        return ("0x{:x}".format(opcode))

    def _oam_search(self):
        pass

    def _do_hblank(self):
        self.current_mode = PPU.HBLANK
        self._screen.new_scanline()
        self._increment_ly()
        ly = self.get_LY()
        self._fetcher.update_row(self.get_LY())
        self._pixel_fifo.clear()
        self.x = 0
        self.tc = 0
        self.tile_index = 0

    def _do_vblank(self):
        interrupt_flags = self._mmu.read(InterruptHandler.IF)
        interrupt_flags = interrupt_flags | 0x0040
        self._mmu.write(InterruptHandler.IF, interrupt_flags)
        self.current_mode = PPU.VBLANK
        self._increment_ly()


    def _refresh_screen(self):
        self.set_LY(0)
        self._fetcher.reset_fetcher()
        self._screen.update()

    def _update_tile_index(self):
        self.tc += 1
        if self.tc == 8:
            self.tc = 0
            self.tile_index += 1
            self._fetcher.update_column(self.tile_index)

    def _increment_ly(self):
        ly =  self.get_LY()
        ly += 1
        self.set_LY(ly)

    def set_LY(self, value):
        self._mmu.write(PPU.LY_REGISTER, value)

    def get_LY(self):
        return self._mmu.read(PPU.LY_REGISTER)

    def _pixel_transfer(self):
        self._fetcher.step()
        if self.x == 160:
            self._do_hblank()
        else:
            if self._pixel_fifo.is_filled():
                self._pixel_fifo.shift()
                self.x += 1
                self._update_tile_index()

            if self._fetcher.state == Fetcher.PUSH_PIXELS:
                if self._pixel_fifo.is_ready():
                    pixels = self._fetcher._decode(self._fetcher.data_0, self._fetcher.data_1)
                    self._pixel_fifo.push_block(pixels)
                    self._fetcher.state = Fetcher.READ_TILE

    def _hblank(self):
        pass

    def _vblank(self):
        pass
    def step(self):
        if self.current_mode == self.OAM_SEARCH and self.ticks == 80:
            self._oam_search()
            self.current_mode = PPU.PIXEL_TRANSFER
        elif self.current_mode == PPU.PIXEL_TRANSFER:
            self._pixel_transfer()
        elif self.current_mode == PPU.VBLANK:
            self._vblank()
        elif self.current_mode == PPU.HBLANK:
            self._hblank()

        if self.ticks == 456:
            self.ticks = 0
            #if self.get_LY() == 144:
            if self.get_LY() >= 144 and self.get_LY() < 153:
                self._do_vblank()
            elif self.get_LY() == 153:
                self._refresh_screen()
            elif self.current_mode == PPU.HBLANK:
                self.current_mode = PPU.OAM_SEARCH
            else:
                self.current_mode = PPU.OAM_SEARCH

        self.ticks += 1
