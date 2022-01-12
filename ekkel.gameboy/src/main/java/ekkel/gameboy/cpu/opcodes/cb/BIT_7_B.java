package ekkel.gameboy.cpu.opcodes.cb;

import core.cpu.registers.Registers;

public class BIT_7_B extends BIT_r {

    public BIT_7_B() {
        this.instr = 0x78;
        this.setPosition(7);
        this.setLoadRegister(Registers.B);
    }
}
