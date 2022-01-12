package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_C_L extends LD_r_r {

    public LD_C_L() {
        this.instr = 0x4D;
        this.setLeftRegister(Registers.C);
        this.setRightRegister(Registers.L);
    }
}
