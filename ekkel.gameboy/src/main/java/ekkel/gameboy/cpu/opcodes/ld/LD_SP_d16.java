package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;
import core.mmu.Computable;
import core.mmu.MemoryAddress;

public class LD_SP_d16 extends LD_nn_d16 {

    public LD_SP_d16() {
        super();
        this.instr = 0x31;
        this.setLoadRegister(Registers.SP);
    }
}
