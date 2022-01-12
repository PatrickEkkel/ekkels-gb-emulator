package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_A_D extends LD_r_r {

    public LD_A_D() {
        this.instr = 0x7A;
        this.setLeftRegister(Registers.A);
        this.setRightRegister(Registers.D);
    }

}
