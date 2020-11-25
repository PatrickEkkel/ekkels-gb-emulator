from .screen import Screen
from .mmu import MMU



class Fetcher:

    def __init__(self, mmu):
        self._mmu = mmu
        self.offset = MMU.BACKGROUND_MAP_START
        self.tilemap_ram = MMU.TILERAM_START
    
    def update_offset(self, scy):
        if scy % 8 == 0:
                self.offset += 32

    
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


        
    def get_pixels(self,scx, scy):
        current_offset = self.offset + scx
        tile_id = self._mmu.read(current_offset)
        tile_address = self.tilemap_ram + (tile_id * 16)
        row = (scy % 8)
        row += row
        tr = self._decode_tile_row(tile_address,row)
        return tr

    def _decode_tile_row(self, address, offset):
        tile_row = address + offset

        fb = tile_row
        sb = tile_row + 1

        first_byte = self._mmu.read(fb)
        second_byte = self._mmu.read(sb)
        return self._decode(first_byte, second_byte)