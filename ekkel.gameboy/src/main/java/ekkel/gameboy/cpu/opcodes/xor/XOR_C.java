package ekkel.gameboy.cpu.opcodes.xor;

import core.cpu.registers.Registers;
public class XOR_C  extends XOR_r {

    public XOR_C() {
        this.instr = 0xA9;
        setLoadRegister(Registers.C);
    }


}
