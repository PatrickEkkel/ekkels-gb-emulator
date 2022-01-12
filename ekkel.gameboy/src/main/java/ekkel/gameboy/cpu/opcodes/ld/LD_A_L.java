package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_A_L extends LD_r_r {

    public LD_A_L() {
        super();
        this.instr = 0x7d;
        this.setLeftRegister(Registers.A);
        this.setRightRegister(Registers.L);
    }
}
