from ..component import Component
from .opcode_dsl import OpcodeContext


class InterruptHandler(Component):

    IF = 0xFF0F
    IE = 0xFFFF

    VBLANK = 0xFF40
    def __init__(self, mmu, cpu):
        super().__init__(mmu)
        self._mmu = mmu
        self._cpu = cpu
        self.mapping = {InterruptHandler.IF: 0xFF00, InterruptHandler.IE: 0xFFFF}
    def _format_hex(self, opcode):
        return ("0x{:x}".format(opcode))

    def _handle_vblank_interrupt(self, vector):
        # reset interrupt flag 
        self._mmu.write(InterruptHandler.IF,0x1F00)
        # build context so we can use the cpu core to construct a jump
        context = OpcodeContext(self._cpu, self._mmu,None)
        r1 = 'PC' 
        # set the interrupt vector
        context.load(r1).inc().push().set(vector).store(r1)
        
    def step(self):
        # 
        IM = (self.mapping[InterruptHandler.IF] & self.mapping[InterruptHandler.IE]) 
        if IM == InterruptHandler.VBLANK:
            input('vblank interrupt triggered')
            self._handle_vblank_interrupt(0x40)
        
    def read(self, address):
        return self.mapping[address]

    def write(self, address, value):
        self.mapping[address] = value
        
        
    def is_in_range(self, address):
        return InterruptHandler.IF == address or InterruptHandler.IE == address
