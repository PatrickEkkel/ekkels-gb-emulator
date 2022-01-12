package ekkel.gameboy.cpu.opcodes.ldh;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.MemoryAddress;

public class LDH_A_a8  extends LDH_xx {

    public LDH_A_a8() {
        this.instr = 0xF0;
       // this.mnemonic.setMnemonic("LDH (0xFF00)");
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.loadD8WithOffset(MemoryAddress.fromValue(0xFF00)).loadIV16().store(Registers.A).incPC();
        return 12;
    }


}
