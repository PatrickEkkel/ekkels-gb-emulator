package ekkel.gameboy.cpu.opcodes.add;

import core.cpu.registers.Registers;

public class ADD_HL_DE extends ADD_rr_rr {

    public ADD_HL_DE() {
        this.instr = 0x19;
        this.setLeftRegister(Registers.HL);
        this.setRightRegister(Registers.DE);
    }
}
