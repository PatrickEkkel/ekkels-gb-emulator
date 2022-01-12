package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_HL_H extends LD_i16_r {

    public LD_HL_H() {
        this.instr = 0x74;
        this.setLeftLoadRegister(Registers.HL);
        this.setRightLoadRegister(Registers.H);
    }

}
