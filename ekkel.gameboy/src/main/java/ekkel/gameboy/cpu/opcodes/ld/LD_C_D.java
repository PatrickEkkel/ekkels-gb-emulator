package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_C_D extends LD_r_r {

    public LD_C_D() {
        this.instr = 0x4A;
        this.setLeftRegister(Registers.C);
        this.setRightRegister(Registers.D);
    }

}
