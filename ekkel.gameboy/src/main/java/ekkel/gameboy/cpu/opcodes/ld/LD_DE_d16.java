package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_DE_d16 extends LD_nn_d16 {

    public LD_DE_d16() {
        this.instr = 0x11;
        this.setLoadRegister(Registers.DE);
    }
}
