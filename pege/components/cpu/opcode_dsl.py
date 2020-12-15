
class Opcode:
    def __init__(self, meta, address=None):
        self.mnemonic = meta['m']
        self.address = address
        self.cycles = meta['cycles']
        self.jump_instruction = meta['jump_instruction']


    def _format_hex(self, opcode):
        return ("0x{:x}".format(opcode))

    def get_cycles(self,jump=False):
        if self.jump_instruction:
            if jump:
                return self.cycles[1]
            else:
                return self.cycles[0]
        else:
            return self.cycles


    def __str__(self):
        if self.address:
            address = self._format_hex(self.address)
            return f'{self.mnemonic} {address}'
        else:
            return f'{self.mnemonic}'


class OpcodeState:

    def __init__(self, cpu):
        self._cpu = cpu
        self.selected_register_key = None
        self.selected_register_value = None
        self.selected_address_key = None
        self.selected_address_value = None

    def storereg(self, register, value):
        if register == 'HL':
            self._cpu.reg.SET_HL(value)
        elif register == 'A':
            self._cpu.reg.SET_A(value)
        else:
            input('not implemented')

    def loadreg(self, register):
        if register == 'HL':
            return self._cpu.reg.GET_HL()
        elif register == 'A':
            return self._cpu.reg.GET_A()
        else:
            input('not implemented')
    
    # retrieve the value from the selected_register_key and put it in the buffer
    def load_register_value(self):
        if self.selected_register_key:
            register = self.selected_register_key
        self.selected_register_value = self.loadreg(register)
        return self


        
class OpcodeContext:

    def __init__(self, cpu, mmu, meta):
        self._mmu = mmu
        self._cpu = cpu
        self._meta = meta
        self.opcode_state = OpcodeState(cpu)
        self.opcode = Opcode(self._meta)

    
    def select_reg(self, register):
        self.opcode_state.selected_register_key = register
        return self

    # increment the current selected value by one
    def increg(self,register=None):
        self.opcode_state.selected_register_value += 1
        return self
    # write the current contents of the register value buffer to the selected register
    def storereg(self):
        self.opcode_state.storereg(self.opcode_state.selected_register_key, self.opcode_state.selected_register_value)
        return self
    # write the value of the passed regsiter (reg) in the buffer to the memory address that is stored in the selected register
    def storereg_to_addr(self, reg=None):
        value = self.opcode_state.loadreg(reg)
        self._mmu.write(self.opcode_state.selected_register_value, value)
        return self
    
    # write the current address value that is stored in the buffer to (reg)
    def storeaddr_to_reg(self,reg=None):
        value = self.opcode_state.selected_address_value
        self.opcode_state.storereg(reg,value)
        return self
    
    # load the value from the memory address that is currently in the loaded register value buffer
    def loadaddr_from_reg(self):
        self.opcode_state.selected_address_key = self.opcode_state.selected_register_value
        self.opcode_state.selected_address_value = self._mmu.read(self.opcode_state.selected_register_value)
        return self

    def loadval_from_reg(self):
        self.opcode_state.load_register_value()
        return self
  
    # read the current position of the program counter as an address value for the current selected register
    def loadaddr_from_opcode(self):
        self._cpu.pc += 1
        self.opcode_state.selected_address_key = self._cpu.pc
        self.opcode_state.selected_address_value = self._mmu.read(self._cpu.pc)
        return self

  