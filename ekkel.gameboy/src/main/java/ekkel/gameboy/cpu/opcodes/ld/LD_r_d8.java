package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.Computable;
import core.mmu.MemoryAddress;

/**
 * Put 8-bit immediate value into A.
 */
public class LD_r_d8 extends LD_xx {
   // private Computable data;
    public LD_r_d8() {
        this.mnemonic.setMnemonic("LD");
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.loadD8().storeRD8(register).incPC();
        return 8;
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        loadD8Computables();
    }

    @Override
    public int[] toBinary() {
        // It should be a memory address
        MemoryAddress data = (MemoryAddress) this.getData();
        return new int[] {this.instr,data.getLowByte()};
    }

    @Override
    public String toString() {

        String data = "nn";

        if(this.getData() != null) {
           data = this.getData().toString();
        }
        String result = String.format("%s %s %s",this.mnemonic.getMnemonic(), this.mnemonic.getRegister(), data);
        return result;
    }
}
