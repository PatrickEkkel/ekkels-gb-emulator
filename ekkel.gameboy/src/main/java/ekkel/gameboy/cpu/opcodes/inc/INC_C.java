package ekkel.gameboy.cpu.opcodes.inc;

import core.cpu.registers.Registers;

public class INC_C extends INC_r {

    public INC_C() {
        this.instr = 0x0C;
        this.setLoadRegister(Registers.C);
    }
}
