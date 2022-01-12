package ekkel.gameboy.cpu.opcodes.dec;

import core.cpu.registers.Registers;

public class DEC_A extends DEC_r {

    public DEC_A() {
        this.instr = 0x3D;
        this.setLoadRegister(Registers.A);
    }

}
