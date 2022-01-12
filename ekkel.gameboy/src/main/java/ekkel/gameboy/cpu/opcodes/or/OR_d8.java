package ekkel.gameboy.cpu.opcodes.or;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.MemoryAddress;

public class OR_d8 extends Opcode {

    public OR_d8() {
        this.instr = 0xF6;
        this.mnemonic.setMnemonic("OR");
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
        dsl.loadD8().load(Registers.A).bitwiseOr().flags(Flags.Z,0,0,0).store(Registers.A).incPC();
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
