package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_L_E  extends LD_r_r {

    public LD_L_E() {
        this.instr = 0x6B;
        this.setLeftRegister(Registers.L);
        this.setRightRegister(Registers.E);
    }
}
