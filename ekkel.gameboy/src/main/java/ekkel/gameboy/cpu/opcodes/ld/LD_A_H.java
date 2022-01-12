package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_A_H extends LD_r_r {

    public LD_A_H() {
        this.instr = 0x7C;
        this.length = 1;
        this.setLeftRegister(Registers.A);
        this.setRightRegister(Registers.H);
    }

}
