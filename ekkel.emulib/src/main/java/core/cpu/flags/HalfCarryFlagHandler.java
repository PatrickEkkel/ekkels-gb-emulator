package core.cpu.flags;

import core.cpu.Flags;
import core.cpu.registers.Register;
import core.mmu.Computable;
import core.mmu.ComputableImpl;

public class HalfCarryFlagHandler extends BaseFlagHandler {
    public HalfCarryFlagHandler(Computable flagValue) {
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

    private boolean isHalfCarry() {

        if (isSubstractSet()) {
            return (((a.getValue() & 0xF) - (b.getValue() & 0xF)) & 0x10) == 0x10;
        } else {
            return (((a.getValue() & 0xF) + (b.getValue() & 0xF)) & 0x10) == 0x10;
        }
    }

    private void handleHalfCarry() {
        if (this.isHalfCarry()) {
            set();
        } else {
            clear();
        }
    }

    public Computable handle() {
        super.handle();

        if (currentFlag == Flags.H) {
            popValues();
            if (!noexec) {
                this.handleHalfCarry();
            }
            pushValues();
        }

        return flagsRegister;
    }
}
