package ekkel.gameboy.cpu.opcodes.inc;

import core.cpu.registers.Registers;

public class INC_DE extends INC_nn {

    public INC_DE() {
        this.instr = 0x13;
        this.setRegister(Registers.DE);
        this.cycles = 8;
    }
}
