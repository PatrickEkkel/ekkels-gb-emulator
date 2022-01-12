package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_HL_d16 extends LD_nn_d16 {

    public LD_HL_d16() {
        this.instr = 0x21;
        this.setLoadRegister(Registers.HL);
        this.length = 3;
    }

}
