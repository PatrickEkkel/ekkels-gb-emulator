package ekkel.gameboy.cpu.opcodes.add;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class ADD_SP_r8 extends Opcode {

    public ADD_SP_r8() {
        this.instr = 0xE8;
        this.mnemonic.setMnemonic("ADD SP");
    }


    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        loadD8Computables();
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr,this.getData().getLowByte()};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.loadS8().load(Registers.SP).add().flags(0,0, Flags.H,Flags.C).store(Registers.SP).incPC();
        return 16;
    }

    @Override
    public String toString() {
        String data = "s8";
        if(this.getData() != null) {
            data = this.getData().toString();
        }
        return String.format("%s %s",this.mnemonic.getMnemonic(), data);
    }
}
