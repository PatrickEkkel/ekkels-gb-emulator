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
    def read_u16(self,address):
        return int.from_bytes(self._getbyte(address) + self._getbyte(address + 1), 'little')
        

class Registers:

    def __init__(self):
        self.sA(0x00)
        self.sB(0x00)
        self.sC(0x00)
        self.sD(0x00)
        self.sE(0x00)
        self.sF(0x00)
        self.sH(0x00)
        self.sL(0x00)
    
    def sA(self, value):
        self.a = value

    def sB(self, value):
        self.b = value

    def sC(self, value):
        self.c = value

    def sD(self, value):
        self.d = value

    def sE(self, value):
        self.e = value
    
    def sF(self, value):
        self.f = value
    
    def sH(self, value):
        self.h = value
    
    def sL(self, value):
        self.l = value

    def gA(self):
        return self.a

    def gB(self):
        return self.b
    
    def gC(self):
        return self.c

    def gD(self):
        return self.d

    def gE(self):
        return self.e
    
    def gF(self):
        return self.f
    
    def gH(self):
        return self.h

    def gL(self):
        return self.l

class CPU:
    def __init__(self, mmu):
        self.pc = 0x00
        self._sp = 0x00
        self._mmu = mmu
        self.debug_opcode = True
        self.reg = Registers()
        self.opcodes = [None] * 255
        self.opcodes[0x31] = opcodes.LD16d
        
    def _read_pc_opcode(self):
        return self._mmu.read(self.pc)
    
    def debug(self, opcode):
        return ("0x{:x}".format(opcode))

    def set_sp(self, sp):
        self._sp = sp
        
    def step(self):
       
        opcode = self._read_pc_opcode()
        hex =  self.debug(opcode)
        if self.debug_opcode:
            print(f'CPU: {hex}')
        
        try:
            self.opcodes[opcode](self._mmu,self)
        except Exception as e:
            print(e)
            print(f'Unknown opcode {hex}')
               
                
        self.pc += 1
        
