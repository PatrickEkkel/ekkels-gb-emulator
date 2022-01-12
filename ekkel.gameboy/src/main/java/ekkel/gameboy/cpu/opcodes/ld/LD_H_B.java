package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_H_B  extends LD_r_r {

    public LD_H_B() {
        this.instr = 0x60;
        this.setLeftRegister(Registers.H);
        this.setRightRegister(Registers.B);
    }

}
