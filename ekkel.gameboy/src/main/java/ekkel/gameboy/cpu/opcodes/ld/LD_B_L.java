package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_B_L extends LD_r_r {

    public LD_B_L() {
        this.setLeftRegister(Registers.B);
        this.setRightRegister(Registers.L);
        this.instr = 0x45;
    }

}
