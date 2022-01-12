package ekkel.gameboy.cpu.opcodes.xor;

import core.cpu.registers.Registers;

public class XOR_A extends XOR_r {

    public XOR_A() {
        this.instr = 0xAF;
        this.setLoadRegister(Registers.A);
    }
}
