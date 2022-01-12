package ekkel.gameboy.cpu.opcodes.xor;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.MemoryAddress;

public class XOR_d8 extends Opcode {

    public XOR_d8() {
        this.instr = 0xEE;
        this.mnemonic.setMnemonic("XOR");
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
        this.dsl.loadD8().load(Registers.A).xor().flags(Flags.Z,0,0,0).store(Registers.A).incPC();
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
