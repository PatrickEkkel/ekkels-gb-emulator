package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_C_B extends LD_r_r {

    public LD_C_B() {
        this.instr = 0x48;
        this.setLeftRegister(Registers.C);
        this.setRightRegister(Registers.B);
    }
}
