package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_L_A extends LD_r_r {

    public LD_L_A() {
        this.instr = 0x6F;
        this.setLeftRegister(Registers.L);
        this.setRightRegister(Registers.A);
    }

}
