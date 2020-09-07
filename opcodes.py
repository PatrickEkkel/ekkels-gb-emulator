import bitwise_functions


def NOP(mmu, cpu):
    cpu.debugger.print_opcode('NOP')
    
    return True

def DECn(mmu, cpu):
    cpu.debugger.print_opcode('DECn')
    
    result = False
    upper_param = cpu.read_upper_opcode_parameter()
    lower_param = cpu.read_lower_opcode_parameter()

    val = 0x00
    
    if lower_param == 0x50:  
        # do decrement on register B
        if upper_param == 0x00:
            B = cpu.reg.GET_B()
            cpu.debugger.print_register('B',B, 8)
            B -= 0x01
            val = B
            cpu.reg.SET_B(B)
            result = True
    if lower_param == 0xD0:
        # do decrement on register C
        if upper_param == 0x00:
            C = cpu.reg.GET_C()
            cpu.debugger.print_register('C',C, 8)
            C -= 0x01
            val = C
            cpu.reg.SET_C(C)
            result = True
    
        # do decrement on register A
        elif upper_param == 0x03:
            A = cpu.reg.GET_A()
            cpu.debugger.print_register('A',A, 8)
            A -= 0x01
            val = A
            cpu.reg.SET_A(A)
            result = True
    

    # set the necessary flags 
    half_carry = ((val & 0xF) - (0x01 & 0xF) & 0x10) == 0x10

    # set the zero flag
    if val == 0x00:
        cpu.reg.SET_ZERO()
    else:
        cpu.reg.CLEAR_ZERO()

    if half_carry:
        cpu.reg.SET_HALF_CARRY()
    else:
        cpu.reg.CLEAR_HALF_CARRY()
    # set substract flag
    cpu.reg.SET_SUBSTRACT()

    return result

def RET(mmu, cpu):
    cpu.debugger.print_opcode('RET')
    val1 = cpu.stack.pop()
    val2 = cpu.stack.pop()
    
    jump_address =  bitwise_functions.merge_8bit_values(val2, val1)
    cpu.debugger.print_iv(jump_address)
    cpu.pc = jump_address
    return True

def INCnn(mmu, cpu):
    cpu.debugger.print_opcode('INCnn')
    parameter = cpu.read_upper_opcode_parameter()
    result = False

    if parameter == 0x01:
        result = True
        DE = cpu.reg.GET_DE()
        cpu.debugger.print_register('DE',DE, 16)
        DE += 1
        cpu.reg.SET_DE(DE)
    
    elif parameter == 0x02:
        result = True
        HL = cpu.reg.GET_HL()
        cpu.debugger.print_register('HL',HL, 16)
        HL += 1
        cpu.reg.SET_HL(HL)
    
    return result
    



def INCn(mmu, cpu):
    cpu.debugger.print_opcode('INCn')
    cpu.reg.CLEAR_SUBSTRACT()
    parameter = cpu.read_upper_opcode_parameter()
    result = False
    selected_register = None
    if parameter == 0x0:
        C = cpu.reg.GET_C()
        selected_register = C
        C = C + 1
        # get the third bit by shifting 2 positions to the right and do a and against 0000 0001
        
        cpu.debugger.print_register('C',C, 8)
        cpu.reg.SET_C(C)
        result = True
    

    if selected_register >> 2 & 0x1 == 0x1:
        cpu.reg.SET_HALF_CARRY()

    return result

# length: 2 bytes 
# 0xE0 and 1 byte unsigned
# write contents of register A to memory address FF00 + n
def LDHnA(mmu, cpu):
    # get 8 bit unsigned parameter
    cpu.pc += 1
    val = mmu.read(cpu.pc)
    # print disassembly info
    cpu.debugger.print_opcode('LDHnA')
    cpu.debugger.print_iv(val)
   
    # read A register
    A = cpu.reg.GET_A()
    cpu.debugger.print_register('A',A, 8)
    
    offset_address = 0xFF00 + val
    
    mmu.write(offset_address, A)
    return True
# length: 1 byte
# 0x1A
# Read the Value of register DE from memory and put the contents of adress DE in A
def LDAn(mmu, cpu):
    cpu.debugger.print_opcode('LDAn')

    parameter = cpu.read_upper_opcode_parameter()
    result = False
    if parameter == 0x1:
        DE = cpu.reg.GET_DE()
        cpu.debugger.print_register('DE',DE, 16)
        val = mmu.read(DE)
        cpu.reg.SET_A(val)
        A = cpu.reg.GET_A()
        cpu.debugger.print_register('A',A, 8)
        result = True
    
    return result

       
# length 1 byte
# 0xE2 
# write contents of register A to memory address FF00 + C
def LDCA(mmu, cpu):
    cpu.debugger.print_opcode('LDCA')
    C = cpu.reg.GET_C()
    A = cpu.reg.GET_A()
    cpu.debugger.print_register('C',C, 8)
    cpu.debugger.print_register('A',A, 8)
    offset_address = 0xFF00 + C
    mmu.write(offset_address, A)
    return True

def LDnn(mmu, cpu):
    cpu.debugger.print_opcode('LDnn')
    parameter = cpu.read_upper_opcode_parameter()
    cpu.debugger.print_iv(parameter)
    result = False
    if parameter == 0x7:
        E = cpu.reg.GET_E()
        A = cpu.reg.GET_A()
        cpu.debugger.print_register('E',E, 8)
        cpu.debugger.print_register('A',A, 8)
        A = E
        cpu.reg.SET_A(A)
        result = True

    return result
     
def CPn(mmu, cpu):
    cpu.debugger.print_opcode('CPn')
     
    cpu.pc += 1
    n = mmu.read(cpu.pc)
    cpu.debugger.print_iv(n)
    A = cpu.reg.GET_A()
    
    cpu.reg.SET_SUBSTRACT()

    if A == n:
        cpu.reg.SET_ZERO()
    elif A < n:
        cpu.reg.SET_CARRY()

    half_carry = (A & 0x0F) < (n & 0x0F)

    if half_carry:
        cpu.reg.SET_HALF_CARRY()

    
    return True

    
# TODO: test needed
# length: 3 bytes
# Put value A into nn 
# 0xEA 16 bit immediate value
def LDnn16a(mmu, cpu):
    cpu.debugger.print_opcode('LDnn16a')
    A = cpu.reg.GET_A()
    cpu.pc += 1
    address = mmu.read_u16(cpu.pc)
    cpu.debugger.print_register('A',A, 8)
    mmu.write(address, A)
    cpu.pc += 1
    return True
       
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
             cpu.debugger.print_register('H', H, 8)
             cpu.reg.SET_H(H)
             result = True
         elif upper_param == 0x05:
             D = cpu.reg.GET_D()
             D = A
             cpu.debugger.print_register('D', D, 8)
             cpu.reg.SET_D(D)
             result = True

     elif lower_param == 0xF0:     
        if upper_param == 0x04:
             C = cpu.reg.GET_C()
             C = A
             cpu.debugger.print_register('C',C, 8)
             cpu.reg.SET_C(C)
             result = True
      
     return result

def POPBC(mmu, cpu):
    cpu.debugger.print_opcode('POPBC')
    val_l = cpu.stack.pop()
    val_r = cpu.stack.pop()

    cpu.reg.SET_BC(bitwise_functions.merge_8bit_values(val_l, val_r))
    BC = cpu.reg.GET_BC()
    cpu.debugger.print_register('BC', BC, 16)
    return True

def PUSHBC(mmu, cpu):
    cpu.debugger.print_opcode('PUSHBC')
    
    B = cpu.reg.GET_B()
    C = cpu.reg.GET_C()

    cpu.debugger.print_register('B',C, 8)
    cpu.debugger.print_register('C',C, 8)

    cpu.stack.push(B)
    cpu.stack.push(C)
    return True

def LDn8d(mmu, cpu):
    cpu.debugger.print_opcode('LDn8d')
    from emulator import MMU
    # get Register from opcode
    pc = cpu.pc + 1
    val = mmu.read(pc)
    
    upper_parameter = cpu.read_upper_opcode_parameter()

    lower_parameter = cpu.read_lower_opcode_parameter()
    
    result = False
    cpu.pc = pc

    if lower_parameter == 0x60:
        if upper_parameter == 0x0:
            cpu.reg.SET_B(val)
            B = cpu.reg.GET_B()
            cpu.debugger.print_register('B', B, 8)
            result = True
    else:
        if upper_parameter == 0x00:
            cpu.reg.SET_C(val)
            C = cpu.reg.GET_C()
            cpu.debugger.print_register('C',C, 8)
            result = True
        elif upper_parameter == 0x02:
            cpu.reg.SET_L(val)
            L = cpu.reg.GET_L()
            cpu.debugger.print_register('L',L, 8)
            result = True
        elif upper_parameter == 0x03:
            cpu.reg.SET_A(val)
            A = cpu.reg.GET_A()
            cpu.debugger.print_register('A',A, 8)
            result = True
        
    return result


# length: 3 bytes 
# 0x31 and 2 bytes unsigned
def LDnn16d(mmu, cpu):
    cpu.debugger.print_opcode('LDnn16d')
    from emulator import MMU
    parameter = cpu.read_upper_opcode_parameter()
    cpu.pc += 1
    val = mmu.read_u16(cpu.pc)
    cpu.debugger.print_iv(val)
    if parameter == 0x02:
        cpu.reg.SET_HL(val)
        cpu.debugger.print_register('HL',cpu.reg.GET_HL(),16)
    elif parameter == 0x01:
        cpu.reg.SET_DE(val)
        cpu.debugger.print_register('DE',cpu.reg.GET_DE(),16)
        pass
    cpu.pc += 1
    return True

def LDHL8A(mmu, cpu):
    cpu.debugger.print_opcode('LDHL8A')
    from emulator import MMU
    A = cpu.reg.GET_A()
    HL = cpu.reg.GET_HL()
    mmu.write(HL, A)
    return True

def LDDHL8A(mmu, cpu):
    cpu.debugger.print_opcode('LDDHL8A')
    parameter = cpu.read_upper_opcode_parameter()
    from emulator import MMU
    # get A
    A = cpu.reg.GET_A()
    AF = cpu.reg.GET_AF()
    HL = cpu.reg.GET_HL()
    cpu.debugger.print_register('AF',AF,16)
    cpu.debugger.print_register('HL',HL,16)
    #A = MMU.get_high_byte(AF)
    cpu.debugger.print_register('A',A,8)
    mmu.write(HL,A)
    result = False 
    if parameter == 0x03:
        HL -= 1
        result = True
    elif parameter == 0x02:
        HL += 1
        result = True
    cpu.reg.SET_HL(HL)
    cpu.debugger.print_register('HL',cpu.reg.GET_HL(),8)
    return True

# length: 3 bytes 
# 0x31 (1 byte) (2 bytes) unsigned
def LDSP16d(mmu, cpu):
    cpu.debugger.print_opcode('LDSP16d')
    cpu.pc += 1
    SP = mmu.read_u16(cpu.pc)
    cpu.reg.SET_SP(SP)
    cpu.debugger.print_register('SP',SP,16)
    cpu.pc += 1
    return True

# length: 1 bytes
# 0xAF 
def XORA(mmu, cpu):
  cpu.debugger.print_opcode('XORA')
  A = cpu.reg.GET_AF()
  A = A ^ A
  if A == 0x0:
      cpu.reg.SET_ZERO()
  cpu.debugger.print_register('A', A,8)
  cpu.reg.SET_AF(A) 
  return True
    
# special prefix for a different set of opcodes
def CB(mmu, cpu):
    cpu.debugger.print_opcode('CB')
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

def JRn(mmu, cpu):
    cpu.debugger.print_opcode('JRn')
    pc = cpu.pc
    cpu.pc += 1
    jump_address = mmu.read_s8(cpu.pc)
    cpu.debugger.print_iv(jump_address)
    cpu.pc += jump_address
    return True


def JRZn(mmu, cpu):
    cpu.debugger.print_opcode('JRZn')
    cpu.pc += 1
    val = mmu.read_s8(cpu.pc)
    cpu.debugger.print_iv(val)
    #jump_address = cpu.pc + val
    if cpu.reg.GET_ZERO():
        jump_address = cpu.pc + val
        cpu.pc = jump_address
    else:
        cpu.pc += 1
    return True
    

    
def JRNZn(mmu, cpu):
    cpu.debugger.print_opcode('JRNZn')
    pc = cpu.pc + 1
    val = mmu.read_s8(pc)
    cpu.debugger.print_iv(val)
    jump_address = pc
    if not cpu.reg.GET_ZERO():
        jump_address += val
        cpu.pc = jump_address
    else:
        cpu.pc += 1
    return True
    
# length: 3 bytes 
# 0xCD 
# pushes the PC to the stack and jump to specified 16 bit operand
def CALLnn(mmu, cpu):
    cpu.debugger.print_opcode('CALLnn')
    from emulator import MMU
    
    # address of next instruction
    pc = cpu.pc + 1
    val = mmu.read_u16(pc)
    pc += 1

    cpu.debugger.print_iv(val)
    # Decrease the jump value by one, because the step will do a +1 
    cpu.pc = val - 0x01
    SP = cpu.reg.GET_SP()
    cpu.debugger.print_register('SP',SP,16)
    cpu.stack.push_u16bit(pc)
    #cpu.stack.push(pc)

    # push address of next instruction to the stack
    return True


def RLA(mmu, cpu):
    cpu.debugger.print_opcode('RLA')
    # get the value from the C register
    A = cpu.reg.GET_A()
    previous_carry = cpu.reg.GET_CARRY()

    cpu.debugger.print_register('A', cpu.reg.GET_A(),8)
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
    from emulator import MMU
    cpu.debugger.print_opcode('BIT7H')
    HL = cpu.reg.GET_HL()
    cpu.debugger.print_register('HL',HL,16)
    H = MMU.get_high_byte(HL)
    # check if most significant bit is 1
    isset = H >> 7 & 0x01

    if isset:
        cpu.reg.CLEAR_ZERO()
    else:
        cpu.reg.SET_ZERO()

    cpu.debugger.print_register('H',H,8)
    
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

    cpu.debugger.print_register('C', cpu.reg.GET_C(),8)
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