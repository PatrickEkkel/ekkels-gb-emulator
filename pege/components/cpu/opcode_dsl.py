from ..mmu import MMU
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
        self.addressing_mode = AddressingMode.IMPLIED
        self.transient_value = None

        self.left_operand = None
        self.right_operand = None

    def storereg(self, register, value):
        if register == 'HL':
            self._cpu.reg.SET_HL(value)
        elif register == 'PC':
            self._cpu.pc = value 
        elif register == 'BC':
            self._cpu.reg.SET_BC(value)
        elif register == 'A':
            self._cpu.reg.SET_A(value)
        elif register == 'B':
            self._cpu.reg.SET_B(value)
        elif register == 'C':
            self._cpu.reg.SET_C(value)
        elif register == 'E':
            self._cpu.reg.SET_E(value)
        elif register == 'D':
            self._cpu.reg.SET_D(value)
        elif register == 'H':
            self._cpu.reg.SET_H(value)
        elif register == 'L':
            self._cpu.reg.SET_L(value)
        elif register == 'F':
            self._cpu.reg.SET_F(value)
        else:
            print('store reg')
            input('not implemented')

    def loadreg(self, register):
        if register == 'HL':
            return self._cpu.reg.GET_HL()
        elif register == 'PC':
            return self._cpu.pc
        elif register == 'A':
            return self._cpu.reg.GET_A()
        elif register == 'B':
            return self._cpu.reg.GET_B()
        elif register == 'C':
            return self._cpu.reg.GET_C()
        elif register == 'D':
            return self._cpu.reg.GET_D()
        elif register == 'E':
            return self._cpu.reg.GET_E()
        elif register == 'F':
            return self._cpu.reg.GET_F()
        elif register == 'H':
            return self._cpu.reg.GET_H()
        elif register == 'L':
            return self._cpu.reg.GET_L()
        elif register == 'BC':
            return self._cpu.reg.GET_BC()
        elif register == 'DE':
            return self._cpu.reg.GET_DE()
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
    # CPL is short for complement register, which is a bitwise NOT
    CPL = 4
    NOT = 4
    SHIFT_RIGHT = 5
    SHIFT_LEFT = 6
    
class AddressingMode:
    # means 8 bit unsigned data, which are added to $FF00 in certain instructions
    a8 = 8
    # 16 bit addressing mode
    a16 = 15
    i8 = 9
    # Direct 8 bit adressing mode pc+1
    d8 = 10
    # Indirect 16 bit register adressing mode, read 16 value from register and use it as pointer to loaded value
    ir16 = 11
    # direct read 16 register, put the address in the register without dereferencing
    dr16 = 12


    IMPLIED = 13

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

    # write the value of the passed register (reg) in the buffer to the offset FF00 + n(where n is the value loaded via selected_address_value)
    def _storereg_to_addr_offset(self, reg):
        value = self.opcode_state.loadreg(reg)    
        address = 0xFF00 + self.opcode_state.selected_address_value
        self._mmu.write(address, value)

    # write to loaded register values memory addres and write the value that is read from memory 
    def _store_addr_from_opcode_to_addr(self, reg=None):
        value = self.opcode_state.selected_address_value
        address = self.opcode_state.selected_register_value
        self._mmu.write(address, value)
        return self
        
    # write the current address value that is stored in the buffer to (reg)
    def _storeaddr_to_reg(self,reg=None):
        value = self.opcode_state.selected_address_value
        if self.opcode_state.addressing_mode == AddressingMode.a16:
            value = MMU.get_high_byte(value)
        
        self.opcode_state.storereg(reg, value)
        return self


    # load the value from the memory address that is currently in the loaded register value buffer
    def _loadaddr_from_reg(self):
        self.opcode_state.selected_address_key = self.opcode_state.selected_register_value
        self.opcode_state.selected_address_value = self._mmu.read(self.opcode_state.selected_register_value)
        return self

    # load the address value based on the address that is loaded in address value
    def _loadaddr_value_to_reg(self):
        self.opcode_state.selected_address_value = self._mmu.read(self.opcode_state.selected_address_value)
        self._storeaddr_to_reg(self._get_selected_reg())
        
    def _loadval_from_reg(self):
        self.opcode_state.load_register_value()
        return self

    # read the current position of the program counter as an address value for the current selected register
    def _loadaddr_from_opcode(self, offset=None):
        if self.opcode_state.addressing_mode == AddressingMode.d8:
            self._cpu.pc += 1   
            self.opcode_state.selected_address_key = self._cpu.pc
            self.opcode_state.selected_address_value = self._mmu.read(self._cpu.pc)
        elif self.opcode_state.addressing_mode == AddressingMode.a16:
            self._cpu.pc += 1   
            self.opcode_state.selected_address_key = self._cpu.pc
            self.opcode_state.selected_address_value = self._mmu.read_u16(self._cpu.pc)
            self._cpu.pc += 1
        return self
    # read the current opf the program counter as an address value for currect selected register with offset FF00
    #def _loadaddr_from_opcode_FF00(self):
    #    _loadaddr_from_opcode()

    def _set_adressingmode(self, addressing_mode):
        self.opcode_state.addressing_mode = addressing_mode
        return self

    def _select_reg(self, register):
        self.opcode_state.selected_register_key = register
        return self

    def _get_selected_reg(self):
        return self.opcode_state.selected_register_key
        
    def _get_select_reg_value(self):
        if self.opcode_state.addressing_mode == AddressingMode.d8:
            return self.opcode_state.selected_address_value
        elif self.opcode_state.addressing_mode == AddressingMode.IMPLIED:
            return self.opcode_state.selected_register_value

    def _set_reg_value(self, value):
        self.opcode_state.selected_register_value = value

    def _check_carry(self):
        value_a = self.opcode_state.left_operand
        value_b = self.opcode_state.right_operand

        carry = (value_a & 0x80) and (value_b & 0x80)

        if carry:
            self._cpu.reg.SET_CARRY()
        else:
            self._cpu.reg.CLEAR_CARRY()
    def _check_substract(self):
        pass

    def _check_half_carry(self):
        value_a = self.opcode_state.left_operand
        value_b = self.opcode_state.right_operand
        half_carry = ((value_a & 0xF) + (value_b & 0xf)) & 0x10
        if half_carry:
            self._cpu.reg.SET_HALF_CARRY()
        else:
            self._cpu.reg.CLEAR_HALF_CARRY()

    def _check_zero(self):
        value = self._get_select_reg_value()
        if value == 0x00:
            self._cpu.reg.SET_ZERO()
        else:
            self._cpu.reg.CLEAR_ZERO()

    def _set_operands(self, left,right):
        self.opcode_state.left_operand = left
        self.opcode_state.right_operand = right

    def bitwise(self, register=None, operation=None, position=0, value=None,transient_load=False):
        if not transient_load:
            value_a =  self._get_select_reg_value()
            if register:
                self._select_reg(register)._loadval_from_reg()
        else:
            value_a = self.opcode_state.transient_value

        if value is not None:
                value_b = value
        else:
            if register:
                self._select_reg(register)._loadval_from_reg()
                value_b = self._get_select_reg_value()
            
        if operation == BitwiseOperators.OR:
            value_b = self._get_select_reg_value()
            self._set_reg_value(value_a | value_b)
        elif operation == BitwiseOperators.AND:
            self._set_reg_value(value_a & value_b)
            self._set_operands(value_a, value_b)
        elif operation == BitwiseOperators.CPL:
            value = self._get_select_reg_value()
            self._set_reg_value(value ^ 0xFF)
        elif operation == BitwiseOperators.XOR:
            self._set_reg_value(value_a ^ value_b)
            self._set_operands(value_a, value_b)
        elif operation == BitwiseOperators.SHIFT_LEFT:
            self._set_reg_value(value_a << position)
        elif operation == BitwiseOperators.SHIFT_RIGHT:
            self._set_reg_value(value_a >> position)
        elif operation == BitwiseOperators.NOT:
            self._set_reg_value(~value_a)
        
        else:
            print('bitwise')
            input('not implemented')

        self._set_adressingmode(AddressingMode.IMPLIED)
        return self
    
    def add(self, register=None):
        value_a = self._get_select_reg_value()
        self._select_reg(register)._loadval_from_reg()
        value_b = self._get_select_reg_value()
        self._set_reg_value(value_a + value_b)
        self._set_operands(value_a, value_b)
        return self

    def sub(self, register=None):
        value_a = self._get_select_reg_value()
        self._select_reg(register)._loadval_from_reg()
        value_b = self._get_select_reg_value()
        self._set_reg_value(value_a - value_b)
        self._set_operands(value_a, value_b)
        return self

    def dec(self, register=None):
        if register == None:
            register = self._get_selected_reg()
        
        value_a = self._get_select_reg_value()
        self._select_reg(register)._decreg()
        value_b = self._get_select_reg_value()
        self._set_operands(value_a,value_b)

        return self

    def flags(self, zero, substract, halfcarry, carry):
        I = '-'
        E = 0
        S = 1
        Z = 2
        N = 3
        H = 4
        C = 5

        if zero == Z:
            self._check_zero()
        elif zero == S:
            self._cpu.reg.SET_ZERO()
        elif zero == E:
            self._cpu.reg.CLEAR_ZERO()

        if substract == N:
            self._check_substract()
        elif substract == S:
            self._cpu.reg.SET_SUBSTRACT()
        elif substract == E:
            self._cpu.reg.CLEAR_SUBSTRACT()

        if halfcarry == H:
            self._check_half_carry()
        elif halfcarry == S:
            self._cpu.reg.SET_HALF_CARRY()
        elif halfcarry == E:
            self._cpu.reg.CLEAR_HALF_CARRY()

        if carry == C:
            self._check_carry()
        elif carry == S:
            self._cpu.reg.SET_CARRY()
        elif carry == E:
            self._cpu.reg.CLEAR_CARRY()

        return self


    def inc(self, register=None):
        if register == None:
            register = self._get_selected_reg()
        value_a = self._get_select_reg_value()
        self._select_reg(register)._increg()
        value_b = self._get_select_reg_value()
        self._set_operands(value_a, value_b)
        return self

    def transient_load(self):
        value_a =  self.opcode_state.transient_value
        self._set_reg_value(value)
        return self

    def transient_store(self, value=None):
        if value:
            self.opcode_state.transient_value = value
        else:
            value_a = self._get_select_reg_value()
            self.opcode_state.transient_value = value_a
        return self

    def load(self, register=None, addressing_mode=AddressingMode.IMPLIED, transient_store=False):
        self._set_adressingmode(addressing_mode)
        if addressing_mode == AddressingMode.d8:
            context = self._loadaddr_from_opcode()
        elif addressing_mode == AddressingMode.a16:
            context = self._select_reg(register)._loadaddr_from_opcode()._loadaddr_value_to_reg()
        elif addressing_mode == AddressingMode.ir16:
            context = self._select_reg(register)._loadval_from_reg()._loadaddr_from_reg()
        elif addressing_mode == AddressingMode.IMPLIED:
            context = self._select_reg(register)._loadval_from_reg()

        if transient_store:
            return self.transient_store()
        return self
        
    def reset(self, position):
        value_a = self._get_select_reg_value()
        value_a = value_a & ~(1 << position)
        self._set_reg_value(value_a)
        return self

    def set(self, address):
        self._set_reg_value(address)
        return self

    def push(self):
        if len(self._get_selected_reg()) == 2:
            self._cpu.stack.push_u16bit(self._get_select_reg_value())    
        else:
            self._cpu.stack.push(self._get_select_reg_value())
        return self

    def pop(self):
        self._set_reg_value(self._cpu.stack.pop())
        return self
    
    def store(self, register=None, addressing_mode=None,transient_store=False, value=None):
        
        if addressing_mode != None:
            self._set_adressingmode(addressing_mode)

        if transient_store:
            if value:
                self.transient_store(value)
            else:
                value_a = self._get_select_reg_value()
                self.transient_store(value_a)
        else:
            if register == None:
                register = self._get_selected_reg()
            if self.opcode_state.addressing_mode == AddressingMode.IMPLIED:
                self._select_reg(register)._storereg()
            elif self.opcode_state.addressing_mode == AddressingMode.i8:
                self._select_reg(register)._store_addr_from_opcode_to_addr(register)
            elif self.opcode_state.addressing_mode == AddressingMode.d8:
                self._select_reg(register)._storeaddr_to_reg(register)
            elif self.opcode_state.addressing_mode == AddressingMode.ir16:
                self._select_reg(register)._storeaddr_to_reg(register)
            elif self.opcode_state.addressing_mode == AddressingMode.a16:
                self._select_reg(register)._storeaddr_to_reg(register)
            elif self.opcode_state.addressing_mode == AddressingMode.dr16:
                self._select_reg(register)._storereg_to_addr(register)
            elif self.opcode_state.addressing_mode == AddressingMode.a8:
                self._storereg_to_addr_offset(register)

        return self
