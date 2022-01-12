package ekkel.gameboy.cpu.opcodes.branch;

import core.cpu.BranchCondition;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

/**
 * Abstract Base class for all JR Conditional Jumps
 */
public abstract class JR_c_r8 extends Opcode {

    private BranchCondition condition;

    protected void setBranchCondition(BranchCondition condition) {
        this.condition = condition;
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        this.loadS8Computables();
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.peekS8()
                .exprIf(condition, Registers.F)
                .load(Registers.PC).add(2)
                .add().store(Registers.PC).exprElse()
                .load(Registers.PC).add(2).store(Registers.PC);
        return dsl.hasBranched() ? 12 : 8;
    }

    @Override
    public int[] toBinary() {
        return new int[]{this.instr, this.getData().getLowByte()};
    }


    @Override
    public String toString() {
        String address = "s8";
        if (this.getData() != null) {
            address = this.getData().toString();
        }
        String result = String.format("%s %s", this.mnemonic.getMnemonic(), address);
        return result;
    }
}
