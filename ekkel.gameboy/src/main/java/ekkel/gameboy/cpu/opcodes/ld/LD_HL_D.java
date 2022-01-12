package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_HL_D extends LD_i16_r {

    public LD_HL_D() {
        this.instr = 0x72;
        this.setLeftLoadRegister(Registers.HL);
        this.setRightLoadRegister(Registers.D);
    }

}
