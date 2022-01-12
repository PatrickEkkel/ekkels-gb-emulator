package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class LD_HL_SP_add_r8 extends Opcode {

    public LD_HL_SP_add_r8() {
        this.instr = 0xF8;
        this.mnemonic.setMnemonic("LD HL SP+");
    }

    @Override
    public int[] toBinary() {
        return new int[] { this.instr,this.getData().getLowByte()};
    }
    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        loadS8Computables();
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.loadS8().load(Registers.SP).add().flags(0, 0, Flags.H,Flags.C).store(Registers.HL).incPC();
        return 12;
    }

    @Override
    public String toString() {
        String address = "nn";
        if(this.getData() != null) {
            address = this.getData().toString();
        }
        return String.format("%s %s ",this.mnemonic.getMnemonic(), address);
    }
}
