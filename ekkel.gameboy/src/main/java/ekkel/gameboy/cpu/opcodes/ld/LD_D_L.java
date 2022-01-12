package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_D_L extends LD_r_r {

    public LD_D_L() {
        this.instr = 0x55;
        this.setLeftRegister(Registers.D);
        this.setRightRegister(Registers.L);
    }
}
