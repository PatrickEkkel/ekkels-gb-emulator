package ekkel.gameboy.cpu.opcodes.xor;

import core.cpu.registers.Registers;

public class XOR_L extends XOR_r {

    public XOR_L() {
        this.instr = 0xAD;
        this.setLoadRegister(Registers.L);
    }
}
