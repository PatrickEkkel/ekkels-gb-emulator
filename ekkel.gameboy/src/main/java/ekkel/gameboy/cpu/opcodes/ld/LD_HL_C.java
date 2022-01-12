package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_HL_C extends LD_i16_r {

    public LD_HL_C() {
        this.instr = 0x71;
        this.setLeftLoadRegister(Registers.HL);
        this.setRightLoadRegister(Registers.C);
    }

}
