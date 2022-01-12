package ekkel.gameboy.cpu.opcodes.ret;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;

public class RET_NZ extends Opcode {

    public RET_NZ() {
        this.instr = 0xC0;
        this.mnemonic.setMnemonic("RET NZ");
    }

    @Override
    public int[] toBinary() {
        return new int[]{this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        throw new NotImplementedException("RET NZ is not yet implemented");
    }
}
