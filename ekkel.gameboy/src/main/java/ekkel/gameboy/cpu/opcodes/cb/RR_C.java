package ekkel.gameboy.cpu.opcodes.cb;

import core.cpu.registers.Registers;

public class RR_C extends RR_r {

    public RR_C() {
        this.instr = 0x19;
        this.setLoadRegister(Registers.C);
    }
}
