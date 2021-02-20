from .screen import Screen
from .mmu import MMU



class Fetcher:

    READ_TILE = 0
    READ_DATA_0 = 1
    READ_DATA_1 = 2
    PUSH_PIXELS = 3

    LY_REGISTER = 0xFF44
    LCDC_REGISTER = 0xFF40



    def __init__(self, mmu, ppu):
        self._mmu = mmu
        self.state = Fetcher.READ_TILE
        self.ppu = ppu
        self.offset = MMU.BACKGROUND_MAP_START
        self.tilemap_ram = MMU.TILERAM_START
        self.tile_address = None
        self.column = 0
        self.ticks = 0
    def update_row(self, scy):
        if scy % 8 == 0:
                self.offset += 32

    def update_column(self, scx):
        self.column = scx

    def _decode(self, fb, sb):
        result = []
        for x in range(7, -1, -1):
            msb = fb >> x & 0x01
            lsb = sb >> x & 0x01

            if msb and lsb:
                result.append(Screen.DARK_GREEN)
            elif not msb and not lsb:
                result.append(Screen.LIGHTEST_GREEN)
            elif msb and not lsb:
                result.append(Screen.DARKEST_GREEN)
            elif lsb and not msb:
                result.append(Screen.LIGHT_GREEN)
        return result


    def _read_tile(self):
        LY = self._getLY()
        #LY = self.ppu.get_LY()
        current_offset = self.offset + self.column
        tile_id = self._mmu.read(current_offset)
        self.tile_address = self.tilemap_ram + (tile_id * 16)

    def _getLY(self):
        return self._mmu.read(Fetcher.LY_REGISTER)

    def _read_data_0(self):
        address = self.tile_address
        LY = self._getLY()
        offset = (LY % 8)
        offset += offset
        tile_row = address + offset
        b = tile_row

        self.data_0 = self._mmu.read(b)

    def _read_data_1(self):
        address = self.tile_address
        b = address + 1
        self.data_1 = self._mmu.read(b)


    def step(self):
            
        self.ticks += 1
        if self.ticks < 2:
            return
        self.ticks = 0

        if self.state == Fetcher.READ_TILE:
            self._read_tile()
            self.state = Fetcher.READ_DATA_0

        elif self.state == Fetcher.READ_DATA_0:
            self._read_data_0()
            self.state = Fetcher.READ_DATA_1
        elif self.state == Fetcher.READ_DATA_1:
            self._read_data_1()
            self.state = Fetcher.PUSH_PIXELS

    def reset_fetcher(self):
        self.state = Fetcher.READ_TILE
        self.offset = MMU.BACKGROUND_MAP_START
        self.tilemap_ram = MMU.TILERAM_START
        self.tile_address = None
        self.column = 0
        self.ticks = 0


    def reset_column(self):
        self.column = 0

    def fetch():
        return self._decode(self.data_0, self.data_1)
