

def CP(cpu):
    pass
# length: 3 bytes 
# 0x31 (1 byte) (2 bytes) unsigned
def LD16d(mmu, cpu):
    cpu.pc += 1
    mem = mmu.read_u16(cpu.pc)
    cpu.set_sp(mem)
    if cpu.debug_opcode:
        print(f'CPU: {cpu.debug(mem)}')
    cpu.pc += 2
    