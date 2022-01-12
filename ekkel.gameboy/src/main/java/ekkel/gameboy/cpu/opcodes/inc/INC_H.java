package ekkel.gameboy.cpu.opcodes.inc;

import core.cpu.registers.Registers;

public class INC_H  extends INC_r {

    public INC_H() {
        this.instr = 0x24;
        setLoadRegister(Registers.H);
    }

}
