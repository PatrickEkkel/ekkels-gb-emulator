package ekkel.gameboy.cpu.opcodes.misc;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class RRA extends Opcode {

    public RRA() {
        this.instr = 0x1F;
        this.mnemonic.setMnemonic("RRA");
    }

    @Override
    public int[] toBinary() {
        return new int[]{this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.load(Registers.A).carryLsb().shiftRight(1).rotate(Flags.C, 7).flags(0, 0, 0, Flags.C).store(Registers.A).incPC();
        return 4;
    }
}
