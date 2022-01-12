package ekkel.gameboy.cpu.opcodes.inc;

import core.cpu.registers.Registers;

public class INC_SP extends INC_nn {

    public INC_SP() {
        this.instr = 0x33;
        this.cycles = 8;
        this.setRegister(Registers.SP);
    }

}
