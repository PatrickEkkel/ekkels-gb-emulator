import struct

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
        #self.init_io_registers()
        self.components = []


    def register_component(self, component):
        self.components.append(component)

    #def init_io_registers(self):
    #    self.io[0xFF00] = MMU.FF00


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

        if address == 0xFFB6:
            pass
            #input('start DMA')
        if not self._handle_write(address, value):
            # writing to VRAM
            if self._is_vram(address):
                self.vram[address] = value
            elif self._is_rom(address):
                print('ignoring rom writes')
            elif self._is_io(address):
                self.io[address] = value
            elif self._is_hram(address):
                #print('hram write')
                self.hram[address] = value
            elif self._is_wram_bank0(address):
                #print('wram bank 0')
                self.wram_bank_0[address] = value
            elif self._is_wram_bank1(address):
                #print('wram bank 1')
                self.wram_bank_1[address] = value
            elif self._is_oam(address):
                #print('wram bank oam')
                self.oam[address]  = value
            elif self._is_not_usable(address):
                pass
                #print('not usable')
            else:
                # just dump all illigal writes in this array, so we can use it for testing
                self.unmapped[address] = value
            
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
    
    def _handle_read(self, address):
        result = None
        for c in self.components:
            if c.is_in_range(address):
                result = c.read(address)
                break
        
        return result

    def _handle_write(self, address, value):
        result = False
        for c in self.components:
            if c.is_in_range(address):
                c.write(address, value)
                break
        return result
        

    def read(self, address):
        local_data = None

        # determine if we are above 0x00FF,
        # this implies that we are not trying to read addresses from the bootrom
        # everything above 0x104 to 7FFF is 'cartrdige ROM' space, switchable via MBC if available

        value =  self._handle_read(address)
            
        if value:
            return value
        else:
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
            elif self._is_wram_bank1(address):
                return self.wram_bank_1[address]
            elif self._is_wram_bank0(address):
                return self.wram_bank_0[address]
            elif self._is_oam(address):
                return self.oam[address]
            else:
                # trying to access unmapped memory
                # just return the garbage array
                return self.unmapped[address]
        
                #return 0x0000


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

    def read_u16(self,address):
        return int.from_bytes(self._getbyte(address) + self._getbyte(address + 1), 'little')
