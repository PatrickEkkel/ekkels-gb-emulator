package core.cpu.flags;

import core.mmu.Computable;

public class MsbCarryHandler extends CarryFlagHandler {
    public MsbCarryHandler(Computable flagValue) {

        super(flagValue);
        disableSet();
    }

    @Override
    public Computable handle() {
        super.handle();

        //  check if msb bit is set
        if ((a.getValue() & 0x80) == 0x80) {
            set();
        } else {
            clear();
        }
        return flagsRegister;
    }
}
