
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
        self.adressing_mode = AddressingMode.IMPLIED

    def storereg(self, register, value):
        print(register)
        if register == 'HL':
            self._cpu.reg.SET_HL(value)
        elif register == 'A':
            self._cpu.reg.SET_A(value)
        elif register == 'B':
            self._cpu.reg.SET_B(value)
        elif register == 'C':
            self._cpu.reg.SET_C(value)
        else:
            print('store reg')
            input('not implemented')

    def loadreg(self, register):
        if register == 'HL':
            return self._cpu.reg.GET_HL()
        elif register == 'A':
            return self._cpu.reg.GET_A()
        elif register == 'B':
            return self._cpu.reg.GET_B()
        elif register == 'C':
            return self._cpu.reg.GET_C()
        elif register == 'BC':
            return self._cpu.reg.GET_BC()
        else:
            print('loadreg')
            input('not implemented')

    # retrieve the value from the selected_register_key and put it in the buffer
    def load_register_value(self):
        if self.selected_register_key:
            register = self.selected_register_key
        self.selected_register_value = self.loadreg(register)
        return self

class BitwiseOperators:
    OR = 1
    AND = 2
    XOR = 3

class AddressingMode:
    # Direct 8 bit adressing mode pc+1
    d8 = 10
    # Indirect 16 bit register adressing mode, read 16 value from register and use it as pointer to loaded value
    ir16 = 11
    IMPLIED = 12

class OpcodeContext:



    def __init__(self, cpu, mmu, meta):
        self._mmu = mmu
        self._cpu = cpu
        self._meta = meta
        self.opcode_state = OpcodeState(cpu)
        self.opcode = Opcode(self._meta)



    def _decreg(self, register=None):
        self.opcode_state.selected_register_value -= 1
        return self
    # increment the current selected value by one
    def _increg(self,register=None):
        self.opcode_state.selected_register_value += 1
        return self
    # write the current contents of the register value buffer to the selected register
    def _storereg(self):
        self.opcode_state.storereg(self.opcode_state.selected_register_key, self.opcode_state.selected_register_value)
        return self
    # write the value of the passed regsiter (reg) in the buffer to the memory address that is stored in the selected register
    def _storereg_to_addr(self, reg=None):
        value = self.opcode_state.loadreg(reg)
        self._mmu.write(self.opcode_state.selected_register_value, value)
        return self

    # write the current address value that is stored in the buffer to (reg)
    def _storeaddr_to_reg(self,reg=None):
        value = self.opcode_state.selected_address_value
        self.opcode_state.storereg(reg, value)
        return self

    # load the value from the memory address that is currently in the loaded register value buffer
    def _loadaddr_from_reg(self):
        self.opcode_state.selected_address_key = self.opcode_state.selected_register_value
        self.opcode_state.selected_address_value = self._mmu.read(self.opcode_state.selected_register_value)
        return self

    def _loadval_from_reg(self):
        self.opcode_state.load_register_value()
        return self

    # read the current position of the program counter as an address value for the current selected register
    def _loadaddr_from_opcode(self):
        self._cpu.pc += 1
        self.opcode_state.selected_address_key = self._cpu.pc
        self.opcode_state.selected_address_value = self._mmu.read(self._cpu.pc)
        return self

    def _set_adressingmode(self, addressing_mode):
        self.opcode_state.addressing_mode = addressing_mode
        return self

    def _select_reg(self, register):
        self.opcode_state.selected_register_key = register
        return self

    def _get_selected_reg(self):
        return self.opcode_state.selected_register_key
    def _get_select_reg_value(self):
        return self.opcode_state.selected_register_value
    def _set_reg_value(self, value):
        self.opcode_state.selected_register_value = value

    def _check_zero(self):
        value = self._get_select_reg_value()
        if value == 0x00:
            self._cpu.reg.SET_ZERO()
        else:
            self._cpu.reg.CLEAR_ZERO()

    def bitwise(self, register, operation):
        if operation == BitwiseOperators.OR:
            value_a =  self._get_select_reg_value()
            self._select_reg(register)._loadval_from_reg()
            value_b = self._get_select_reg_value()
            self._set_reg_value(value_a | value_b)
            self._check_zero()
        else:
            print('bitwise')
            input('not implemented')

        return self

    def dec(self, register):
        return self._select_reg(register)._loadval_from_reg()._decreg()

    def inc(self, register=None):
        if register == None:
            register = self._get_selected_reg()

        return self._select_reg(register)._increg()

    def load(self, register=None, addressing_mode=AddressingMode.IMPLIED):
        self._set_adressingmode(addressing_mode)
        if addressing_mode == AddressingMode.d8:
            context = self._loadaddr_from_opcode()
        elif addressing_mode == AddressingMode.ir16:
            context = self._select_reg(register)._loadval_from_reg()._loadaddr_from_reg()
        elif addressing_mode == AddressingMode.IMPLIED:
            context = self._select_reg(register)._loadval_from_reg()

        return context

    def store(self, register=None):
        if register == None:
            register = self._get_selected_reg()
        if self.opcode_state.addressing_mode == AddressingMode.IMPLIED:
            self._select_reg(register)._storereg()
        elif self.opcode_state.addressing_mode == AddressingMode.d8:
            self._select_reg(register)._storeaddr_to_reg(register)
        elif self.opcode_state.addressing_mode == AddressingMode.ir16:
            self._select_reg(register)._storeaddr_to_reg(register)
        return self
