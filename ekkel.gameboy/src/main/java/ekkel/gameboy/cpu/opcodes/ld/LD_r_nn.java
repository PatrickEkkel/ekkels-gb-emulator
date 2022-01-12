package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.MemoryAddress;

public class LD_r_nn  extends LD_xx {

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {

        dsl.loadA16().loadIV16().store(Registers.A).incPC();

        return 16;
    }

    @Override
    public int[] toBinary() {
        MemoryAddress address = (MemoryAddress) this.getData();
        return new int[] {this.instr,address.getLowByte(),address.getHighByte()};
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
        String result = String.format("%s %s %s",this.mnemonic.getMnemonic(), this.mnemonic.getRegister(), address);
        return result;
    }
}
