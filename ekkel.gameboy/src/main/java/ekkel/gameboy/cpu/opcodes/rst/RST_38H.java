package ekkel.gameboy.cpu.opcodes.rst;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;

public class RST_38H extends Opcode {

    public RST_38H() {
        this.instr = 0xFF;
        this.mnemonic.setMnemonic("RST38H");
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        throw new NotImplementedException("RST 38H is not yet implemented");
    }
}
