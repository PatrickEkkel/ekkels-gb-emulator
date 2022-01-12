package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_BC_d16 extends LD_nn_d16 {

    public LD_BC_d16() {
        this.instr = 0x01;
        this.setLoadRegister(Registers.BC);
    }
}
