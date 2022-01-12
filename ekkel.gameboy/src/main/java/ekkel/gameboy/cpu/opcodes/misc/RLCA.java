package ekkel.gameboy.cpu.opcodes.misc;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class RLCA extends Opcode {

    public RLCA() {
        this.instr = 0x07;
        this.mnemonic.setMnemonic("RLCA");
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.load(Registers.A).carryMsb().shiftLeft(1).rotate(Flags.C,0).flags(0,0,0,Flags.C).store(Registers.A).incPC();
        return 4;
    }
}
