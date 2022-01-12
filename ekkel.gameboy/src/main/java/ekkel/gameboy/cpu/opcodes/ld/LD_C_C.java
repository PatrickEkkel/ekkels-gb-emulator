package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_C_C extends LD_r_r {

    public LD_C_C() {
        this.instr = 0x49;
        this.setLeftRegister(Registers.C);
        this.setRightRegister(Registers.C);
    }
}
