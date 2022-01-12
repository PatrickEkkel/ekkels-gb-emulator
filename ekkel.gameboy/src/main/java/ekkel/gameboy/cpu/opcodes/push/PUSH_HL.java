package ekkel.gameboy.cpu.opcodes.push;

import core.cpu.registers.Registers;

public class PUSH_HL extends PUSH_rr {

    public PUSH_HL() {
        this.setRegister(Registers.HL);
        this.instr = 0xE5;
    }

}
