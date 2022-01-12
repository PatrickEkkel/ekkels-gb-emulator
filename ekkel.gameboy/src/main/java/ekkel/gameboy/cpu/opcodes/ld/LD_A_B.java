package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_A_B extends LD_r_r {

    public LD_A_B() {
        super();
        this.setLeftRegister(Registers.A);
        this.setRightRegister(Registers.B);
        this.instr = 0x78;
    }
}
