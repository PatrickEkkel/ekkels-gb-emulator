package ekkel.gameboy.cpu.opcodes.ld;
import core.cpu.registers.Registers;

public class LD_A_C extends LD_r_r {

    public LD_A_C() {
        super();
        this.instr = 0x79;
        this.setLeftRegister(Registers.A);
        this.setRightRegister(Registers.C);
    }
}
