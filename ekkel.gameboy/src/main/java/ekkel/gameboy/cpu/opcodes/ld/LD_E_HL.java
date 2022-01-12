package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_E_HL extends LD_r_i16 {

    public LD_E_HL() {
        this.instr = 0x5E;
        this.setLeftLoadRegister(Registers.E);
        this.setRightLoadRegister(Registers.HL);
    }

}
