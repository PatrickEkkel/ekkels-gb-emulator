import struct
import constants

class MemoryMap:
    def __init__(self):
        self._memory_map =  [0x0000] * (0xFFFF + 1)


    def init_read_memory_map(self):
        result = []
        for address in range(0xFFFF + 1):
            result.append(self.read)

        return result

    def init_write_memory_map(self):
        result = []
        for address in range(0xFFFF + 1):
            result.append(self.write)
        
        return result

    def read(self, address):
        return self._memory_map[address]

    def write(self, address, value):
        self._memory_map[address] = value

class MMU:

    WRAM_BANK_0_START      = 0xC000
    WRAM_BANK_0_END        = 0xCFFF 

    WRAM_BANK_1_START      = 0xD000
    WRAM_BANK_1_END        = 0xDFFF

    VRAM_START             = 0x8000
    VRAM_END               = 0x9FFF

    TILERAM_START          = 0x8000
    TILERAM_END            = 0x97FF

    BACKGROUND_MAP_START   = 0x9800
    BACKGROUND_MAP_END     = 0x9BFF

    HRAM_START             = 0xFF80
    HRAM_END               = 0xFFFE

    BOOTROM_START          = 0x0000
    BOOTROM_END            = 0x00FF

    CARTRIDGE_ROM_START    = 0x0100

    IO_REGISTER_START      = 0xFF00
    IO_REGISTER_END        = 0xFF7F

    CARTRIDGE_ROM_00_START = 0x0000
    CARTRIDGE_ROM_00_END   = 0x3FFF

    CARTRIDGE_ROM_01_START = 0x4000
    CARTRIDGE_ROM_01_END   = 0x7FFF

    NOT_USABLE_START       = 0xFEA0
    NOT_USABLE_END         = 0xFEFF

    OAM_START              = 0xFE00
    OAM_END                = 0xFE9F

    #FF00 = 0xCF


    def __init__(self):
        self.booted = False
        self.rom = None
        self.bios = None
        self.io = self.init_memory(MMU.IO_REGISTER_START,MMU.IO_REGISTER_END)
        self.vram = self.init_memory(MMU.VRAM_START, MMU.VRAM_END)
        self.hram = self.init_memory(MMU.HRAM_START, MMU.HRAM_END)
        self.wram_bank_0 = self.init_memory(MMU.WRAM_BANK_0_START, MMU.WRAM_BANK_0_END)
        self.wram_bank_1 = self.init_memory(MMU.WRAM_BANK_1_START, MMU.WRAM_BANK_1_END)
        self.oam = self.init_memory(MMU.OAM_START, MMU.OAM_END)
        self.unmapped = self.init_memory(0x0,0xFFFF)
        self._memory_device = MemoryMap()
        self._read_memory_map = self._memory_device.init_read_memory_map()
        self._write_memory_map = self._memory_device.init_write_memory_map()
        self.memory_map = self.init_memory(0x0000,0xFFFF)
        self.components = []


    #def register_component(self, component):
    #    self.components.append(component)
    
    def register_component(self, component):
        self.components.append(component)
        ppu_memory_addresses = component.get_memory_map()
        for address in ppu_memory_addresses:
            self._read_memory_map[address] = component.read
            self._write_memory_map[address] = component.write

    def init_memory(self, start, end):
        #size = end - start
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
        
        if self._is_rom(address):
            print('ignoring rom writes')
        else:
            self._write_memory_map[address](address, value)
         
    def _is_not_usable(self, address):
        return address >= MMU.NOT_USABLE_START and address <= MMU.NOT_USABLE_END

    def _is_oam(self, address):
        return address >= MMU.OAM_START and address <= MMU.OAM_END

    def _is_wram_bank0(self, address):
        return address >= MMU.WRAM_BANK_0_START and address <= MMU.WRAM_BANK_0_END

    def _is_wram_bank1(self, address):
        return address >= MMU.WRAM_BANK_1_START and address <= MMU.WRAM_BANK_1_END

    def _is_rom(self, address):
        return address >= MMU.CARTRIDGE_ROM_00_START and address <= MMU.CARTRIDGE_ROM_01_END

    def _is_vram(self, address):
        return address >= MMU.VRAM_START and address <= MMU.VRAM_END

    def _is_io(self, address):
        return address >= MMU.IO_REGISTER_START and address <= MMU.IO_REGISTER_END

    def _is_hram(self, address):
        return address >= MMU.HRAM_START and address <= MMU.HRAM_END
    
    def read(self, address):
        if self._is_rom(address):
            if self.booted:
                return self.rom.read(address)
            else:
                return self.bios.read(address)
        else:
         
            return self._read_memory_map[address](address)
  
        
    def _getbyte(self,address, signed=False):
        pack_method = 'B'
        if signed:
            pack_method = 'b'

        if self.booted:
            return struct.pack(pack_method, self.read(address))
        else:
            return struct.pack(pack_method, self.bios.read(address))

    def read_s8(self, address):
        result = self.read(address)
        if (result & 0x80):
            result = (result + -0xFF) - 1
        return result

    def read_u16(self,address):
        return int.from_bytes(self._getbyte(address) + self._getbyte(address + 1), 'little')
