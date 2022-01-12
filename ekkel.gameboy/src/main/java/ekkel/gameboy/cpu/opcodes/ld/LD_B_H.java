package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_B_H extends LD_r_r {

    public LD_B_H() {
        this.setLeftRegister(Registers.B);
        this.setRightRegister(Registers.H);
        this.instr = 0x44;
    }
}
