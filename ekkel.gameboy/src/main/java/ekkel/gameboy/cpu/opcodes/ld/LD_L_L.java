package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_L_L  extends LD_r_r {

    public LD_L_L() {
        this.instr = 0x6D;
        this.setLeftRegister(Registers.L);
        this.setRightRegister(Registers.L);
    }

}
