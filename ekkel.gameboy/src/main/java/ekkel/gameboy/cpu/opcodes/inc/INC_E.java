package ekkel.gameboy.cpu.opcodes.inc;

import core.cpu.registers.Registers;

public class INC_E extends INC_r {

    public INC_E() {
        this.instr = 0x1C;
        this.setLoadRegister(Registers.E);
    }

}
