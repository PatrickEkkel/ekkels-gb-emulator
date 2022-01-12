package core.cpu.flags;

import core.mmu.Computable;

public class SBCCarryHandler extends BaseFlagHandler {
    public SBCCarryHandler(Computable flagValue) {
        super(flagValue);
    }
    private boolean isCarry(Computable a, Computable b) {
        return a.getValue() - b.getValue() - 1 < 0x00;
    }

    @Override
    public Computable handle() {
        // ADC has computed a value with carry so operate on that
        if(this.parameters.size() == 4) {
            // value with carry, should be pushed back to the stack
            Computable d = this.parameters.pop();
            // value without carry, not important
            Computable c = this.parameters.pop();
            // Byte 1
            Computable b = this.parameters.pop();
            // Byte 2
            Computable a = this.parameters.pop();

            if(isCarry(b,a)) {
                set();
            }
            else {
                clear();
            }

            this.parameters.push(a);
            this.parameters.push(b);
            this.parameters.push(d);

            return flagsRegister;
        }
        else {
            /// default to standard Halfcarry behavior
            CarryFlagHandler carryFlagHandler = new CarryFlagHandler(this.flagValue);
            carryFlagHandler.setFlagsRegister(this.flagsRegister);
            carryFlagHandler.setCurrentFlag(this.currentFlag);
            carryFlagHandler.setParameters(this.parameters);
            carryFlagHandler.setCPU(this.cpu8Bit);
            return  carryFlagHandler.handle();
        }
    }
}
