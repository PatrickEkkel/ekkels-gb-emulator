package ekkel.gameboy.cpu.opcodes.branch;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class JP_HL extends Opcode {

    public JP_HL() {
        this.mnemonic.setMnemonic("JP HL");
        this.instr = 0xE9;

    }


    @Override
    public int[] toBinary() {
        return new int[] {this.instr };
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.load(Registers.HL).store(Registers.PC);
        return 4;
    }

    @Override
    public String toString() {
        return this.mnemonic.getMnemonic();
    }
}
