from .mmu import MMU
from .screen import Screen

class Tile:
    def __init__(self):
        self.rows = []
    
    def add(self, row):
        self.rows.append(row)

class TileRow:

    def __init__(self, fb, sb):
        self.fb = fb
        self.sb = sb
        self.row = []
    def decode(self):
        for x in range(7, -1, -1):
            msb = self.fb >> x & 0x01
            lsb = self.sb >> x & 0x01

            if msb and lsb:
                self.row.append(Screen.DARK_GREEN)
            elif not msb and not lsb:
                self.row.append(Screen.LIGHTEST_GREEN)
            elif msb and not lsb:
                self.row.append(Screen.DARKEST_GREEN)
            elif lsb and not msb:
                self.row.append(Screen.LIGHT_GREEN)
            

    
class GPU:
    def __init__(self, mmu, screen):
        self._mmu = mmu
        self._screen = screen

    def format_hex(self, opcode):
        return ("0x{:x}".format(opcode))

    def _decode_tile_row(self, address, offset):
        tile_row = address + offset

        fb = tile_row
        sb = tile_row + 1

        first_byte = self._mmu.read(fb)
        second_byte = self._mmu.read(sb)

        tr = TileRow(first_byte, second_byte)

        tr.decode()
        return tr



    # Test method to test if we get the GPU/Screen implementation right
    def render_nintento_logo(self):
         # loop through VRAM to get tileset info
        start =  MMU.VRAM_START
        current = start
        end = MMU.VRAM_END

        # add copyright sign to memory address 
        vram_address = 0x8190
        tile = [0x3C,0x00, 0x42, 0x00, 0xB9, 0x00,0xA5,0x00,0xB9,0x00,0xA5,0x00,0x42,0x00,0x3C,0x00]
        offset = 0
        for i in tile:
            offset_address = vram_address + offset
            self._mmu.write(offset_address, i)
            offset += 1


        #while(current < end):
        #    current += 1
        #    if current > 0x8190 and current < (0x8190 + 16):
        #        print(self.format_hex(self._mmu.read(current)))
                #print(self.format_hex(current))

        
        #print(self.format_hex(self._mmu.read(0x8190)))

        #first_byte = self._mmu.read(0x8190)
        #second_byte = self._mmu.read(0x8191)
        tile = Tile()
        for x in range(0,16,2):
            tr = self._decode_tile_row(vram_address, x)
            #print(tr)
            tile.add(tr)

        self._screen.render_tile(tile)
        #
        # 
        # print(tr.row)
