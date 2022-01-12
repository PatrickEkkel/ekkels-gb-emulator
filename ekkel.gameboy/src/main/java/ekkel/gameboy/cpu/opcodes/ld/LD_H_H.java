package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_H_H extends LD_r_r {

    public LD_H_H() {
        this.instr = 0x64;
        this.setLeftRegister(Registers.H);
        this.setRightRegister(Registers.H);
    }
}
