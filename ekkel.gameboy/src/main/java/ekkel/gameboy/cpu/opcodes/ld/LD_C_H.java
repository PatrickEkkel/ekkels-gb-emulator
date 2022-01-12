package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_C_H extends LD_r_r {

    public LD_C_H() {
        this.instr = 0x4C;
        this.setLeftRegister(Registers.C);
        this.setRightRegister(Registers.H);
    }
}
