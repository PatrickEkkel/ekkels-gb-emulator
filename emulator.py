import struct
import opcodes
from array import array

class Stack:

    def __init__(self, cpu, mmu):
        self.mmu = mmu
        self.cpu = cpu
    
    def push(self, value):
        sp = self.cpu.reg.GET_SP()
        sp -= 1
        self.mmu.write(sp, value)
        self.cpu.reg.SET_SP(sp)
    
    def pop(self):
        sp = self.cpu.reg.GET_SP()
        return_val = self.mmu.read(sp)
        sp += 1
        self.cpu.reg.SET_SP(sp)
        return return_val

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
            print('vram is writing')
            self.vram[address] = value
        elif self._is_io(address):
            print('io is writing')
            # do nothing with I/O until it is needed
            self.io[address] = value
        elif self._is_hram(address):
            print('hram is writing')
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
        

class Debugger:

    def __init__(self, cpu):
        self.cpu = cpu
        self.show_registers = True
        self.show_opcodes = True
        self.show_cpu_flags = False
        self.show_program_counter = True
    
    def format_hex(self, opcode):
        return ("0x{:x}".format(opcode))

    def print_opcode(self, opcode_description):
        if self.cpu.debug_opcode:
            print(opcode_description, end=' ')

    def print_register(self, name, value, size):
        if self.cpu.debug_opcode and self.show_registers:
            hex = self.format_hex(value)
            print(f'REG: {name}: {hex} size: {size}', end=' ')

    def print_iv(self, value):
        if self.cpu.debug_opcode and self.show_opcodes:
            hex = self.format_hex(value)
            print(f'{hex} ',end=' ')

    def end(self):
        print('')

    def print_cpu_flags(self):
        if self.cpu.debug_opcode and self.show_cpu_flags:
            hex = self.format_hex(self.cpu.reg.GET_F())
            print(f'FLAGS-REG: {hex}')

    def print_state(self, data):
        hex = self.format_hex(data)
        hex_pc = self.format_hex(self.cpu.pc)
        if self.cpu.debug_opcode and self.show_program_counter:
            print(f'PC: {hex_pc} CPU: {hex}', end=' ')


class Registers:

    ZERO = 0x80
    SUBSTRACT = 0x40
    HALFCARRY = 0x20
    CARRY = 0x10
    def __init__(self):
        self.SET_SP(0x0000)
        self.SET_AF(0x0000)
        self.SET_BC(0x0000)
        self.SET_DE(0x0000)
        self.SET_HL(0x0000)
        
    
    def _set_flag(self, flag):
        F = self.GET_F()
        F = flag | F
        self.SET_F(F)
    
    def _clear_flag(self, flag):
        F = self.GET_F()
        F = ~flag & F
        self.SET_F(F)

    def _get_flag(self, flag):
        return (self.GET_F() & flag) > 0


    def SET_CARRY(self):
        self._set_flag(Registers.CARRY)

    def GET_CARRY(self):
        return self._get_flag(Registers.CARRY)

    def CLEAR_CARRY(self):
        return self._clear_flag(Registers.CARRY)

    def SET_HALF_CARRY(self):
        self._set_flag(Registers.HALFCARRY)
    
    def GET_HALF_CARRY(self):
        return self._get_flag(Registers.HALFCARRY)

    def CLEAR_HALF_CARRY(self):
        return self._clear_flag(Registers.HALFCARRY)

    def CLEAR_ZERO(self):
        self._clear_flag(Registers.ZERO)

    def SET_ZERO(self):
        self._set_flag(Registers.ZERO)

    def GET_ZERO(self):
        return self._get_flag(Registers.ZERO)

    def CLEAR_SUBSTRACT(self):
        self._clear_flag(Registers.SUBSTRACT)
    
    def SET_SUBSTRACT(self):
        self._set_flag(Registers.SUBSTRACT)
    
    def GET_SUBSTRACT(self):
        return self._get_flag(Registers.SUBSTRACT)

    def SET_SP(self, value):
        self.sp = value
    
    def GET_SP(self):
        return self.sp

    def SET_AF(self, value):
        self.A = MMU.get_high_byte(value)
        self.F = MMU.get_low_byte(value)
        self.AF = value

    def SET_B(self, value):
        C = MMU.get_low_byte(self.bc)
        B = value
        B = B << 8
        self.bc = C | B


    def SET_C(self, value):
        C = value
        B = MMU.get_high_byte(self.bc)
        self.bc = B | C


    def SET_DE(self, value):
        self.de = value

    #def SET_D(self, value):
    #    self.d = value

    #def SET_E(self, value):
    #    self.e = value
    
    def SET_HL(self, value):
        self.hl = value
    

    def GET_A(self):
        return self.A
    
    def GET_F(self):
        return self.F

    def SET_A(self, value):
        self.A = value
        #F = MMU.get_low_byte(self.af)
        #A = value
        #A = A << 8
        #self.af = F | A

    def SET_F(self, value):
        self.F = value
        #F = value
        #A = MMU.get_high_byte(self.af)
        #self.af = A | F

    def GET_AF(self):
        return (self.GET_A() << 8) | self.GET_F()

    def GET_B(self):
        return MMU.get_high_byte(self.bc)
    
    def GET_C(self):
        return MMU.get_low_byte(self.bc)

    def SET_BC(self, value):
        self.bc = value

    def GET_BC(self):
        return self.bc

    def GET_DE(self):
        return self.de

    def GET_D(self):
        return MMU.get_high_byte(self.de)

    def GET_E(self):
        return MMU.get_low_byte(self.de)
    
    def GET_HL(self):
        return self.hl
    
class CPU:
    def __init__(self, mmu):
        self.pc = 0x00
        self._mmu = mmu
        self.debug_opcode = True
        self.stack = Stack(self, mmu)
        self.reg = Registers()
        self.debugger = Debugger(self)
        self.opcodes = [None] * 255
        self.cb_opcodes = [None] * 255
        self.opcodes[0x31] = opcodes.LDSP16d
        self.opcodes[0xAF] = opcodes.XORA
        self.opcodes[0xC5] = opcodes.PUSHBC
        self.opcodes[0x21] = opcodes.LDnn16d
        self.opcodes[0x11] = opcodes.LDnn16d
        self.opcodes[0x32] = opcodes.LDDHL8A
        self.opcodes[0x20] = opcodes.JRNZN
        self.opcodes[0x4f] = opcodes.LDnA
        self.opcodes[0x0E] = opcodes.LDn8d
        self.opcodes[0x06] = opcodes.LDn8d
        self.opcodes[0x3E] = opcodes.LDn8d
        self.opcodes[0xE2] = opcodes.LDCA
        self.opcodes[0x17] = opcodes.RLA
        self.opcodes[0xC] = opcodes.INCn
        self.opcodes[0x77] = opcodes.LDHL8A
        self.opcodes[0xE0] = opcodes.LDHnA
        self.opcodes[0x1A] = opcodes.LDAn
        self.opcodes[0xCD] = opcodes.CALLnn
        self.opcodes[0xC1] = opcodes.POPBC
        self.cb_opcodes[0xcb] = opcodes.CB
        self.cb_opcodes[0x7c] = opcodes.BIT7H
        self.cb_opcodes[0x11] = opcodes.RLC


    
    def read_opcode(self):
        return self._mmu.read(self.pc)
    
    def read_lower_opcode_parameter(self):
        return self._mmu.read(self.pc) << 4

    def read_upper_opcode_parameter(self):
        return self._mmu.read(self.pc) >> 4

    def step(self):
        success = False
        opcode = self.read_opcode()
        
        hex = self.debugger.format_hex(opcode)
        hex_pc = self.debugger.format_hex(self.pc)
        
        if opcode == 0xcb:
            instruction = self.cb_opcodes[opcode]
        else:    
            instruction = self.opcodes[opcode]
        if instruction:
            self.debugger.print_state(opcode)
            success = instruction(self._mmu,self)
            self.debugger.print_cpu_flags()
            self.debugger.end()
            if not success:
                print(f'Opcode failed {hex} at {hex_pc}')
        else:       
            print(f'Unknown opcode {hex} at {hex_pc}')      
        self.pc += 1
        return success
        
