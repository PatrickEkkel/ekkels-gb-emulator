

# length: 3 bytes 
# 0x31 (1 byte) (2 bytes) unsigned
def LDHL16d(mmu, cpu):
    cpu.pc += 1
    mem = mmu.read_u16(cpu.pc)
    # reimplement this as high byte low byte
    H = (mem >> 8) & 0xFF 
    L = mem & 0xFF
    print('blurp')
    cpu.debugger.print_state(L)
    cpu.debugger.print_state(H)
    cpu.debugger.print_state(mem)
    cpu.pc += 1

# length: 3 bytes 
# 0x31 (1 byte) (2 bytes) unsigned
def LDSP16d(mmu, cpu):
    cpu.pc += 1
    mem = mmu.read_u16(cpu.pc)
    cpu.set_sp(mem)
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
    
    