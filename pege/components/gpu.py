from .mmu import MMU
from .fetcher import Fetcher
from .screen import Screen

class GPU:

    OAM_SEARCH = 0
    PIXEL_TRANSFER = 1
    VBLANK = 2
    HBLANK = 3

    def __init__(self, mmu, screen, clock):
        self._mmu = mmu
        self._screen = screen
        self._clock = clock
        self.current_mode = GPU.OAM_SEARCH
        self.LY = 0
        self._fetcher = Fetcher(mmu)


    def format_hex(self, opcode):
        return ("0x{:x}".format(opcode))

       
    def _tick(self):
        if self._clock.start_of_cycle():
            pass
        self._clock.tick()

    def step(self):

        if self._clock.lines_drawn >= 144:
            self.current_mode = GPU.VBLANK
            #print(self._clock.lines_drawn)
            #print('VBLANK')
        elif self._clock.lines_drawn > 152 and self._clock.lines_drawn < 155:
            self.current_mode = GPU.OAM_SEARCH
            #print('OAM_SEARCH')
        else:

            if self._clock.line_counter == 20 and self.current_mode == GPU.OAM_SEARCH:
                self.current_mode = GPU.PIXEL_TRANSFER
                #print('PIXEL_TRANSFER')
            elif self._clock.line_counter == 63 and self.current_mode == GPU.PIXEL_TRANSFER:
                self.current_mode = GPU.HBLANK
                #print('HBLANK')
            elif self._clock.line_counter == 114:
                self.current_mode = GPU.OAM_SEARCH
                #print('OAM_SEARCH')

        self._tick()

    def create_tile(self, vram_address):
        tilerows = []
        for x in range(0, 16, 2):
            tr = self._fetchers_decode_tile_row(vram_address, x)
            tilerows.append(tr)
        return tilerows

    # Test method to test if we get the GPU/Screen implementation right
    def render_nintento_logo(self):
         # loop through VRAM to get tileset info
        start =  MMU.VRAM_START
        current = start
        end = MMU.VRAM_END

       
        
        self.LY = 0
        pointer = 0
        for scy in range(0, self._screen.height):

            width = int(self._screen.width / 8)
            self._fetcher.update_offset(scy)
         
            for scx in range(0, width):
                tr = self._fetcher.get_pixels(scx, scy)
                self._screen.render_tile_row(tr, scy)
        
            self._screen.new_scanline()
            self._screen.update()