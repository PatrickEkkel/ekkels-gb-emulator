package ekkel.gameboy.cpu.opcodes.ret;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class RET extends Opcode {

    public RET() {
        this.length = 1;
        this.instr = 0xC9;
        this.mnemonic.setMnemonic("RET");
    }

    @Override
    public int[] toBinary() {
        return new int[] { this.instr };
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.pop().store(Registers.PC);
        return 16;
    }

    @Override
    public String toString() {
        String result = String.format("%s",this.mnemonic.getMnemonic());
        return result;
    }
}
