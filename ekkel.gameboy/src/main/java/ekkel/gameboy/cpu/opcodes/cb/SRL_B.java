package ekkel.gameboy.cpu.opcodes.cb;

import core.cpu.registers.Registers;

public class SRL_B extends SRL_r {

    public SRL_B() {
        this.instr = 0x38;
        setLoadRegister(Registers.B);
    }
}
