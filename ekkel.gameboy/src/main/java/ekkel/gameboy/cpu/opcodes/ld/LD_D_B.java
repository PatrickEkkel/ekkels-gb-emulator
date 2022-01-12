package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_D_B extends LD_r_r {

    public LD_D_B() {
        this.setLeftRegister(Registers.D);
        this.setRightRegister(Registers.B);
        this.instr = 0x50;
    }

}
