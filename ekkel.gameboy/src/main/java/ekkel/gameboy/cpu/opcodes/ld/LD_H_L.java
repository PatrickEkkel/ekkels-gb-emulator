package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_H_L  extends LD_r_r {

    public LD_H_L() {
        super();
        this.instr = 0x65;
        this.setLeftRegister(Registers.H);
        this.setRightRegister(Registers.L);
    }

}
