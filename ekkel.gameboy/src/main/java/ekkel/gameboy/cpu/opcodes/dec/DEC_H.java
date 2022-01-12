package ekkel.gameboy.cpu.opcodes.dec;

import core.cpu.registers.Registers;

public class DEC_H extends DEC_r {

    public DEC_H() {
        this.setLoadRegister(Registers.H);
        this.instr = 0x25;
    }

}
