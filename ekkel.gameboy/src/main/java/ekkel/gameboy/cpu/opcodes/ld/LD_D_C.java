package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_D_C extends LD_r_r {
    public LD_D_C() {
        this.setLeftRegister(Registers.D);
        this.setRightRegister(Registers.C);
        this.instr = 0x51;
    }
}
