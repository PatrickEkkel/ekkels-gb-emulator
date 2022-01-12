package ekkel.gameboy.cpu.opcodes.dec;

import core.cpu.registers.Registers;

public class DEC_B extends DEC_r {

    public DEC_B() {
        this.instr = 0x5;
        this.setLoadRegister(Registers.B);
    }
}
