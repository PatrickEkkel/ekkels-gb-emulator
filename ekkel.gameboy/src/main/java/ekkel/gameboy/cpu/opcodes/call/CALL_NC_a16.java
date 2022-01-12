package ekkel.gameboy.cpu.opcodes.call;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;

public class CALL_NC_a16 extends Opcode {

    public CALL_NC_a16() {
        this.instr = 0xD4;
        this.mnemonic.setMnemonic("CALLNC");
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        this.loadD16Computables();
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        throw new NotImplementedException("CALL NC is not yet implemented");
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
