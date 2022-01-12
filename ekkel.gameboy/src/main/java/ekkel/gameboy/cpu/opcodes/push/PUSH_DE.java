package ekkel.gameboy.cpu.opcodes.push;

import core.cpu.registers.Registers;

public class PUSH_DE extends PUSH_rr {

    public PUSH_DE() {
        this.setRegister(Registers.DE);
        this.instr = 0xD5;
    }

}
