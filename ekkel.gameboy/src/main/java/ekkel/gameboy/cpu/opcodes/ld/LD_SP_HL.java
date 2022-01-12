package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class LD_SP_HL extends Opcode {

    public LD_SP_HL() {
        this.instr = 0xF9;
        this.mnemonic.setMnemonic("LD SP HL");
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.load(Registers.HL).store(Registers.SP).incPC();
        return 8;
    }
}
