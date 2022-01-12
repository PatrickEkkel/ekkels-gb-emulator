package ekkel.gameboy.cpu.opcodes.branch;

import core.cpu.BranchCondition;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class JR_Z_r8 extends Opcode {

    public JR_Z_r8() {
        this.instr = 0x28;
        this.mnemonic.setMnemonic("JRZ");
    }

    @Override
    public int[] toBinary() {
        return new int[] { this.instr, this.getData().getLowByte() };
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        // add the length of the opcode (2) to the length of the signed value to get to the relative jump position
        dsl.peekS8()
                .exprIf(BranchCondition.Z,Registers.F)
                .load(Registers.PC).add().add(2)
                .store(Registers.PC).exprElse().load(Registers.PC).add(2).store(Registers.PC);
        return dsl.hasBranched() ? 12 : 8;
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        this.loadS8Computables();
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
