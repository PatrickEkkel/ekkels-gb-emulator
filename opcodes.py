
def INCn(mmu, cpu):
    cpu.debugger.print_opcode('INCn')

    parameter = cpu.read_opcode_parameter()
    result = False
    if parameter == 0x0:
        C = cpu.reg.GET_C()
        C = C + 1
        cpu.debugger.print_register('C',C, 8)
        cpu.reg.SET_C(C)
        result = True
    return result

def LDCA(mmu, cpu):
    cpu.debugger.print_opcode('LDCA')
    C = cpu.reg.GET_C()
    A = cpu.reg.GET_A()
    cpu.debugger.print_register('C',C, 8)
    cpu.debugger.print_register('A',A, 8)
    offset_address = 0xFF00 + C
    mmu.write(offset_address, A)
    return True


def LDn8d(mmu, cpu):
    cpu.debugger.print_opcode('LDn8d')
    from emulator import MMU
    # get Register from opcode
    pc = cpu.pc + 1
    val = mmu.read(pc)
    
    parameter = cpu.read_opcode_parameter()
    print(cpu.debugger.format_hex(cpu.read_opcode()))
    cpu.pc = pc
    if parameter == 0x0:
        cpu.reg.SET_C(val)
        C = cpu.reg.GET_C()
        cpu.debugger.print_register('C',C, 8)
    if parameter == 0x3:
        cpu.reg.SET_A(val)
        A = cpu.reg.GET_A()
        cpu.debugger.print_register('A',A, 8)
        
    return True


# length: 3 bytes 
# 0x31 (1 byte) (2 bytes) unsigned
def LDHL16d(mmu, cpu):
    cpu.debugger.print_opcode('LDHL16d')
    from emulator import MMU
    cpu.pc += 1
    HL = mmu.read_u16(cpu.pc)
    cpu.reg.SET_HL(HL)
    cpu.debugger.print_register('HL',cpu.reg.GET_HL(),16)
    cpu.pc += 1
    return True

def LDHL8A(mmu,cpu):
    cpu.debugger.print_opcode('LDHL8A')
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