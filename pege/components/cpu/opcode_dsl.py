

class OpcodeContext:

    def __init__(self, cpu, mmu, meta):
        self._mmu = mmu
        self._cpu = cpu
        self._meta = meta
        self._operands = [None, None]
        self._pointer = 0
        self._pc = cpu.pc
        self._selected_register = None
        self._selected_address_value = None
        self._selected_reg_value = None

    def set_selected_register(self, register):
        self._selected_register = register
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
        value = self._load_operand()
        self._storereg(self._selected_register, value)
        return self

    def increg(self,register=None):
        self._selected_reg_value += 1
        return self

    def storereg_to_addr(self, reg=None):
        value = self._loadreg(reg)
        print(self._cpu.debugger.format_hex(value))
        self._mmu.write(self._selected_reg_value, value)
        return self
    def storeaddr_to_reg(self, reg=None):
        if reg is None and self._selected_register:
            register = self._selected_register
        else:
            register = reg
        self._storereg(register, self._selected_reg_value)
        return self

    def loadaddr(self):
        self._selected_address_value = self._mmu.read(self._selected_reg_value)
        return self
    def loadval_from_reg(self):
        #value = self._load_operand()
        if self._selected_register:
            register = self._selected_register
        self._selected_reg_value = self._loadreg(register)
        return self

    def _storereg(self, register, value):
        if register == 'HL':
            self._cpu.reg.SET_HL(value)
        elif register == 'A':
            print(self._cpu.debugger.format_hex(value))
            self._cpu.reg.SET_A(value)
        else:
            input('not implemented')

    def _loadreg(self, register):
        if register == 'HL':
            return self._cpu.reg.GET_HL()
        elif register == 'A':
            return self._cpu.reg.GET_A()
        else:
            input('not implemented')

    def selectreg(self,reg=None):
        if reg == None:
            self._selected_register = self._load_operand()
        else:
            self._store_operand(reg)
            self._selected_register = reg
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
