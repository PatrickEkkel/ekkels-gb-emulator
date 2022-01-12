package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_H_E extends LD_r_r {

    public LD_H_E() {
        super();
        this.instr = 0x63;
        this.setLeftRegister(Registers.H);
        this.setRightRegister(Registers.E);
    }
}
