package ekkel.gameboy.cpu.opcodes.inc;

import core.cpu.registers.Registers;

public class INC_BC extends INC_nn {

    public INC_BC() {
        this.instr = 0x03;
        this.cycles = 8;
        this.setRegister(Registers.BC);
    }
}
