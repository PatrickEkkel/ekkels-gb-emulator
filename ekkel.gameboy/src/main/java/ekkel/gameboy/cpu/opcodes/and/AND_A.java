package ekkel.gameboy.cpu.opcodes.and;

import core.cpu.registers.Registers;

public class AND_A extends AND_r {

    public AND_A() {
        this.instr = 0xA6;
        this.setLoadRegister(Registers.A);
    }
}
