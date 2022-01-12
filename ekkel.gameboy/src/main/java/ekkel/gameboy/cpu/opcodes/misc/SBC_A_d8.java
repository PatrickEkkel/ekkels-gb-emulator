package ekkel.gameboy.cpu.opcodes.misc;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.MemoryAddress;

public class SBC_A_d8 extends Opcode {

    public SBC_A_d8() {
        this.instr = 0xDE;
        this.mnemonic.setMnemonic("SBC A");
    }

    @Override
    public int[] toBinary() {
        // It should be a memory address
        MemoryAddress data = (MemoryAddress) this.getData();
        return new int[] {this.instr,data.getLowByte()};
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        dsl.loadD8();
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.loadD8().load(Registers.A).sub().sbc().flags(Flags.Z,1,Flags.H,Flags.C).store(Registers.A).incPC();
         return 8;
    }

    @Override
    public String toString() {

        String data = "nn";

        if(this.getData() != null) {
            data = this.getData().toString();
        }
        String result = String.format("%s %s",this.mnemonic.getMnemonic(), data);
        return result;
    }
}
