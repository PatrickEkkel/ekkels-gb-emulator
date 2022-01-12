package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_L_H  extends LD_r_r {

    public LD_L_H() {
        super();
        this.instr = 0x6C;
        this.setLeftRegister(Registers.L);
        this.setRightRegister(Registers.H);
    }
}
