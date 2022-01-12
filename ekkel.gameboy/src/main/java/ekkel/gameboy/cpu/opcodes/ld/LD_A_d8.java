package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_A_d8  extends LD_r_d8 {

    public LD_A_d8() {
        this.instr = 0x3E;
        this.setLoadRegister(Registers.A);
    }
}
