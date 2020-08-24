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
        
class CPU:
    def __init__(self, mmu):
        self.pc = 0x00
        self.mmu = mmu
        self.debug_opcode = True
        self.opcodes = [None] * 255
        self.opcodes[0xFE] = opcodes.CP
    
    def _read_pc_opcode(self):
        return self.mmu.read(self.pc)
    
    def debug(self, opcode):
        print("0x{:02x}".format(opcode))

    def step(self):
        self.pc += 1
        opcode = self._read_pc_opcode()
        if self.debug_opcode:
            self.debug(opcode)
            self.opcodes[opcode](self)
        #print(str(self.pc))

