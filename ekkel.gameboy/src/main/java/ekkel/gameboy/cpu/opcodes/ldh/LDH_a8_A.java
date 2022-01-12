package ekkel.gameboy.cpu.opcodes.ldh;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.MemoryAddress;

/**
 * Put A into memory address $FF00+n
 */
// TODO: unit test is missing because it relies on other not implemented features
public class LDH_a8_A extends LDH_xx {

    public LDH_a8_A() {
        this.instr = 0xE0;
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.load(Registers.A).loadD8WithOffset(MemoryAddress.fromValue(0xFF00)).store().incPC();
        return 12;
    }
}
