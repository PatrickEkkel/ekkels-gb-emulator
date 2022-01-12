package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_D_E  extends LD_r_r {

    public LD_D_E() {
        this.setLeftRegister(Registers.D);
        this.setRightRegister(Registers.E);
        this.instr = 0x53;
    }
}
