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
      cpu.reg.SET_ZERO_FLAG(True)
  cpu.debugger.print_register('A', A,8)
  cpu.reg.SET_AF(A) 
  return True
    
# special prefix for a different set of opcodes
def CB(mmu, cpu):
    cpu.debugger.print_opcode('CB')
    cpu.pc += 1
    opcode = cpu._read_pc_opcode()
    instruction = cpu.cb_opcodes[opcode]
    # fetch the special instruction from cb_opcode list 
    # increment the PC, so we can get the CB instruction
    # do nothing, its just a prefix
    result = False
    if instruction:
        result = instruction(mmu, cpu)
    else:
        hex = hex = cpu.debugger.print_hex(opcode)
        print(f'Unknown CB opcode {hex} at {cpu.pc}')
    
    return result

def JRNZN(mmu, cpu):
    cpu.debugger.print_opcode('JRNZN')
    cpu.pc += 1
    val = mmu.read_s8(cpu.pc)
    jump_address = cpu.pc
    if not cpu.reg.GET_ZERO_FLAG():
        print(val)
        print(cpu.pc)
        jump_address += val.to_bytes()
        print(cpu.debugger.print_hex(jump_address))
        #jump_address = cpu.pc + 1
        #print(cpu.debugger.print_hex(jump_address))
        #print(cpu.debugger.print_hex(cpu.pc))
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
        cpu.reg.SET_ZERO_FLAG(False)
    else:
        cpu.reg.SET_ZERO_FLAG(True)

    cpu.debugger.print_register('H',H,8)
    
    return True