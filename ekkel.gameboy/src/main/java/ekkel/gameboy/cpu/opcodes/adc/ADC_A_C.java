package ekkel.gameboy.cpu.opcodes.adc;

import core.cpu.registers.Registers;

public class ADC_A_C extends ADC_A_r {

    public ADC_A_C() {
        this.instr = 0x89;
        this.setRightRegister(Registers.C);
    }
}
