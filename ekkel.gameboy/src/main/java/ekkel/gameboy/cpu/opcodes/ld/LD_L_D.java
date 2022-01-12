package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_L_D  extends LD_r_r {

    public LD_L_D() {
        super();
        this.instr = 0x6A;
        this.setLeftRegister(Registers.L);
        this.setRightRegister(Registers.D);
    }
}
