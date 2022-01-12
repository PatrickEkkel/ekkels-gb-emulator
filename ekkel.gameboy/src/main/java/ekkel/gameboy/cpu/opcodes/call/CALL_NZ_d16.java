package ekkel.gameboy.cpu.opcodes.call;

import core.cpu.BranchCondition;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class CALL_NZ_d16 extends Opcode {

    public CALL_NZ_d16() {
        this.instr = 0xC4;
        this.mnemonic.setMnemonic("CALLNZ");
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        this.loadD16Computables();;
    }

    @Override
    public String toString() {
        String address = "nnnn";
        if (this.getData() != null) {
            address = this.getData().toString();
        }
        String result = String.format("%s %s", this.mnemonic.getMnemonic(), address);
        return result;
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.loadD16().exprIf(BranchCondition.NZ,Registers.F).incPC().push(this.cpu.readRegister(Registers.PC)).store(Registers.PC).exprElse().incPC();
        return dsl.hasBranched() ? 24 : 12;
    }
}
