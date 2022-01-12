package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_L_d8 extends LD_r_d8 {

    public LD_L_d8() {
        this.instr = 0x2E;
        this.setLoadRegister(Registers.L);
    }

}
