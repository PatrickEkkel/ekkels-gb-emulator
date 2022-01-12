package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_H_d8 extends LD_r_d8 {

    public LD_H_d8() {
        this.setLoadRegister(Registers.H);
        this.instr = 0x26;
    }

}
