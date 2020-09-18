import struct
import opcodes
from array import array

class Stack:

    def __init__(self, cpu, mmu):
        self.mmu = mmu
        self.cpu = cpu
    

    def push_u16bit(self, value):
        lowbyte = MMU.get_high_byte(value)
        highbyte = MMU.get_low_byte(value)
        self.push(lowbyte)
        self.push(highbyte)

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
        self.step_instruction = True
        self.stop_at = 0x21b
        self.stop_at_opcode = None
    
    def format_hex(self, opcode):
        return ("0x{:x}".format(opcode))

    def print_opcode(self, opcode_description):
        if self.cpu.debug_opcode:
            print(opcode_description, end=' ')

    def print_register(self):
        if self.show_registers:
            AF = self.format_hex(self.cpu.reg.GET_AF())
            BC = self.format_hex(self.cpu.reg.GET_BC())
            DE = self.format_hex(self.cpu.reg.GET_DE())
            HL = self.format_hex(self.cpu.reg.GET_HL())
            print(f'AF: {AF}')
            print(f'BC: {BC}')
            print(f'DE: {DE}')
            print(f'HL: {HL}')
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

    def debug(self, pc, opcode):
        if self.step_instruction or self.stop_at == pc:
            input('press enter to continue')
            self.print_register()
        if self.stop_at_opcode == opcode:
            input('press enter to continue')

        return 


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

    def _write_register(self,value):
        if value < 0x00:
            return 0xff
        else:
            return value
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
        self.B = self._write_register(value)

    def SET_C(self, value):
        self.C = self._write_register(value)
    
    def SET_D(self, value):
        self.D = self._write_register(value)
    
    def SET_E(self, value):
        self.E = self._write_register(value)

    def SET_DE(self, value):
        self.D = MMU.get_high_byte(value)
        self.E = MMU.get_low_byte(value)
        self.DE = value

    def SET_HL(self, value):
        self.H = MMU.get_high_byte(value)
        self.L = MMU.get_low_byte(value)
        self.HL = value
    

    def GET_A(self):
        return self.A
    
    def GET_F(self):
        return self.F

    def SET_A(self, value):
        self.A = self._write_register(value)
       
    def SET_F(self, value):
        self.F = self._write_register(value)

    def SET_L(self, value):
        self.L = self._write_register(value)

    def SET_H(self, value):
        self.H = self._write_register(value)

    def GET_AF(self):
        return (self.GET_A() << 8) | self.GET_F()

    def GET_B(self):
        return self.B
        
    def GET_C(self):
        return self.C

    def SET_BC(self, value):
        self.B = MMU.get_high_byte(value)
        self.C = MMU.get_low_byte(value)
        self.BC = value

    def GET_BC(self):
        return (self.GET_B() << 8) | self.GET_C()

    def GET_DE(self):
        return (self.GET_D() << 8) | self.GET_E()


    def GET_D(self):
        return self.D

    def GET_E(self):
        return self.E
    
    def GET_H(self):
        return self.H
    
    def GET_L(self):
        return self.L

    def GET_HL(self):
        return (self.GET_H() << 8) | self.GET_L()
        #return self.hl

    def initialize_without_bootrom(self):
        self.SET_BC(0x0013)
        self.SET_AF(0x01B0)
        self.SET_DE(0x00D8)
        self.SET_HL(0x014D)
        self.SET_SP(0xFFFE)
    
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
        self.opcodes[0x00] = opcodes.NOP
        self.opcodes[0x31] = opcodes.LDSP16d
        self.opcodes[0xAF] = opcodes.XORn
        self.opcodes[0xC5] = opcodes.PUSHBC
        self.opcodes[0x21] = opcodes.LDnn16d
        self.opcodes[0x11] = opcodes.LDnn16d
        self.opcodes[0x32] = opcodes.LDDHL8A
        self.opcodes[0x22] = opcodes.LDDHL8A
        self.opcodes[0x20] = opcodes.JRNZn
        self.opcodes[0x28] = opcodes.JRZn
        self.opcodes[0xc3] = opcodes.JPnn
        self.opcodes[0x18] = opcodes.JRn
        self.opcodes[0x4f] = opcodes.LDnA
        self.opcodes[0x67] = opcodes.LDnA
        self.opcodes[0x57] = opcodes.LDnA
        self.opcodes[0x7b] = opcodes.LDnn
        self.opcodes[0x0E] = opcodes.LDn8d
        self.opcodes[0x1E] = opcodes.LDn8d
        self.opcodes[0x2E] = opcodes.LDn8d
        self.opcodes[0x06] = opcodes.LDn8d
        self.opcodes[0x3E] = opcodes.LDn8d
        self.opcodes[0xE2] = opcodes.LDCA
        self.opcodes[0x17] = opcodes.RLA
        self.opcodes[0xC] = opcodes.INCn
        self.opcodes[0x04] = opcodes.INCn
        self.opcodes[0x23] = opcodes.INCnn
        self.opcodes[0x13] = opcodes.INCnn
        self.opcodes[0x77] = opcodes.LDHL8A
        self.opcodes[0xE0] = opcodes.LDHnA
        self.opcodes[0xF0] = opcodes.LDHAn
        self.opcodes[0x1A] = opcodes.LDAn
        self.opcodes[0xCD] = opcodes.CALLnn
        self.opcodes[0xC1] = opcodes.POPBC
        self.opcodes[0x05] = opcodes.DECn
        self.opcodes[0x3D] = opcodes.DECn
        self.opcodes[0x0D] = opcodes.DECn
        self.opcodes[0xc9] = opcodes.RET
        self.opcodes[0xFE] = opcodes.CPn
        self.opcodes[0xEA] = opcodes.LDnn16a
        self.cb_opcodes[0xcb] = opcodes.CB
        self.cb_opcodes[0x7c] = opcodes.BIT7H
        self.cb_opcodes[0x11] = opcodes.RLC



    
    def read_opcode(self):
        return self._mmu.read(self.pc)
    
    def read_lower_opcode_parameter(self):
        return self._mmu.read(self.pc) << 4 & 0xFF

    def read_upper_opcode_parameter(self):
        return self._mmu.read(self.pc) >> 4 & 0xFF

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
            self.debugger.debug(self.pc, opcode)
            success = instruction(self._mmu,self)
            self.debugger.print_cpu_flags()
            self.debugger.end()
            if not success:
                print(f'Opcode failed {hex} at {hex_pc}')
        else:       
            print(f'Unknown opcode {hex} at {hex_pc}')      
        self.pc += 1
        return success
        
