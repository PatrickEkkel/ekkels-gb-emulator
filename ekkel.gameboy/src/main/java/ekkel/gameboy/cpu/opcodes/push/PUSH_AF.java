package ekkel.gameboy.cpu.opcodes.push;

import core.cpu.registers.Registers;

public class PUSH_AF extends PUSH_rr {

    public PUSH_AF() {
        this.instr = 0xF5;
        this.setRegister(Registers.AF);
    }

}
