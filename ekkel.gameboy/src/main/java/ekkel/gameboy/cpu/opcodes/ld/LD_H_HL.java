package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_H_HL extends LD_r_i16 {

    public LD_H_HL() {
        this.instr = 0x66;
        this.setLeftLoadRegister(Registers.H);
        this.setRightLoadRegister(Registers.HL);
    }

}
