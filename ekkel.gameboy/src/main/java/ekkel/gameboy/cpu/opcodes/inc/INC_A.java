package ekkel.gameboy.cpu.opcodes.inc;

import core.cpu.registers.Registers;

public class INC_A extends INC_r {

    public INC_A() {
        this.instr = 0x3C;
        this.setLoadRegister(Registers.A);
    }

}
