package core.cpu.flags;

import core.mmu.Computable;

public class IncHalfCarryHandler extends HalfCarryFlagHandler{
    public IncHalfCarryHandler(Computable flagValue) {
        super(flagValue);
    }

    public Computable handle() {
        super.handle();

        if((this.c.getValue() & 0x0f) == 0x0) {
            set();
        }
        else {
            clear();
        }
        return flagsRegister;
    }
}
