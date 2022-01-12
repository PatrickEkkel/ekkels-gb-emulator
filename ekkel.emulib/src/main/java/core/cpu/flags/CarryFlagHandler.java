package core.cpu.flags;

import core.cpu.Flags;
import core.mmu.Computable;

public class CarryFlagHandler extends BaseFlagHandler {


    public CarryFlagHandler(Computable flagValue) {
        super(flagValue);
    }



    @Override
    protected void popValues() {
        c = this.parameters.pop();
        a = this.parameters.pop();
        b = this.parameters.pop();
    }

    @Override
    protected void pushValues() {
        this.parameters.push(b);
        this.parameters.push(a);
        this.parameters.push(c);
    }

    @Override
    public Computable handle() {
        super.handle();
        if (currentFlag == Flags.C) {
            this.popValues();
            if(!this.noexec) {
                if (isSubstractSet()) {
                    if (a.getValue() - b.getValue() < 0x00) {
                        set();
                    }
                    else {
                        clear();
                    }
                } else {
                    if (this.is16Bits()) {
                        if (a.getValue() + b.getValue() > 0xFFFF) {
                            set();
                        } else {
                            clear();
                        }
                    } else {
                        if (a.getValue() + b.getValue() > 0xFF) {
                            set();
                        }

                        else {
                            clear();
                        }
                    }
                }
            }
            this.pushValues();
        }
        return flagsRegister;
    }
}
