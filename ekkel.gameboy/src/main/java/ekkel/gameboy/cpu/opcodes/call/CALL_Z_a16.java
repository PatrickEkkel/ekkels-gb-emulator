package ekkel.gameboy.cpu.opcodes.call;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.MemoryAddress;

public class CALL_Z_a16 extends Opcode {

    public CALL_Z_a16() {
        this.instr = 0xCC;
        this.mnemonic.setMnemonic("CALLZ");
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
        throw new NotImplementedException("Opcode CALL Z is not implemented");
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
