package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_B_C  extends LD_r_r {

    public LD_B_C() {
        this.instr = 0x41;
        this.setLeftRegister(Registers.B);
        this.setRightRegister(Registers.C);
    }

}
