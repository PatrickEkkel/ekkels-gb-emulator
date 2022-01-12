package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_B_B  extends LD_r_r {

    public LD_B_B() {
        this.instr = 0x40;
        this.setLeftRegister(Registers.B);
        this.setRightRegister(Registers.B);
    }
}
