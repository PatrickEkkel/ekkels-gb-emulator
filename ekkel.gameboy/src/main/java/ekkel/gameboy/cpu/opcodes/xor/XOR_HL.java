package ekkel.gameboy.cpu.opcodes.xor;

import core.cpu.registers.Registers;

public class XOR_HL extends XOR_i16 {

    public XOR_HL() {
        this.instr = 0xAE;
        this.setLoadRegister(Registers.HL);
    }

}
