package ekkel.gameboy.cpu.opcodes.inc;

import core.cpu.registers.Registers;

public class INC_D extends INC_r {

    public INC_D() {
        this.instr = 0x14;
        this.setLoadRegister(Registers.D);
    }

}
