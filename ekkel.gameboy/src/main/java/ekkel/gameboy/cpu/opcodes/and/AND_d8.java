package ekkel.gameboy.cpu.opcodes.and;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class AND_d8 extends Opcode {

    public AND_d8() {
        this.mnemonic.setMnemonic("AND");
        this.instr = 0xE6;
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr,this.getData().getLowByte()};
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        loadD8Computables();
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.loadD8().load(Registers.A).bitwiseAnd().flags(Flags.Z,0,1,0).store(Registers.A).incPC();
        return 8;
    }

    @Override
    public String toString() {
        String data = "nn";
        if(this.getData() != null) {
            data = this.getData().toString();
        }
        return String.format("%s %s", this.mnemonic.getMnemonic(),data);
    }
}
