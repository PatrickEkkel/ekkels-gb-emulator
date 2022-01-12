package ekkel.gameboy.cpu.opcodes.misc;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;

public class CB extends Opcode {

    public CB() {
        this.instr = 0xCB;
        this.mnemonic.setMnemonic("CB");
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        // Do nothing
        return 4;
    }
}
