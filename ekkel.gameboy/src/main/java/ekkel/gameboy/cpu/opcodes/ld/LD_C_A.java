package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_C_A extends LD_r_r {

    public LD_C_A() {
        this.setLeftRegister(Registers.C);
        this.setRightRegister(Registers.A);
        this.instr = 0x4F;
    }

}
