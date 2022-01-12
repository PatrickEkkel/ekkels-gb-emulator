package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_B_D  extends LD_r_r {

    public LD_B_D() {
        this.instr = 0x42;
        this.setLeftRegister(Registers.B);
        this.setRightRegister(Registers.D);
    }
}
