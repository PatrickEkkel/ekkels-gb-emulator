package ekkel.gameboy.cpu.opcodes.ret;

import core.cpu.BranchCondition;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class RET_NC extends Opcode {

    public RET_NC() {
        this.instr = 0xD0;
        this.mnemonic.setMnemonic("RET NC");
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.exprIf(BranchCondition.NC, Registers.F).pop().store(Registers.PC).exprElse().incPC();
        return dsl.hasBranched() ? 20 : 8;
    }
}
