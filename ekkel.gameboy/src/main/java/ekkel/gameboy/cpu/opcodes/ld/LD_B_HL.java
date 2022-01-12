package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_B_HL extends LD_r_i16 {

    public LD_B_HL() {
        this.instr = 0x46;
        this.setLeftLoadRegister(Registers.B);
        this.setRightLoadRegister(Registers.HL);
    }

}
