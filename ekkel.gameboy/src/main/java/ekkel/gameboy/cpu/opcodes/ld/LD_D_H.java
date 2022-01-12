package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_D_H extends LD_r_r {

    public LD_D_H() {
        this.setLeftRegister(Registers.D);
        this.setRightRegister(Registers.H);
        this.instr = 0x54;
    }
}
