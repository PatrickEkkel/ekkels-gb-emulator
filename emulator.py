import struct
import opcodes
from array import array



class MMU: 

    def __init__(self):
        pass
        #self.memory = array('B')
    
    def set_bios(self, bios):
        self.bios = bios

    def read(self, address):
        return self.bios.data[address]
        # pass in the bios
    def _getbyte(self,address):
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


    def print_state(self, data):
        pc = self.cpu.pc
        hex = self.print_hex(data)
        if self.cpu.debug_opcode:
            print(f'PC: {pc} CPU: {hex}')


class Registers:

    def __init__(self):
        self.SET_A(0x00)
        self.SET_B(0x00)
        self.SET_C(0x00)
        self.SET_D(0x00)
        self.SET_E(0x00)
        self.SET_F(0x00)
        self.SET_H(0x00)
        self.SET_L(0x00)
        self.ZERO = False
    
    def SET_ZERO_FLAG(self, value):
        self.ZERO = True

    def SET_A(self, value):
        self.a = value

    def SET_B(self, value):
        self.b = value

    def SET_C(self, value):
        self.c = value

    def SET_D(self, value):
        self.d = value

    def SET_E(self, value):
        self.e = value
    
    def SET_F(self, value):
        self.f = value
    
    def SET_H(self, value):
        self.h = value
    
    def SET_L(self, value):
        self.l = value

    def GET_A(self):
        return self.a

    def GET_B(self):
        return self.b
    
    def GET_C(self):
        return self.c

    def GET_D(self):
        return self.d

    def GET_E(self):
        return self.e
    
    def GET_F(self):
        return self.f
    
    def GET_H(self):
        return self.h

    def GET_L(self):
        return self.l

class CPU:
    def __init__(self, mmu):
        self.pc = 0x00
        self._sp = 0x00
        self._mmu = mmu
        self.debug_opcode = True
        self.reg = Registers()
        self.debugger = Debugger(self)
        self.opcodes = [None] * 255
        self.opcodes[0x31] = opcodes.LDSP16d
        self.opcodes[0xAF] = opcodes.XORA
        self.opcodes[0x21] = opcodes.LDHL16d
        
    def _read_pc_opcode(self):
        return self._mmu.read(self.pc)
    
   
    def set_sp(self, sp):
        self._sp = sp
        
    def step(self):
        success = False
        opcode = self._read_pc_opcode()
        self.debugger.print_state(opcode)
        try:
            instruction = self.opcodes[opcode]
            if instruction:
                instruction(self._mmu,self)
                success = True
            else:
                hex = self.debugger.print_hex(opcode)
                print(f'Unknown opcode {hex} at {self.pc}')
                
        except Exception as e:
            print(e)            
        self.pc += 1
        return success
        
