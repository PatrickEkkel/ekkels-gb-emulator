package core.cpu.flags;

import core.mmu.Computable;
import core.mmu.ComputableImpl;

public class AddD16toS8CarryHandler extends CarryFlagHandler {
    public AddD16toS8CarryHandler(Computable flagValue) {
        super(flagValue);
        this.disableSet();
    }

    @Override
    public Computable handle() {
        super.handle();

        Computable la = new ComputableImpl(a.getLowByte());
        Computable lb = new ComputableImpl(b.getLowByte());

        Computable ha = new ComputableImpl(a.getLowByte());
        Computable hb = new ComputableImpl(b.getLowByte());

        if(la.getValue() + lb.getValue() > 0xFF)
        {
            set();
        }

        else if(ha.getValue() + hb.getValue() > 0xFF)
        {
            set();
        }
        else {
            clear();
        }
        /*
        if (a.getUnsignedValue() + b.getUnsignedValue() > 0xFFFF) {
            set();
        } else {
            clear();
        } */

        return flagsRegister;
    }
}
