package ekkel.gameboy.cpu.opcodes.push;

import core.cpu.registers.Registers;

public class PUSH_BC extends PUSH_rr {

    public PUSH_BC() {
        this.instr = 0xc5;
        this.setRegister(Registers.BC);
    }
}
