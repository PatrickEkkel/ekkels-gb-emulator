package ekkel.gameboy.cpu.opcodes.misc;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;

public class CPL extends Opcode {

    public CPL() {
        this.instr = 0x2F;
        this.mnemonic.setMnemonic("CPL");
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        throw new NotImplementedException("CPL is not yet implemented");
    }
}
