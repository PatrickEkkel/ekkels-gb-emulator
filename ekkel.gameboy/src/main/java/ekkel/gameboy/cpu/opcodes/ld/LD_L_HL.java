package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_L_HL extends LD_r_i16 {

    public LD_L_HL() {
        this.instr = 0x6E;
        this.setLeftLoadRegister(Registers.L);
        this.setRightLoadRegister(Registers.HL);
    }

}
