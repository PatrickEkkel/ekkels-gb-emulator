package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.MemoryAddress;

public class LD_a16_SP extends Opcode  {

    public LD_a16_SP() {
        this.instr = 0x08;
        this.mnemonic.setMnemonic("LD");
        this.mnemonic.setRegister("SP");
    }

    @Override
    public int[] toBinary() {
        MemoryAddress address = (MemoryAddress) this.getData();
        return new int[] {this.instr,address.getLowByte(),address.getHighByte()};
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        this.loadD16Computables();
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.loadA16().load(Registers.SP).storeA16().incPC();
        return 20;
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
