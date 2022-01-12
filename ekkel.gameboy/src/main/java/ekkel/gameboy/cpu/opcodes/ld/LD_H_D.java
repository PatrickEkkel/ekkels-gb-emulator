package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_H_D extends LD_r_r {

    public LD_H_D() {
        this.instr = 0x62;
        this.setLeftRegister(Registers.H);
        this.setRightRegister(Registers.D);
    }
}
