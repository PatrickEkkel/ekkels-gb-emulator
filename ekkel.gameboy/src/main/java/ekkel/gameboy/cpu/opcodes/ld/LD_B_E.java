package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_B_E extends LD_r_r {

    public LD_B_E() {
        this.instr = 0x43;
        this.setLeftRegister(Registers.B);
        this.setRightRegister(Registers.E);
    }
}
