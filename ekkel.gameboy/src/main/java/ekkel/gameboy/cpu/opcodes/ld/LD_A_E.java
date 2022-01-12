package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_A_E extends LD_r_r {

    public LD_A_E() {
        this.instr = 0x7B;
        this.setLeftRegister(Registers.A);
        this.setRightRegister(Registers.E);
    }
}
