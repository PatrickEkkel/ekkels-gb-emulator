package ekkel.gameboy.cpu.opcodes.sub;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class SUB_A_d8 extends Opcode {

    public SUB_A_d8() {
        this.instr = 0xD6;
        this.mnemonic.setMnemonic("SUB A");
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        loadD8Computables();
    }

    @Override
    public int[] toBinary() {
        return new int[]{this.instr, this.getData().getLowByte()};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.loadD8().load(Registers.A).sub().flags(Flags.Z, 1, Flags.H, Flags.C).store(Registers.A).incPC();
        return 8;
    }

    @Override
    public String toString() {
        String data = "nn";
        if (this.getData() != null) {
            data = this.getData().toString();
        }
        return String.format("%s %s", this.mnemonic.getMnemonic(), data);
    }
}
