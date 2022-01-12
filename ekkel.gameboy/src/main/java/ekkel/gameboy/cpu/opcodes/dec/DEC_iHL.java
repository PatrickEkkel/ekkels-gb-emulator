package ekkel.gameboy.cpu.opcodes.dec;

import core.cpu.registers.Registers;

public class DEC_iHL extends DEC_ir16 {

    public DEC_iHL() {
        this.setRightRegister(Registers.HL);
        this.instr = 0x35;
    }

}
