import struct
import opcodes
from array import array



class MMU: 
    VRAM_START = 0x8000
    VRAM_END = 0x9FFF
    def __init__(self):
        self.bootrom_loaded = False
        self.data = array('B')
        self.bios = array('B')
        self.vram = self.init_memory(MMU.VRAM_START,MMU.VRAM_END)


    def init_memory(self, start,end):
        size = end - start
        result = [0x0000] * (end + 1) 
        return result

    def print_hex(self, opcode):
        return ("0x{:x}".format(opcode))


    def disable_bootrom(self):
        self.bootrom_loaded = True

    def set_rom(self, rom):
        self.data = rom

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
    def _is_vram(self, address):
        return address >= 0x8000 and address <= 0x9FFF

    def read(self, address):
        local_data = None
        if self.bootrom_loaded:
            local_data = self.data
        else:
            local_data = self.bios.data
        
        # is the address within vram?  
        if self._is_vram(address):
            return self.vram[address]
        else:
            return local_data[address]

  
    def _getbyte(self,address):
        if self.bootrom_loaded:
            return struct.pack('B', self.data[address])
        else:
            return struct.pack('B', self.bios.data[address])
    
    def read_u8(self,address):
        return _getbyte(address)

    def read_u16(self,address):
        return int.from_bytes(self._getbyte(address) + self._getbyte(address + 1), 'little')
        

class Debugger:

    def __init__(self, cpu):
        self.cpu = cpu
    
    def print_hex(self, opcode):
        return ("0x{:x}".format(opcode))

    def print_opcode(self, opcode_description):
        if self.cpu.debug_opcode:
            print(opcode_description)

    def print_register(self, name, value, size):
        if self.cpu.debug_opcode:
            hex = self.print_hex(value)
            print(f'REG: {name} val: {hex} size: {size}')


    def print_state(self, data):
        pc = self.cpu.pc
        hex = self.print_hex(data)
        if self.cpu.debug_opcode:
            print(f'PC: {pc} CPU: {hex}',end=' ')


class Registers:

    def __init__(self):
        self.SET_AF(0x00)
        self.SET_B(0x00)
        self.SET_C(0x00)
        self.SET_D(0x00)
        self.SET_E(0x00)
        self.SET_HL(0x0000)
        self.SET_SP(0x0000)
        self.ZERO = False
    
    def SET_ZERO_FLAG(self, value):
        self.ZERO = True

    def SET_AF(self, af):
        self.af = af

    def SET_B(self, value):
        self.b = value

    def SET_C(self, value):
        self.c = value

    def SET_D(self, value):
        self.d = value

    def SET_E(self, value):
        self.e = value
    
    def SET_HL(self, value):
        self.hl = value
    
    def SET_SP(self, value):
        self.sp = value

    def GET_A(self):
        return MMU.get_high_byte(self.af)

    def GET_AF(self):
        return self.af

    def GET_B(self):
        return self.b
    
    def GET_C(self):
        return self.c

    def GET_D(self):
        return self.d

    def GET_E(self):
        return self.e
    
    def GET_HL(self):
        return self.hl
    
    def GET_SP(self):
        return self.sp

class CPU:
    def __init__(self, mmu):
        self.pc = 0x00
        self._mmu = mmu
        self.debug_opcode = True
        self.reg = Registers()
        self.debugger = Debugger(self)
        self.opcodes = [None] * 255
        self.cb_opcodes = [None] * 255
        self.opcodes[0x31] = opcodes.LDSP16d
        self.opcodes[0xAF] = opcodes.XORA
        self.opcodes[0x21] = opcodes.LDHL16d
        self.opcodes[0x32] = opcodes.LDHL8A
        self.cb_opcodes[0xcb] = opcodes.CB
        self.cb_opcodes[0x7c] = opcodes.BIT7H
        
    def _read_pc_opcode(self):
        return self._mmu.read(self.pc)
        
    def step(self):
        success = False
        opcode = self._read_pc_opcode()
        
        hex = self.debugger.print_hex(opcode)
        try:
            if opcode == 0xcb:
                instruction = self.cb_opcodes[opcode]
            else:    
                instruction = self.opcodes[opcode]
            if instruction:
                self.debugger.print_state(opcode)
                success = instruction(self._mmu,self)
                if not success:
                    print(f'Opcode failed {hex} at {self.pc}')
            else:
                
                print(f'Unknown opcode {hex} at {self.pc}')
                
        except Exception as e:
            print(e)            
        self.pc += 1
        return success
        
