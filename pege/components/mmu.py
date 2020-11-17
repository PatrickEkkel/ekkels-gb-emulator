import struct

class MMU:
    VRAM_START             = 0x8000
    VRAM_END               = 0x9FFF

    HRAM_START             = 0xFF80
    HRAM_END               = 0xFFFE

    BOOTROM_START          = 0x0000
    BOOTROM_END            = 0x00FF

    CARTRIDGE_ROM_START    = 0x0100

    IO_REGISTER_START      = 0xFF00
    IO_REGISTER_END        = 0xFF7F

    CARTRIDGE_ROM_00_START = 0x000
    CARTRIDGE_ROM_00_END   = 0x3FFF

    CARTRIDGE_ROM_01_START = 0x4000
    CARTRIDGE_ROM_01_END   = 0x7FFF

    LY_REGISTER = 0xFF44

    def __init__(self):
        self.booted = False
        self.rom = None
        self.bios = None
        self.io = self.init_memory(MMU.IO_REGISTER_START,MMU.IO_REGISTER_END)
        self.vram = self.init_memory(MMU.VRAM_START, MMU.VRAM_END)
        self.hram = self.init_memory(MMU.HRAM_START, MMU.HRAM_END)


    def init_memory(self, start,end):
        size = end - start
        result = [0x0000] * (end + 1)
        return result

    def print_hex(self, opcode):
        return ("0x{:x}".format(opcode))


    def disable_bootrom(self):
        self.booted = True

    def set_rom(self, rom):
        self.rom = rom

    def set_bios(self, bios):
        self.bios = bios

    def write_u8(self,address, u8):
        self.data[address] = u8

    def get_high_byte(value):
        return (value >> 8) & 0xFF

    def get_low_byte(value):
        return value & 0xFF

    def write(self,address, value):
        # writing to VRAM
        if self._is_vram(address):
            self.vram[address] = value
        elif self._is_io(address):
            self.io[address] = value
        elif self._is_hram(address):
            self.hram[address] = value
        else:
            print('nothing to write')


    def _is_rom(self, address):
        return address >= MMU.CARTRIDGE_ROM_00_START and address <= MMU.CARTRIDGE_ROM_01_END

    def _is_vram(self, address):
        return address >= MMU.VRAM_START and address <= MMU.VRAM_END

    def _is_io(self, address):
        return address >= MMU.IO_REGISTER_START and address <= MMU.IO_REGISTER_END

    def _is_hram(self, address):
        return address >= MMU.HRAM_START and address <= MMU.HRAM_END

    def read(self, address):
        local_data = None

        # determine if we are above 0x00FF,
        # this implies that we are not trying to read addresses from the bootrom
        # everything above 0x104 to 7FFF is 'cartrdige ROM' space, switchable via MBC if available


        #if self.bootrom_loaded:
        #    local_data = self.data
        #else:
        #    local_data = self.bios.data

        # is the address within vram?
        if self._is_rom(address):
            if self.booted:
                return self.rom.read(address)
            elif not self.booted and address >= MMU.BOOTROM_END:
                return self.rom.read(address)
            else:
                return self.bios.read(address)
        elif self._is_hram(address):
            return self.hram[address]
        elif self._is_vram(address):
            return self.vram[address]
        elif self._is_io(address):
            return self.io[address]
        elif address == MMU.LY_REGISTER:
            return self.LY
        else:
            # trying to access unmapped memory
            return 0x0000


    def _getbyte(self,address, signed=False):
        pack_method = 'B'
        if signed:
            pack_method = 'b'

        if self.booted:
            return struct.pack(pack_method, self.rom.read(address))
        else:
            return struct.pack(pack_method, self.bios.read(address))

    def read_s8(self, address):
        result = self.read(address)
        if (result & 0x80):
            result = (result + -0xFF) - 1
        return result

    def read_u8(self, address):
        return self._getbyte(address)

    def read_u16(self,address):
        return int.from_bytes(self._getbyte(address) + self._getbyte(address + 1), 'little')
