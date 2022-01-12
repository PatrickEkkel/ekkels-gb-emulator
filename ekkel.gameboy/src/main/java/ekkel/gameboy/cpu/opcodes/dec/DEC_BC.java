package ekkel.gameboy.cpu.opcodes.dec;

import core.cpu.registers.Registers;

public class DEC_BC extends DEC_r16 {

    public DEC_BC() {
        this.instr = 0x0B;
        this.setRightRegister(Registers.BC);
    }

}
