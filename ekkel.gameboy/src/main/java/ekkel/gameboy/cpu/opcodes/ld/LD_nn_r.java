package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.MemoryAddress;

public class LD_nn_r  extends LD_xx {
    public LD_nn_r() {
        this.length = 3;
    }

    @Override
    public int[] toBinary() {
        MemoryAddress address = (MemoryAddress) this.getData();
        return new int[] {this.instr,address.getLowByte(),address.getHighByte()};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.loadA16().load(register).storeA8().incPC();
        return 16;
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        loadD16Computables();
    }

    @Override
    public String toString() {
        String address = "nnnn";
        if(this.getData() != null) {
            address = this.getData().toString();
        }
        String result = String.format("%s %s %s",this.mnemonic.getMnemonic(), address, this.mnemonic.getRegister());
        return result;
    }
}
