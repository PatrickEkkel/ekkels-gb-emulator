

class OpcodeContext:

    def __init__(self, cpu, mmu, meta, pc):
        self._mmu = mmu
        self._cpu = cpu
        self._meta = meta
        self._operands = [None, None]
        self._pointer = 0
        self._pc = pc
        self._selected_register = None

    # read the next opcode as register
    def readreg(self):
        opcode = self._mmu.read(self._pc)
        self._pc += 1
        opcodes = self._meta['register_options']
        for k, v in opcodes.items():
            if v == opcode:
                self._store_operand(k)
                return self

        return self

    def store(self,value=None):
        if self._selected_register == 'HL':
            value = self._load_operand()
            self._cpu.reg.SET_HL(value)
        else:
            input('not implemented')
        return self

    def selectreg(self,reg=None):
        if reg == None:
            self._selected_register = self._load_operand()
        return self


    def readval(self):
        value = self._mmu.read(self._pc)
        self._store_operand(value)
        return self

    def _load_operand(self):
         result = self._operands[self._pointer]
         if self._pointer == 1:
             self._pointer = 0
         else:
             self._pointer += 1

         return result

    def _store_operand(self, value):
        self._operands[self._pointer] = value
        if  self._pointer == 1:
            self._pointer = 0
        else:
            self._pointer += 1
