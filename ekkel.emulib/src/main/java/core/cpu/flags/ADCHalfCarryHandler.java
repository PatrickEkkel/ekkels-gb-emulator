package core.cpu.flags;

import core.mmu.Computable;

public class ADCHalfCarryHandler extends BaseFlagHandler{
    public ADCHalfCarryHandler(Computable flagValue) {
        super(flagValue);
    }
    private boolean isHalfCarry(Computable a, Computable b) {
        return (((a.getValue() & 0xF) + (b.getValue() & 0xF) + 1) & 0x10) == 0x10;
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

           if(isHalfCarry(a,b)) {
               set();
           }
           else {
               clear();
           }

           this.parameters.push(a);
           this.parameters.push(b);
           this.parameters.push(c);
           this.parameters.push(d);

            return flagsRegister;
        }
        else {
            /// default to standard Halfcarry behavior
            return new HalfCarryFlagHandler(this.flagValue).handle();
        }
    }
}
