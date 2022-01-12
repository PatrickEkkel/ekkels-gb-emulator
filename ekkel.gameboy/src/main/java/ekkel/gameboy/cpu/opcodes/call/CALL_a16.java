package ekkel.gameboy.cpu.opcodes.call;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.Computable;
import core.mmu.MemoryAddress;

import java.util.ArrayList;
import java.util.List;

public class CALL_a16 extends Opcode {

    public CALL_a16() {
        this.instr = 0xCD;
        this.length = 3;
        this.mnemonic.setMnemonic("CALL");
    }

    @Override
    public int[] toBinary() {
        MemoryAddress data = (MemoryAddress) this.getData();
        return new int[] {this.instr,data.getLowByte(),data.getHighByte()};
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        this.loadD16Computables();
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.loadD16().incPC().push(this.cpu.readRegister(Registers.PC)).store(Registers.PC);
        return 24;
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
}
