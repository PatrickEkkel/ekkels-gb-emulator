package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_H_C  extends LD_r_r {

    public LD_H_C() {
        this.instr = 0x61;
        this.setLeftRegister(Registers.H);
        this.setRightRegister(Registers.C);
    }
}
