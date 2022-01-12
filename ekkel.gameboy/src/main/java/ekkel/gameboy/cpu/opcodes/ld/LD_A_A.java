package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_A_A  extends LD_r_r {

    public LD_A_A() {
        this.instr = 0x7F;
        this.setLeftRegister(Registers.A);
        this.setRightRegister(Registers.A);
    }
}
