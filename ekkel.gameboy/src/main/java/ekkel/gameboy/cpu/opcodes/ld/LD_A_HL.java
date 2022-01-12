package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_A_HL extends LD_r_i16 {

    public LD_A_HL() {
        this.instr = 0x7E;
        this.setLeftLoadRegister(Registers.A);
        this.setRightLoadRegister(Registers.HL);
    }
}
