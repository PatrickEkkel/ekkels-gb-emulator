package ekkel.gameboy.cpu.opcodes.adc;

import core.cpu.registers.Registers;

public class ADC_A_B extends ADC_A_r {

    public ADC_A_B() {
        this.instr = 0x88;
        this.setRightRegister(Registers.B);
    }

}
