
def INCn(mmu, cpu):
    cpu.debugger.print_opcode('INCn')
    cpu.reg.CLEAR_SUBSTRACT()
    parameter = cpu.read_opcode_parameter()
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

    parameter = cpu.read_opcode_parameter()
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

def LDnA(mmu, cpu):
     cpu.debugger.print_opcode('LDnA')
     parameter = cpu.read_opcode_parameter()
     A = cpu.reg.GET_A()
     result = False
     if parameter == 0x04:
       C = cpu.reg.GET_C()
       C = A
       cpu.debugger.print_register('C',C, 8)
       cpu.reg.SET_C(C)
       result = True
     return result




def LDn8d(mmu, cpu):
    cpu.debugger.print_opcode('LDn8d')
    from emulator import MMU
    # get Register from opcode
    pc = cpu.pc + 1
    val = mmu.read(pc)
    
    parameter = cpu.read_opcode_parameter()
    cpu.pc = pc
    if parameter == 0x0:
        cpu.reg.SET_C(val)
        C = cpu.reg.GET_C()
        cpu.debugger.print_register('C',C, 8)
    elif parameter == 0x3:
        cpu.reg.SET_A(val)
        A = cpu.reg.GET_A()
        cpu.debugger.print_register('A',A, 8)
        
    return True


# length: 3 bytes 
# 0x31 and 2 bytes unsigned
def LDnn16d(mmu, cpu):
    cpu.debugger.print_opcode('LDnn16d')
    from emulator import MMU
    parameter = cpu.read_opcode_parameter()
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
    from emulator import MMU
    # get A
    AF = cpu.reg.GET_AF()
    HL = cpu.reg.GET_HL()
    cpu.debugger.print_register('AF',AF,16)
    cpu.debugger.print_register('HL',HL,16)
    A = MMU.get_high_byte(AF)
    cpu.debugger.print_register('A',A,8)
    mmu.write(HL,A)
    HL -= 1
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

def JRNZN(mmu, cpu):
    cpu.debugger.print_opcode('JRNZN')
    pc = cpu.pc + 1
    val = mmu.read_s8(pc)
    #cpu.pc += 1
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
    # address of next instruction
    pc = cpu.pc + 1
    val = mmu.read_u16(pc)
    cpu.debugger.print_iv(val)
    # Decrease the jump value by one, because the step will do a +1 
    cpu.pc = val - 0x01
    SP = cpu.reg.GET_SP()
    cpu.debugger.print_register('SP',SP,16)
    cpu.stack.push(pc)

    # push address of next instruction to the stack
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