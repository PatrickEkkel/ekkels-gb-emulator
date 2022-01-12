package core.cpu.flags;

import core.cpu.Flags;
import core.mmu.Computable;

public class ZeroFlagHandler extends BaseFlagHandler {

    public ZeroFlagHandler(Computable flagValue) {
        super(flagValue);
    }

    @Override
    protected void popValues() {
       this.a = this.parameters.pop();
    }

    @Override
    protected void pushValues() {
        this.parameters.push(a);
    }

    @Override
    public Computable handle() {
        super.handle();
        if(currentFlag == Flags.Z) {
            popValues();
            if(this.a.getValue() == 0x00) {
                set();
            }
            else {
                clear();
            }
            pushValues();
        }
        return flagsRegister;
    }

}
