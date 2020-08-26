

# length: 3 bytes 
# 0x31 (1 byte) (2 bytes) unsigned
def LDHL16d(mmu, cpu):
    from emulator import MMU
    cpu.pc += 1
    mem = mmu.read_u16(cpu.pc)
    # reimplement this as high byte low byte
    H = MMU.get_high_byte(mem)
    L = MMU.get_low_byte(mem)
    cpu.reg.SET_H(H)
    cpu.reg.SET_L(L)
    cpu.debugger.print_state(mem)
    cpu.pc += 1

def LDHL8A(mmu,cpu):
    pass

# length: 3 bytes 
# 0x31 (1 byte) (2 bytes) unsigned
def LDSP16d(mmu, cpu):
    cpu.pc += 1
    mem = mmu.read_u16(cpu.pc)
    cpu.reg.SET_SP(mem)
    cpu.debugger.print_state(mem)
    cpu.pc += 1

# length: 1 bytes
# 0xAF 
def XORA(mmu, cpu):
  A = cpu.reg.GET_A()
  A = A ^ A
  if A == 0x0:
      cpu.reg.SET_ZERO_FLAG(True)
  cpu.debugger.print_state(A)
  cpu.reg.SET_A(A) 
    
    