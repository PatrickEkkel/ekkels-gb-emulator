package ekkel.gameboy.cpu.opcodes.ret;

import core.cpu.BranchCondition;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class RET_Z extends Opcode {

    public RET_Z() {
        this.instr = 0xC8;
        this.mnemonic.setMnemonic("RET Z");
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.exprIf(BranchCondition.Z, Registers.F).pop().store(Registers.PC).exprElse().incPC();
        return dsl.hasBranched() ? 20 : 8;
    }
}
