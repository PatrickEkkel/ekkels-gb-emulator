from .mmu import MMU

class GPU:
    def __init__(self, mmu):
        self._mmu = mmu

    def format_hex(self, opcode):
        return ("0x{:x}".format(opcode))

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

        first_byte = self._mmu.read(0x8194)
        second_byte = self._mmu.read(0x8195)

        #print(self.format_hex(first_byte))
        #print(self.format_hex(second_byte))

        # try to get the first pixel.. 
        print('first pixel')
        
        msb = first_byte >> 7 & 0x01 
        lsb = second_byte >> 7 & 0x01
        print(msb)
        print(lsb)

        print('second pixel')
        
        msb = first_byte >> 6 & 0x01
        lsb = second_byte >> 6 & 0x01

        print(msb)
        print(lsb)

        print('third pixel')
        
        msb = first_byte >> 5 & 0x01
        lsb = second_byte >> 5 & 0x01

        print(msb)
        print(lsb)

        print('fourth pixel')
        
        msb = first_byte >> 4 & 0x01
        lsb = second_byte >> 4 & 0x01

        print(msb)
        print(lsb)

        print('fifth pixel')
        msb = first_byte >> 3 & 0x01
        lsb = second_byte >> 3 & 0x01

        print(msb)
        print(lsb)

        print('sixth pixel')
        msb = first_byte >> 2 & 0x01
        lsb = second_byte >> 2 & 0x01

        print(msb)
        print(lsb)

        print('seventh pixel')
        msb = first_byte >> 1 & 0x01
        lsb = second_byte >> 1 & 0x01


        print(msb)
        print(lsb)

        print('eigth pixel')
        msb = first_byte & 0x01
        lsb = second_byte & 0x01

        print(msb)
        print(lsb)
