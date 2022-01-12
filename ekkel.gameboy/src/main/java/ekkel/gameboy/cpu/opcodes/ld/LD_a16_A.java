package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;


/**
 * Put value A into 16 bit immediate value
 */
public class LD_a16_A  extends LD_nn_r {

    public LD_a16_A() {
        super();
        this.setLoadRegister(Registers.A);
        this.instr = 0xEA;
    }
}
