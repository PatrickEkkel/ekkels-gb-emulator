package ekkel.gameboy.cpu.opcodes.add;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class ADD_A_d8  extends Opcode {

    public ADD_A_d8() {
        this.mnemonic.setMnemonic("ADD A");
        this.instr = 0xC6;
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
        dsl.loadD8().load(Registers.A).add().flags(Flags.Z,0,Flags.H,Flags.C).store(Registers.A).incPC();
        return 8;
    }

    @Override
    public String toString() {
        String data = "nn";
        if(this.getData() != null) {
            data = this.getData().toString();
        }
        return String.format("%s %s",this.mnemonic.getMnemonic(), data);
    }
}
