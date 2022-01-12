package ekkel.gameboy.cpu.opcodes.misc;

import core.cpu.opcodes.Opcode;
import core.cpu.registers.Registers;

/**
 * Do Nothing for 4 cycles 0x00
 */
public class NOP extends Opcode {

    public NOP() {
        super();
        this.length = 1;
        this.instr = 0x00;
        this.mnemonic.setMnemonic("NOP");
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public int execute() {
        dsl.incPC();
        return 4;
    }
}
