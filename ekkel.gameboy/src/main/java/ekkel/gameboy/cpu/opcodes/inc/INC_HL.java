package ekkel.gameboy.cpu.opcodes.inc;

import core.cpu.registers.Registers;

public class INC_HL extends INC_nn {

    public INC_HL() {
        this.instr = 0x23;
        this.cycles = 8;
        this.setRegister(Registers.HL);
    }
}
