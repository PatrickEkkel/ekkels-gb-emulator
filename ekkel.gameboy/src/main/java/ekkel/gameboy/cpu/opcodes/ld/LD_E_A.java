package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_E_A extends LD_r_r {

    public LD_E_A() {
        this.instr = 0x5F;
        this.setLeftRegister(Registers.E);
        this.setRightRegister(Registers.A);
    }
}
