package ekkel.gameboy.cpu.opcodes.dec;

import core.cpu.registers.Registers;

public class DEC_L extends DEC_r {

    public DEC_L() {
        this.instr = 0x2D;
        this.setLoadRegister(Registers.L);
    }

}
