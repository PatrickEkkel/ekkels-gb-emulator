package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_H_A extends LD_r_r {

    public LD_H_A() {
        this.instr = 0x67;
        this.setLeftRegister(Registers.H);
        this.setRightRegister(Registers.A);
    }
}
