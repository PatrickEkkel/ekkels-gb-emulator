package ekkel.gameboy.cpu.opcodes.misc;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;

public class SCF extends Opcode {

    public SCF() {
        this.instr = 0x37;
        this.mnemonic.setMnemonic("SCF");
    }

    @Override
    public int[] toBinary() {
        return new int[] { this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        throw new NotImplementedException("SCF is not yet implemented");
    }
}
