package ekkel.gameboy.cpu.opcodes.dec;

import core.cpu.registers.Registers;

public class DEC_E  extends DEC_r {

    public DEC_E() {
        this.instr = 0x1D;
        this.setLoadRegister(Registers.E);
    }

}
