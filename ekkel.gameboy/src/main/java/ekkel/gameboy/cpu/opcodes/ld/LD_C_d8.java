package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_C_d8 extends LD_r_d8{


    public LD_C_d8() {
        this.instr = 0x0E;
        this.setLoadRegister(Registers.C);
    }

}
