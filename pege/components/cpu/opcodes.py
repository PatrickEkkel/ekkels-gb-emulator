import bitwise_functions
import time
from components.cpu.opcode_dsl import OpcodeContext, BitwiseOperators, AddressingMode, Opcode
from ..mmu import MMU
from constants import *

I = '-'
E = 0
S = 1
Z = 2
N = 3
H = 4
C = 5


def NOP(mmu, cpu, meta, context):
    opcode = Opcode(meta)


def DEC_HL(mmu, cpu, meta, context):
    r1 = r_HL
    context.load_ir16(r1).dec().store_a16().flags(Z, 1, H,'-')
    
def DEC_rr(mmu, cpu, meta, context):
    upper_param = cpu.read_upper_opcode_parameter()
    operand_mapping = {0x00: 'BC'}
    r1 = operand_mapping[upper_param]
    context.load(r1).dec().store(r1)

# 0x05,0x3D,0x0D length: 1 byte
# decrements the value of register n by 1
# flags zhn-


def DEC_r(mmu, cpu, meta, context):
    opcode = cpu.read_opcode()

    registers = {0x05: 'B', 0x0D: 'C', 0x3D: 'A', 0x1D: 'E', 0x15: 'D'}
    r1 = registers[opcode]
    context.load(r1).dec().store(r1).flags(Z, 1, H, '-')

def RET_Z(mmu, cpu, meta, context):
    r1 = 'PC'
    context.pop().store(transient_store=True).pop().merge().branch(Z).store(r1)

def RET_NZ(mmu, cpu, meta, context):
    r1 = 'PC'
    context.pop().store(transient_store=True).pop().merge().branch(Z,invert=True).store(r1)

def RET(mmu, cpu, meta, context):
    val1 = cpu.stack.pop()
    val2 = cpu.stack.pop()

    jump_address = bitwise_functions.merge_8bit_values(val2, val1)
    cpu.debugger.print_iv(jump_address)
    cpu.pc = jump_address

def RETI(mmu, cpu, meta, context):
    r1 = r_PC
    context.set_address(0xFFFF).load_v16(0xFFFF).store_a16().pop_a16().store_rd16(r1)

def DI(mmu, cpu, meta, context):
    context.set(0xFFFF).store(value=0x0000)


def EI(mmu, cpu, meta, context):
    context.set(0xFFFF).store(value=0xFFFF)


def INC_HL(mmu, cpu, meta, context):
    r1 = r_HL
    context.load_ir16(r1).inc().store_a16().flags(Z, 0, H,'-')

def INC_rr(mmu, cpu, meta, context):
    opcode = cpu.read_opcode()
    registers = {0x13: r_DE, 0x23: r_HL}
    r1 = registers[opcode]
    context.load_rd16(r1).inc().store_rd16(r1)

def INC_r(mmu, cpu, meta, context):
    opcode = cpu.read_opcode()
    registers = {0x3C: r_A, 0xC: r_C, 0x04: r_B, 0x24: r_H, 0x1C: r_E, 0x2C: r_L, 0x14: r_D} 
    #registers = {0x3C: 'A', 0xC: 'C', 0x04: 'B', 0x24: 'H',0x1C: 'E', 0x2C: 'L', 0x14: 'D'}
    r1 = registers[opcode]
    context.load_rd8(r1).inc().store_rd8(r1).flags(Z, 0, H, '-')
    #context.load(r1).inc().store(r1).flags(Z, 0, H, '-')


# length: 2 bytes
# 0xF0 and 1 byte unsigned
# write contents of A into memory address FF00 + n

def LDH_nn_A(mmu, cpu, meta, context):
    context.load('A').load(addressing_mode=AddressingMode.d8).store('A',AddressingMode.a8)

def LDH_A_nn(mmu, cpu, meta, context):
    r1 = r_A
    context.load_d8().load_rd8(r1).load_FFOO().load_ia8().store_rd8(r1)
    
# length: 1 byte
# 0x1A
# Read the Value of register DE from memory and put the contents of adress DE in A


def LD_r_i16(mmu, cpu, meta, context):
    opcode = cpu.read_opcode()
    register_operand_1 = {0x1A: 'DE', 0x5E: 'HL', 0x56: 'HL', 0x7E: 'HL'}
    register_operand_2 = {0x1A: 'A', 0x5E: 'E', 0x56: 'D', 0x7E: 'A'}
    r1 = register_operand_1[opcode]
    r2 = register_operand_2[opcode]
    context.load(r1, addressing_mode=AddressingMode.ir16).store(r2)

# length 1 byte
# 0xE2
# write contents of register A to memory address FF00 + C
def LDCA(mmu, cpu, meta, context):
    opcode = cpu.read_opcode()

    register_operand_1 = {0xE2: r_C}
    register_operand_2 = {0xE2: r_A}
    r1 = register_operand_1[opcode]
    r2 = register_operand_2[opcode]
    context.load_rd8(r1).load_rd8(r2).load_FFOO().store_a8()

def CP_n(mmu, cpu, meta, context):
    context.load_d8().load_rd16(r_A).sub().flags(Z,1,H,C)
# length: 3 bytes
# Put value A into nn
# 0xEA 16 bit immediate value


def LD_nnnn_A(mmu, cpu, meta, context):
    context.load_a16().load_rd8(r_A).store_a8()

def AND_r(mmu, cpu, meta, context):
    opcode = cpu.read_opcode()

    register_operand_1 = {0xA1: r_C, 0xA7: r_A } 
    #register_operand_1 = {0xA1: 'C', 0xA7: 'A'}
    #r1 = 'A'
    r1 = r_A
    r2 = register_operand_1[opcode]
    context.load_rd8(r2).load_rd8(r1).bitwise_and().store_rd8(r1).flags(Z, 0, 1, 0)
    #context.load(r2).bitwise(
    #    r1, operation=BitwiseOperators.AND).store(r1).flags(Z, 0, 1, 0)


def AND_nn(mmu, cpu, meta, context):
    r1 = 'A'
    context.load(r1, transient_store=True).load(addressing_mode=AddressingMode.d8).bitwise(
        r1, operation=BitwiseOperators.AND, transient_load=True).store(r1).flags(Z, 0, 1, 0)


def POP_rr(mmu, cpu, meta, context):
    opcode = cpu.read_opcode()
    register_operand_r1 = {0xC1: 'B', 0xE1: 'H', 0xD1: 'D',0xF1: 'A'}
    register_operand_r2 = {0xC1: 'C', 0xE1: 'L', 0xD1: 'E',0xF1: 'F'}

    r1 = register_operand_r1[opcode]
    r2 = register_operand_r2[opcode]
    context.pop().store(r2).pop().store(r1)

# special ekkel sauice opcode that we can use in our unit testing to clear all flags and still use the parser
def CLRFL(mmu, cpu, meta, context):
    context.flags(0,0,0,0)

# special ekkel sauice opcode that we can use in our unit testing to set all flags and still use the parser
def SETFL(mmu, cpu, meta, context):
    context.flags(1,1,1,1)


def PUSH_rr(mmu, cpu, meta, context):
    opcode = cpu.read_opcode()
    register_operand_r1 = {0xC5: 'B', 0xE5: 'H', 0xD5: 'D', 0xF5: 'A'}
    register_operand_r2 = {0xC5: 'C', 0xE5: 'L', 0xD5: 'E', 0xF5: 'F'}

    r1 = register_operand_r1[opcode]
    r2 = register_operand_r2[opcode]

    context.load(r1).push().load(r2).push()


def LD_r_nn(mmu, cpu, meta, context):
    opcode = cpu.read_opcode()
    register_operand_1 = {0x1E: 'E', 0x06: 'B',
                          0x0E: 'C', 0x3E: 'A', 0x2E: 'L', 0x16: 'D'}
    r1 = register_operand_1[opcode]
    context.load(addressing_mode=AddressingMode.d8).store(r1)


def OR_r(mmu, cpu, meta, context):
    opcode = cpu.read_opcode()
    register_operand_1 = {0xB0: 'B', 0xB1: 'C'}
    r1 = register_operand_1[opcode]

    context.load('A').bitwise(r1, BitwiseOperators.OR).store('A').flags(Z,0,0,0)


def RST_nn(mmu, cpu, meta, context):
    r1 = 'PC'
    # go to position 0x28 
    context.load(r1).inc().push().set(0x00 + 0x27).store(r1)


def JP_HL(mmu, cpu, meta, context):
    r1 = 'HL'
    r2 = 'PC'
    context.load(r1).dec().store(r2)

def JP_Z_nnnn(mmu, cpu, meta, context):
    r1 = 'PC'
    context.load(r1,addressing_mode=AddressingMode.d16).branch(Z).store(r1)

def RES_n_r(mmu, cpu, meta, context):
    opcode = cpu.read_opcode()
    registers = {0x87: 'A'}
    values = {0x87: 0}
    r1 = registers[opcode]
    v1 = values[opcode]
    context.load(r1).reset(v1).store()


def SUB_r(mmu, cpu, meta, context):
    opcode = cpu.read_opcode()
    registers = {0x90: 'B'}

    r1 = registers[opcode]
    r2 = 'A'
    context.load(r2).sub(r1).store(r2).flags(Z, 1, H, C)

def ADD_r_r(mmu, cpu, meta, context):
    #opcode = cpu.read_opcode()
    r1 = 'A'
    r2 = 'A'
    context.load(r2).add(r1).store(r1).flags(Z, 0, H, C)

def ADD_rr_rr(mmu, cpu, meta, context):
    opcode = cpu.read_opcode()
    register_operand_1 = {0x19: 'DE'}
    r1 = 'HL'
    r2 = register_operand_1[opcode]
    context.load(r2).add(r1).store(r1).flags('-', 0, H, C)


def LD_n_n(mmu, cpu, meta, context):
    opcode = cpu.read_opcode()
   
    register_operand_1 = {0x47: 'B', 0x4F: 'C', 0x67: 'H', 0x57: 'D',
                          0x7C: 'A', 0x7B: 'A', 0x78: 'A', 0x79: 'A', 0x5F: 'E'}
    register_operand_2 = {0x47: 'A', 0x4F: 'A', 0x67: 'A', 0x57: 'A',
                          0x7C: 'H', 0x7B: 'E', 0x78: 'B', 0x79: 'C', 0x5F: 'A'}
    r1 = register_operand_1[opcode]
    r2 = register_operand_2[opcode]
    context.load(r2).store(r1)


def CPL(mmu, cpu, meta, context):
    context.load('A').bitwise('A', BitwiseOperators.CPL).store('A').flags('-',1,1,'-')


def LD_rr_nn(mmu, cpu, meta, context):
    opcode = cpu.read_opcode()

    registers = {0x12: 'DE',0x36: 'HL'}
    r1 = registers[opcode]
    context.load(r1).load(addressing_mode=AddressingMode.d8).store(addressing_mode=AddressingMode.i8)


# length: 3 bytes
# 0x31 and 2 bytes unsigned
def LDnn16d(mmu, cpu, meta, context):
    opcode = cpu.read_opcode()

    register_operand_1 = {0x11: r_DE, 0x31: r_SP, 0x21: r_HL, 0x01: r_BC}
    r1 = register_operand_1[opcode]
    context.load_d16().store_d16(r1)

def LD_r_nnnn(mmu, cpu, meta, context):
    context.load('A', addressing_mode=AddressingMode.a16).store('A')

def LD_i_rr_r(mmu, cpu, meta, context):
    opcode = cpu.read_opcode()
    register_operand_1 = {0x12: 'DE', 0x77: 'HL'}
    register_operand_2 = {0x12: 'A' , 0x77: 'A' }
    
    r1 = register_operand_1[opcode]
    r2 = register_operand_2[opcode]

    context.load(r1).store(r2, AddressingMode.dr16)


def LDI_HL_A(mmu, cpu, meta, context):
    r1 = 'HL'
    r2 = 'A'
    context.load('HL').store(
        'A', addressing_mode=AddressingMode.dr16).load('HL').inc().store()


def LDI_A_HL(mmu, cpu, meta, context):
    r1 = 'HL'
    r2 = 'A'
    context.load('HL', addressing_mode=AddressingMode.ir16).store(
        'A').load('HL').inc().store()

def LDD_HL_A(mmu, cpu, meta, context):
    context.load_rd8(r_A).load_ra16(r_HL).store_a16().dec().store_rd16(r_HL)
    
def SWAP_r(mmu, cpu, meta, context):
    context.load('A').bitwise(
        # and r with 0x0F and shift left, store the value in the transient register
        operation=BitwiseOperators.AND, value=0x0F).bitwise(
        operation=BitwiseOperators.SHIFT_LEFT, position=4).transient_store().load('A').bitwise(
         # and r with 0xF0 and shift left, or the resulting value with the transient register
        operation=BitwiseOperators.AND, value=0xF0).bitwise(
        operation=BitwiseOperators.SHIFT_RIGHT, position=4).bitwise(
        operation=BitwiseOperators.OR, transient_load=True).store('A').flags(Z,0,0,0)

# length: 1 bytes
# 0xAF


def XOR_r(mmu, cpu, meta, context):
    opcode = cpu.read_opcode()
    register_operand_1 = {0xAF: 'A', 0xA9: 'C'}
    r1 = 'A'
    r2 = register_operand_1[opcode]
    context.load(r1).bitwise(
        r2, BitwiseOperators.XOR).store(r1).flags(Z, 0, 0, 0)

# special prefix for a different set of opcodes


def CB(mmu, cpu, meta, context):
    cpu.pc += 1
    opcode = cpu.read_opcode()
    instruction = cpu.cb_opcodes[opcode]
    opcode_meta = cpu.cb_opcode_meta[opcode]
    context = cpu.cb_opcode_contexts[opcode]
    # fetch the special instruction from cb_opcode list
    # increment the PC, so we can get the CB instruction
    # do nothing, its just a prefix
    result = False
    if instruction:
        #context = OpcodeContext(cpu, mmu, meta)
        try:
            cpu.debugger.print_opcode(opcode_meta['m'])
            result = instruction(mmu, cpu, meta, context)
        except Exception as e:
            
            hex = cpu.debugger.format_hex(opcode)
            pc = cpu.debugger.format_hex(cpu.pc)
            input(f'opcode failed {hex} at {pc} cause:{e}')

    else:
        hex = cpu.debugger.format_hex(opcode)
        pc = cpu.debugger.format_hex(cpu.pc)
        input(f'Unknown CB opcode {hex} at {pc}')

    return result


def JR_nnnn(mmu, cpu, meta, context):
    context.load_sd8().load_rd8(r_PC).add().store_rd8(r_PC)

def JRZ_r8(mmu, cpu, meta, context):
    context.load_sd8().branch(Z).load_rd16(r_PC).add().store_rd16(r_PC)
    
def JP_nnnn(mmu, cpu, meta, context):
    r1 = r_PC
    context.load_d16().dec().store_rd16(r1)
    #context.load(r1, addressing_mode=AddressingMode.d16).store(r1).load(r1).dec().store(r1)

def JRNZ_r8(mmu, cpu, meta, context):
    context.load_sd8().branch(Z,invert=True).load_rd16(r_PC).add().store_rd16(r_PC)

# length: 3 bytes
# 0xCD
# pushes the PC to the stack and jump to specified 16 bit operand
def CALL_nnnn(mmu, cpu, meta, context):
    context.load_d16().dec().load_rd16(r_PC).push_d16().store_d16(r_PC)

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
    # clear substract and half carryBIT
    cpu.reg.CLEAR_SUBSTRACT()
    cpu.reg.CLEAR_HALF_CARRY()
    return True


# CB opcodes
def BIT_7_r(mmu, cpu, meta, context):
    context.load_rd8(r_H).shift_right(7).load_v8(0x01).bitwise_and().flags(Z, 0, 1, '-')

# length: 2 bytes
# 0xCB 0x11
# Rotates C register left and sets carry bit if most significant bit is 1
# It seems what we are doing here is called 'Rotate trough carry'
# where the most significant bit is shifted out, put in a carry bit and
#
def RLC(mmu, cpu, meta, context):
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
