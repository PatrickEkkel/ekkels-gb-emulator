package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_C_E extends LD_r_r {

    public LD_C_E() {
        this.instr = 0x4B;
        this.setLeftRegister(Registers.C);
        this.setRightRegister(Registers.E);
    }
}
