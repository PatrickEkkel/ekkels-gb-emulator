package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_Ci_A extends LD_i8_r {
    public LD_Ci_A() {
        this.instr = 0xE2;
        this.setLoadRegister(Registers.A);
    }
}
