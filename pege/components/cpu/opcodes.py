import bitwise_functions
from components.cpu.opcode_dsl import OpcodeContext, BitwiseOperators, AddressingMode, Opcode
from ..mmu import MMU

I = '-'
E = 0
S = 1
Z = 2
N = 3
H = 4
C = 5

def NOP(mmu, cpu, meta, context):
    opcode = Opcode(meta)
    #cpu.debugger.print_opcode(opcode)
    #return opcode.get_cycles()

def DEC_rr(mmu, cpu, meta, context):
    upper_param = cpu.read_upper_opcode_parameter()
    operand_mapping = {0x00: 'BC'}
    r1 = operand_mapping[upper_param]
    context.load(r1).dec().store(r1)



# 0x05,0x3D,0x0D length: 1 byte
# decrements the value of register n by 1
# flags zhn-
def DEC_r(mmu, cpu, meta, context):
    result = False
    upper_param = cpu.read_upper_opcode_parameter()
    lower_param = cpu.read_lower_opcode_parameter()

    #input(cpu.debugger.format_hex(upper_param))
    opcode = cpu.read_opcode()

    registers = {0x05: 'B',0x0D: 'C',0x3D: 'A',0x1D: 'E'}
    r1 = registers[opcode]
    context.load(r1).dec().store(r1).flags(Z, 1, H, C)
    val = context._get_select_reg_value()

def RET(mmu, cpu, meta, context):
    val1 = cpu.stack.pop()
    val2 = cpu.stack.pop()

    jump_address =  bitwise_functions.merge_8bit_values(val2, val1)
    cpu.debugger.print_iv(jump_address)
    cpu.pc = jump_address

def DI(mmu, cpu, meta, context):
    cpu.interrupts_enabled = False

def EI(mmu, cpu, meta, context):
    cpu.interrupts_enabled = True


def INCnn(mmu, cpu, meta, context):
    cpu.debugger.print_opcode('INCnn')
    parameter = cpu.read_upper_opcode_parameter()
    result = False

    if parameter == 0x01:
        result = True
        DE = cpu.reg.GET_DE()
        DE += 1
        cpu.reg.SET_DE(DE)

    elif parameter == 0x02:
        result = True
        HL = cpu.reg.GET_HL()
        HL += 1
        cpu.reg.SET_HL(HL)

    return result

def INCn(mmu, cpu, meta, context):
    cpu.reg.CLEAR_SUBSTRACT()
    upper_param = cpu.read_upper_opcode_parameter()
    lower_param = cpu.read_lower_opcode_parameter()
    result = False
    selected_register = None

    if lower_param == 0x40:
        if upper_param == 0x00:
            B = cpu.reg.GET_B()
            selected_register = B
            B = B + 1
            cpu.reg.SET_B(B)
            result = True
    if lower_param == 0xC0:
        if upper_param == 0x00:
            C = cpu.reg.GET_C()
            selected_register = C
            C = C + 1
            # get the third bit by shifting 2 positions to the right and do a and against 0000 0001
            cpu.reg.SET_C(C)
            result = True


    if selected_register >> 2 & 0x1 == 0x1:
        cpu.reg.SET_HALF_CARRY()

    return result

# length: 2 bytes
# 0xF0 and 1 byte unsigned
# write contents of address FF00 + n into register A

def LDHAn(mmu, cpu, meta, context):
    # get 8 bit unsigned parameter
    cpu.pc += 1
    n = mmu.read(cpu.pc)
    # print disassembly info

    # read A register
    A = cpu.reg.GET_A()

    offset_address = 0xFF00 + n
    cpu.debugger.print_iv(offset_address)
    value = mmu.read(offset_address)
    cpu.reg.SET_A(value)

# length: 2 bytes
# 0xE0 and 1 byte unsigned
# write contents of register A to memory address FF00 + n
def LDHnA(mmu, cpu, meta):
    opcode = Opcode(meta)
    # get 8 bit unsigned parameter
    cpu.pc += 1
    val = mmu.read(cpu.pc)
    # print disassembly info
    cpu.debugger.print_opcode(opcode)
    cpu.debugger.print_iv(val)

    # read A register
    A = cpu.reg.GET_A()

    offset_address = 0xFF00 + val

    mmu.write(offset_address, A)
    return meta.get_cycles()

# length: 1 byte
# 0x1A
# Read the Value of register DE from memory and put the contents of adress DE in A
def LDAn(mmu, cpu, meta, context):

    parameter = cpu.read_upper_opcode_parameter()
    result = False
    if parameter == 0x1:
        DE = cpu.reg.GET_DE()
        val = mmu.read(DE)
        cpu.reg.SET_A(val)
        result = True

    return result


# length 1 byte
# 0xE2
# write contents of register A to memory address FF00 + C
def LDCA(mmu, cpu, meta, context):
    C =  cpu.reg.GET_C()
    A = cpu.reg.GET_A()
    offset_address = 0xFF00 + C
    mmu.write(offset_address, A)

def CPn(mmu, cpu, meta, context):
    cpu.pc += 1
    n = mmu.read(cpu.pc)

    A = cpu.reg.GET_A()
    cpu.reg.SET_SUBSTRACT()
    result = A - n
    if result == 0x00:
        cpu.reg.SET_ZERO()
    else:
        cpu.reg.CLEAR_ZERO()


    if A < n:
        cpu.reg.SET_CARRY()
    else:
        cpu.reg.CLEAR_CARRY()

    half_carry = (A & 0x0F) < (n & 0x0F)

    if half_carry:
        cpu.reg.SET_HALF_CARRY()
    else:
        cpu.reg.CLEAR_HALF_CARRY()

# length: 3 bytes
# Put value A into nn
# 0xEA 16 bit immediate value
def LDnn16a(mmu, cpu, meta, context):
    A = cpu.reg.GET_A()
    cpu.pc += 1
    address = mmu.read_u16(cpu.pc)
    mmu.write(address, A)
    cpu.pc += 1

def LDnA(mmu, cpu):
     cpu.debugger.print_opcode('LDnA')
     upper_param = cpu.read_upper_opcode_parameter()
     lower_param = cpu.read_lower_opcode_parameter()
     A = cpu.reg.GET_A()
     result = False

     if lower_param == 0x70:
         if upper_param == 0x06:
             H = cpu.reg.GET_H()
             H = A
             cpu.reg.SET_H(H)
             result = True
         elif upper_param == 0x05:
             D = cpu.reg.GET_D()
             D = A
             cpu.reg.SET_D(D)
             result = True

     elif lower_param == 0xF0:
        if upper_param == 0x04:
             C = cpu.reg.GET_C()
             C = A
             cpu.reg.SET_C(C)
             result = True

     return result

def POPBC(mmu, cpu, meta, context):
    context.pop().store('C').pop().store('B')

def PUSHBC(mmu, cpu, meta, context):
    context.load('B').push().load('C').push()
    #B = cpu.reg.GET_B()
    #C = cpu.reg.GET_C()
    #cpu.stack.push(B)
    #cpu.stack.push(C)

def LDn8d(mmu, cpu, meta, context):
    # get Register from opcode
    pc = cpu.pc + 1
    val = mmu.read(pc)
    cpu.debugger.print_iv(val)
    upper_parameter = cpu.read_upper_opcode_parameter()

    lower_parameter = cpu.read_lower_opcode_parameter()

    result = False
    cpu.pc = pc
    if lower_parameter == 0x60:
        if upper_parameter == 0x0:
            cpu.reg.SET_B(val)
            B = cpu.reg.GET_B()
            result = True
    elif lower_parameter == 0xE0:
        if upper_parameter == 0x00:
            cpu.reg.SET_C(val)
            C = cpu.reg.GET_C()
            result = True
        elif upper_parameter == 0x01:
            cpu.reg.SET_E(val)
            E = cpu.reg.GET_L()
            result = True
        elif upper_parameter == 0x02:
            cpu.reg.SET_L(val)
            L = cpu.reg.GET_L()
            result = True
        elif upper_parameter == 0x03:
            cpu.reg.SET_A(val)
            A = cpu.reg.GET_A()
            result = True

def OR_r(mmu, cpu, meta, context):
    upper_param = cpu.read_upper_opcode_parameter()
    lower_param = cpu.read_lower_opcode_parameter()
    context.load('A').bitwise('C', BitwiseOperators.OR).store('A')

def LD_n_n(mmu, cpu, meta, context):
    upper_param = cpu.read_upper_opcode_parameter()
    lower_param = cpu.read_lower_opcode_parameter()

    #print('show params')
    #input(cpu.debugger.format_hex(upper_param))
    #input(cpu.debugger.format_hex(lower_param))

    register_operand_1 = { 0x07: 'A',0x04: 'C',0x05: 'D',0x06: 'H'}
    register_operand_2 = { 0x80: 'B',0xF0: 'A',0xb0: 'E',0x70: 'A'}
    r2 = register_operand_2[lower_param]
    r1 = register_operand_1[upper_param]

    context.load(r2).store(r1)

def CPL(mmu, cpu, meta, context):
    context.load('A').bitwise('A', BitwiseOperators.CPL).store('A')

def LDHLnn(mmu, cpu, meta, context):
    context.load(addressing_mode=AddressingMode.d8).store('HL')


# length: 3 bytes
# 0x31 and 2 bytes unsigned
def LDnn16d(mmu, cpu, meta, context):
    parameter = cpu.read_upper_opcode_parameter()
    cpu.pc += 1
    val = mmu.read_u16(cpu.pc)
    cpu.debugger.print_iv(val)
    if parameter == 0x03:
        cpu.reg.SET_SP(val)
    elif parameter == 0x02:
        cpu.reg.SET_HL(val)
    elif parameter == 0x01:
        cpu.reg.SET_DE(val)
    elif parameter == 0x00:
        cpu.reg.SET_BC(val)

    cpu.pc += 1

def LDHL8A(mmu, cpu, meta, context):
    context.load('HL').store('A',AddressingMode.dr16)

def LDI_HL_A(mmu, cpu, meta, context):
    r1 = 'HL'
    r2 = 'A'
    context.load('HL').store('A', addressing_mode=AddressingMode.dr16).load('HL').inc().store()

def LDI_A_HL(mmu, cpu, meta, context):
    r1 = 'HL'
    r2 = 'A'
    context.load('HL', addressing_mode=AddressingMode.ir16).store('A').load('HL').inc().store()

#def LDIHL8A(mmu, cpu, meta, context):


def LDDHL8A(mmu, cpu, meta, context):
    parameter = cpu.read_upper_opcode_parameter()
    # get A
    A = cpu.reg.GET_A()
    AF = cpu.reg.GET_AF()
    HL = cpu.reg.GET_HL()
    mmu.write(HL,A)
    result = False
    if parameter == 0x03:
        HL -= 1
        result = True
    elif parameter == 0x02:
        HL += 1
        result = True
    cpu.reg.SET_HL(HL)


# length: 1 bytes
# 0xAF
def XORn(mmu, cpu, meta, context):
  lower_param = cpu.read_lower_opcode_parameter()
  result = False
  if lower_param == 0xF0:
    A = cpu.reg.GET_A()
    A = A ^ A
    if A == 0x0:
      cpu.reg.SET_ZERO()
    else:
      cpu.reg.CLEAR_ZERO()

    cpu.reg.CLEAR_CARRY()
    cpu.reg.CLEAR_SUBSTRACT()
    cpu.reg.CLEAR_HALF_CARRY()

    cpu.reg.SET_A(A)

    result = True

# special prefix for a different set of opcodes
def CB(mmu, cpu, meta, context):
    cpu.pc += 1
    opcode = cpu.read_opcode()
    instruction = cpu.cb_opcodes[opcode]
    # fetch the special instruction from cb_opcode list
    # increment the PC, so we can get the CB instruction
    # do nothing, its just a prefix
    result = False
    if instruction:
        result = instruction(mmu, cpu)
    else:
        hex = cpu.debugger.format_hex(opcode)
        print(f'Unknown CB opcode {hex} at {cpu.pc}')

    return result

def JRn(mmu, cpu, meta, context):
    pc = cpu.pc
    cpu.pc += 1
    jump_address = mmu.read_s8(cpu.pc)
    cpu.debugger.print_iv(jump_address)
    cpu.pc += jump_address


def JRZn(mmu, cpu, meta, context):
    cpu.pc += 1
    val = mmu.read_s8(cpu.pc)
    cpu.debugger.print_iv(val)
    #jump_address = cpu.pc + val
    if cpu.reg.GET_ZERO():
        jump_address = cpu.pc + val
        cpu.pc = jump_address

def JPnn(mmu, cpu, meta, context):
    cpu.pc += 1
    nn = mmu.read_u16(cpu.pc)
    cpu.debugger.print_iv(nn)
    cpu.pc = nn - 1

def JRNZn(mmu, cpu, meta, context):
    pc = cpu.pc + 1
    val = mmu.read_s8(pc)
    cpu.debugger.print_iv(val)
    jump_address = pc
    if not cpu.reg.GET_ZERO():
        jump_address += val
        cpu.pc = jump_address
    else:
        cpu.pc += 1

# length: 3 bytes
# 0xCD
# pushes the PC to the stack and jump to specified 16 bit operand
def CALLnn(mmu, cpu, meta, context):
    # address of next instruction
    pc = cpu.pc + 1
    val = mmu.read_u16(pc)
    pc += 1

    cpu.debugger.print_iv(val)
    # Decrease the jump value by one, because the step will do a +1
    cpu.pc = val - 0x01
    SP = cpu.reg.GET_SP()
    cpu.stack.push_u16bit(pc)

    # push address of next instruction to the stack
    return True


def RLA(mmu, cpu, meta, context):
    # get the value from the C register
    A = cpu.reg.GET_A()
    previous_carry = cpu.reg.GET_CARRY()

    # get msb from register
    msb = (A & 0x80) == 0x80

    A = bitwise_functions.shift_left(A, 8)
    A |= previous_carry

    cpu.reg.SET_A(A)
    if A == 0x00:
        cpu.reg.SET_ZERO()
    else:
        cpu.reg.CLEAR_ZERO()
    # set the contents of msb to the carry flag
    if msb:
        cpu.reg.SET_CARRY()
    else:
        cpu.reg.CLEAR_CARRY()
    # clear substract and half carry
    cpu.reg.CLEAR_SUBSTRACT()
    cpu.reg.CLEAR_HALF_CARRY()
    return True



# CB opcodes
def BIT7H(mmu, cpu):
    cpu.debugger.print_opcode('BIT7H')
    HL = cpu.reg.GET_HL()
    H = MMU.get_high_byte(HL)
    # check if most significant bit is 1
    isset = H >> 7 & 0x01

    if isset:
        cpu.reg.CLEAR_ZERO()
    else:
        cpu.reg.SET_ZERO()

    return True

# length: 2 bytes
# 0xCB 0x11
# Rotates C register left and sets carry bit if most significant bit is 1
# It seems what we are doing here is called 'Rotate trough carry'
# where the most significant bit is shifted out, put in a carry bit and
#
def RLC(mmu, cpu):
    cpu.debugger.print_opcode('RLC')
    # get the value from the C register
    C = cpu.reg.GET_C()
    previous_carry = cpu.reg.GET_CARRY()

    # get msb from register
    msb = (C & 0x80) == 0x80


    C = bitwise_functions.shift_left(C, 8)
    C |= previous_carry

    cpu.reg.SET_C(C)
    if C == 0x00:
        cpu.reg.SET_ZERO()
    else:
        cpu.reg.CLEAR_ZERO()
    # set the contents of msb to the carry flag
    if msb:
        cpu.reg.SET_CARRY()
    else:
        cpu.reg.CLEAR_CARRY()
    # clear substract and half carry
    cpu.reg.CLEAR_SUBSTRACT()
    cpu.reg.CLEAR_HALF_CARRY()
    return True
