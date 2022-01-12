package ekkel.gameboy.cpu.opcodes.cp;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.Computable;
import core.mmu.MemoryAddress;

import java.util.ArrayList;
import java.util.List;

public class CP_d8  extends Opcode {

    public CP_d8() {
        this.mnemonic.setMnemonic("CP");
        this.instr = 0xFE;
    }

    @Override
    public int[] toBinary() {
        // It should be a memory address
        MemoryAddress data = (MemoryAddress) this.getData();
        return new int[] {this.instr,data.getLowByte()};
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        this.loadD8Computables();
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
         dsl.loadD8().load(Registers.A).sub().flags(Flags.Z,1,Flags.H,Flags.C).incPC();
         return  8;
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
