package ekkel.gameboy.cpu.opcodes.dec;

import core.cpu.registers.Registers;

public class DEC_C extends DEC_r {

    public DEC_C() {
        this.instr = 0x0D;
        this.setLoadRegister(Registers.C);
    }
}
