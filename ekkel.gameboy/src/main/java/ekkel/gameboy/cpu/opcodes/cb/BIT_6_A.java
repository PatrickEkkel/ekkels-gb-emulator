package ekkel.gameboy.cpu.opcodes.cb;

import core.cpu.registers.Registers;

public class BIT_6_A extends BIT_r {

    public BIT_6_A() {
        this.instr = 0x77;
        this.setPosition(6);
        this.setLoadRegister(Registers.A);
    }
}
