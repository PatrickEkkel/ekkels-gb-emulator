package core.cpu.flags;

import core.mmu.Computable;

public class SBCHalfCarryHandler extends BaseFlagHandler{

    public SBCHalfCarryHandler(Computable flagValue) {
        super(flagValue);
    }

    private boolean isHalfCarry(Computable a, Computable b) {
      // int res = a.getValue() - b.getValue() - 1;
      //  return ((a.getValue() ^ b.getValue() ^ (res & 0xff)) & (1 << 4)) != 0;
        return (((a.getValue() & 0xF) - (b.getValue() & 0xF) - 1) & 0x10) == 0x10;
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

            if(isHalfCarry(b,a)) {
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
            HalfCarryFlagHandler halfCarryFlagHandler = new HalfCarryFlagHandler(this.flagValue);
            halfCarryFlagHandler.setFlagsRegister(this.flagsRegister);
            halfCarryFlagHandler.setCurrentFlag(this.currentFlag);
            halfCarryFlagHandler.setParameters(this.parameters);
            halfCarryFlagHandler.setCPU(this.cpu8Bit);
            return halfCarryFlagHandler.handle();
        }
    }
}
