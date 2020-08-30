import struct
import opcodes
from array import array

class Stack:

    def __init__(self, cpu, mmu):
        self.mmu = mmu
        self.cpu = cpu
    
    def push(self, value):
        sp = self.cpu.reg.GET_SP()
        self.mmu.write(sp, value)
        sp -= 1
        self.cpu.reg.SET_SP(sp)
        #self.mmu.write()
class MMU: 
    VRAM_START = 0x8000
    VRAM_END = 0x9FFF

    HRAM_START = 0xFF80
    HRAM_END = 0xFFFE

    BOOTROM_START = 0x0000
    BOOTROM_END = 0x00FF
    CARTRIDGE_ROM_START = 0x0100


    def __init__(self):
        self.bootrom_loaded = False
        self.rom = None
        self.bios = array('B')
        self.vram = self.init_memory(MMU.VRAM_START, MMU.VRAM_END)
        self.hram = self.init_memory(MMU.HRAM_START, MMU.HRAM_END)


    def init_memory(self, start,end):
        size = end - start
        result = [0x0000] * (end + 1) 
        return result

    def print_hex(self, opcode):
        return ("0x{:x}".format(opcode))


    def disable_bootrom(self):
        self.bootrom_loaded = True

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
        if self._is_io(address):
            # do nothing with I/O until it is needed
            pass
        if self._is_hram(address):
            self.hram[address] = value
            
    def _is_vram(self, address):
        return address >= MMU.VRAM_START and address <= MMU.VRAM_END

    def _is_io(self, address):
        return address >= 0xFF00 and address <= 0xFF7F

    def _is_hram(self, address):
        return address >= MMU.HRAM_START and address <= MMU.HRAM_END

    def read(self, address):
        local_data = None
        
        # determine if we are above 0x00FF, 
        # this implies that we are not trying to read addresses from the bootrom
        # everything above 0x104 to 7FFF is 'cartrdige ROM' space, switchable via MBC if available 

        if address > MMU.BOOTROM_END:
            if self.rom:
                return self.rom.read(address)
            else:
                # No cartridge loaded, return 0x000
                return 0x0000

        if self.bootrom_loaded:
            local_data = self.data
        else:
            local_data = self.bios.data
        

        # is the address within vram?  
        if self._is_vram(address):
            print('gotta read that vram bitch')
            return self.vram[address]
        elif self._is_io(address):
            return 0x0000
        else:
            return local_data[address]

  
    def _getbyte(self,address, signed=False):
        pack_method = 'B'
        if signed:
            pack_method = 'b'

        if self.bootrom_loaded:
            return struct.pack(pack_method, self.data[address])
        else:
            return struct.pack(pack_method, self.bios.data[address])
    
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
        self.SET_B(0x00)
        self.SET_C(0x00)
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

    def SET_AF(self, af):
        self.af = af

    def SET_B(self, value):
        self.b = value

    def SET_C(self, value):
        self.c = value

    def SET_DE(self, value):
        self.de = value

    #def SET_D(self, value):
    #    self.d = value

    #def SET_E(self, value):
    #    self.e = value
    
    def SET_HL(self, value):
        self.hl = value
    

    def GET_A(self):
        return MMU.get_high_byte(self.af)
    
    def GET_F(self):
        return MMU.get_low_byte(self.af)

    def SET_A(self, value):
        F = MMU.get_low_byte(self.af)
        A = value
        A = A << 8
        self.af = F | A

    def SET_F(self, value):
        F = value
        A = MMU.get_high_byte(self.af)
        self.af = F | A

    def GET_AF(self):
        return self.af

    def GET_B(self):
        return self.b
    
    def GET_C(self):
        return self.c

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
        self.opcodes[0x21] = opcodes.LDnn16d
        self.opcodes[0x11] = opcodes.LDnn16d
        self.opcodes[0x32] = opcodes.LDDHL8A
        self.opcodes[0x20] = opcodes.JRNZN
        self.opcodes[0x4f] = opcodes.LDnA
        self.opcodes[0x0E] = opcodes.LDn8d
        self.opcodes[0x3E] = opcodes.LDn8d
        self.opcodes[0xE2] = opcodes.LDCA
        self.opcodes[0xC] = opcodes.INCn
        self.opcodes[0x77] = opcodes.LDHL8A
        self.opcodes[0xE0] = opcodes.LDHnA
        self.opcodes[0x1A] = opcodes.LDAn
        self.opcodes[0xCD] = opcodes.CALLnn

        self.cb_opcodes[0xcb] = opcodes.CB
        self.cb_opcodes[0x7c] = opcodes.BIT7H

    
    def read_opcode(self):
        return self._mmu.read(self.pc)
    
    def read_opcode_parameter(self):
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
        
