package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.Computable;
import core.mmu.MemoryAddress;

import java.util.ArrayList;
import java.util.List;

public class LD_nn_d16 extends LD_xx {
    public LD_nn_d16() {
        this.length = 3;
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
        dsl.loadD16().store(register).incPC();
        return 12;
    }
    @Override
    public String toString() {
        String address = "nnnn";
        if(this.getData() != null) {
            address = this.getData().toString();
        }
        String result = String.format("%s %s %s",this.mnemonic.getMnemonic(), this.mnemonic.getRegister(),address);
        return result;
    }
}
