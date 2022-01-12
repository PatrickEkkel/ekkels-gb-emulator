package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_A_a16  extends LD_r_nn {

    public LD_A_a16() {
        this.setLoadRegister(Registers.A);
        this.instr = 0xFA;
    }
}
