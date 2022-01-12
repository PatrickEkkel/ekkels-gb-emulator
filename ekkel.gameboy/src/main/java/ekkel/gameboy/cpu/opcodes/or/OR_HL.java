package ekkel.gameboy.cpu.opcodes.or;
;
import core.cpu.registers.Registers;

public class OR_HL extends OR_rr {
    public OR_HL() {
        this.instr = 0xB6;
        this.mnemonic.setMnemonic("OR");
        this.setLeftRegister(Registers.A);
        this.setRightRegister(Registers.HL);
    }
}
