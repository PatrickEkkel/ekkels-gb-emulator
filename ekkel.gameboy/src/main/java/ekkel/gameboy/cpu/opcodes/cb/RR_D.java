package ekkel.gameboy.cpu.opcodes.cb;

import core.cpu.registers.Registers;

public class RR_D extends RR_r {

    public RR_D() {
        this.instr = 0x1A;
        this.setLoadRegister(Registers.D);
    }

}
