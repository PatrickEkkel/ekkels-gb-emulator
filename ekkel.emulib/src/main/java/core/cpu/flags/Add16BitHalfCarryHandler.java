package core.cpu.flags;

import core.mmu.Computable;

public class Add16BitHalfCarryHandler extends HalfCarryFlagHandler {
    public Add16BitHalfCarryHandler(Computable flagValue) {
        super(flagValue);
        this.disableSet();
    }
    private boolean isHalfCarry() {

        return (((a.getValue() & 0xFFF) + (b.getValue() & 0xFFF)) & 0x1000) == 0x1000;
    }

    @Override
    public Computable handle() {
        super.handle();

        if(this.isHalfCarry()) {
            set();
        }
        else {
            clear();
        }

        return this.flagsRegister;
    }
}
