package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_HL_E extends LD_i16_r {

    public LD_HL_E() {
        this.instr = 0x73;
        this.setLeftLoadRegister(Registers.HL);
        this.setRightLoadRegister(Registers.E);
    }

}
