package core.cpu.flags;

import core.mmu.Computable;

public class LsbCarryHandler extends CarryFlagHandler {
    public LsbCarryHandler(Computable flagValue) {

        super(flagValue);
        disableSet();
    }

    @Override
    public Computable handle() {
        super.handle();
        //  check if lsb bit is set
        if((a.getValue() & 0x01) == 0x01) {
            set();
        }
        else {
            clear();
        }
        return flagsRegister;
    }
}
