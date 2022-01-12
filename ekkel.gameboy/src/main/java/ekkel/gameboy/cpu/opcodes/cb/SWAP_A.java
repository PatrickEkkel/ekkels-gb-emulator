package ekkel.gameboy.cpu.opcodes.cb;

import core.cpu.registers.Registers;

public class SWAP_A extends SWAP_r {

    public SWAP_A() {
        this.instr = 0x37;
        this.setLoadRegister(Registers.A);
    }
}
