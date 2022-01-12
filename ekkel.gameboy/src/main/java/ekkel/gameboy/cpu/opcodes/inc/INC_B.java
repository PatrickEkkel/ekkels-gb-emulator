package ekkel.gameboy.cpu.opcodes.inc;

import core.cpu.registers.Registers;

public class INC_B extends INC_r {

    public INC_B() {
        this.instr = 0x04;
        this.setLoadRegister(Registers.B);
    }
}
