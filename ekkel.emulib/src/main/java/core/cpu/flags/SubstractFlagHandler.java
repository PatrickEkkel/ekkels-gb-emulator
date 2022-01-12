package core.cpu.flags;

import core.cpu.Flags;
import core.mmu.Computable;

public class SubstractFlagHandler extends BaseFlagHandler {


    public SubstractFlagHandler(Computable flagValue) {
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

    public Computable handle() {
        super.handle();

        if(currentFlag == Flags.N) {
            popValues();
            pushValues();
            // TODO: implement
        }
        return flagsRegister;
    }

}
