package ekkel.gameboy.cpu.opcodes.add;

import core.cpu.registers.Registers;

public class ADD_HL_HL extends  ADD_rr_rr {

    public ADD_HL_HL() {
        this.instr = 0x29;
        this.setLeftRegister(Registers.HL);
        this.setRightRegister(Registers.HL);
    }
}
