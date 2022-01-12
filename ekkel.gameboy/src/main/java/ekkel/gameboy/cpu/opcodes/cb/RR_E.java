package ekkel.gameboy.cpu.opcodes.cb;

import core.cpu.registers.Registers;

public class RR_E extends RR_r {

    public RR_E() {
        this.instr = 0x1B;
        this.setLoadRegister(Registers.E);
    }

}
