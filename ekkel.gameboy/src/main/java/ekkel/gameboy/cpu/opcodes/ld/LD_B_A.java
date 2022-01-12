package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_B_A extends LD_r_r {

    public LD_B_A() {
        this.setLeftRegister(Registers.B);
        this.setRightRegister(Registers.A);
        this.instr = 0x47;
    }

}
