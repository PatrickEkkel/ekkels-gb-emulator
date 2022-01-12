package ekkel.gameboy.cpu.opcodes.and;

import core.cpu.registers.Registers;

public class AND_C extends AND_r {

    public AND_C() {
        this.instr = 0xA1;
        this.setLoadRegister(Registers.C);
    }
}
