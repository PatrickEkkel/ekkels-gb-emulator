from ..component import Component
from .opcode_dsl_new import NewOpcodeContext
from constants import *

class InterruptHandler(Component):

    VBLANK = 0xFF40
    def __init__(self, mmu, cpu):
        super().__init__(mmu)
        self._mmu = mmu
        self._cpu = cpu
        self.mapping = {IF_REGISTER: 0xFF00, IE_REGISTER: 0xFFE1}
    def _format_hex(self, opcode):
        return ("0x{:x}".format(opcode))

    def _handle_vblank_interrupt(self, vector):
        # reset interrupt flag 
        self._mmu.write(IF_REGISTER,0x1F00)
        # build context so we can use the cpu core to construct a jump
        context = NewOpcodeContext(self._cpu, self._mmu,None)
        r1 = r_PC

        # set the interrupt vector
        context.load_rd16(r1).inc().push_d16().load_v16(vector).store_rd16(r1)
        
    def step(self):
        # 
        IM = ((0xFF00 | self.mapping[IF_REGISTER]) & self.mapping[IE_REGISTER]) 
        if IM == InterruptHandler.VBLANK:
            #input('vblank interrupt triggered')
            self._handle_vblank_interrupt(0x40)
            
        
    def read(self, address):
        return self.mapping[address]

    def write(self, address, value):
        self.mapping[address] = value
        
        
    def is_in_range(self, address):
        return IF_REGISTER == address or IE_REGISTER == address
