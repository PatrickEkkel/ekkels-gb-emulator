package ekkel.gameboy.cpu.opcodes.add;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class ADD_HL_SP extends ADD_rr_rr {

    public ADD_HL_SP() {
        this.instr = 0x39;
        this.setLeftRegister(Registers.HL);
        this.setRightRegister(Registers.SP);
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        return super.execute();
    }
}
