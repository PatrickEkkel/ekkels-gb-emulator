package ekkel.gameboy.cpu.opcodes.cb;

import core.cpu.registers.Registers;

public class SRL_A extends SRL_r {

    public SRL_A() {
        this.instr = 0x3F;
        this.setLoadRegister(Registers.A);
    }

}
