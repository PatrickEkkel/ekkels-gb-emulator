package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_C_HL extends LD_r_i16 {

    public LD_C_HL() {
        this.instr = 0x4E;
        this.setLeftLoadRegister(Registers.C);
        this.setRightLoadRegister(Registers.HL);
    }
}
