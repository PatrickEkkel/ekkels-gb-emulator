package core.cpu.flags;

import core.cpu.CPU8Bit;
import core.cpu.registers.Register;
import core.mmu.Computable;

import java.util.Stack;

public class BaseFlagHandler {


    protected Computable flagsRegister;
    protected Computable flagValue;
    protected int currentFlag;

    protected CPU8Bit cpu8Bit;

    protected Stack<Computable> parameters;
    protected Computable a;
    protected Computable b;
    protected Computable c;
    protected boolean noexec = false;

    public void disableSet() {
        this.noexec = true;
    }

    public BaseFlagHandler(Computable flagValue) {
        this.flagValue = flagValue;
    }

    public void setFlagsRegister(Computable flagsRegister) {
        this.flagsRegister = flagsRegister;
    }

    public void setCurrentFlag(int currentFlag) {
        this.currentFlag = currentFlag;
    }


    public void setCPU(CPU8Bit cpu8Bit) {
        this.cpu8Bit = cpu8Bit;
    }

    public void set() {
        flagsRegister.setValue(flagsRegister.or(flagValue).getValue());
    }

    public void clear() {
        flagValue.invert();
        Computable result = flagValue.and(flagsRegister);
        flagsRegister.setValue(result.getValue());
    }

    public void setParameters(Stack<Computable> parameters) {
        this.parameters = parameters;
    }

    public boolean isSubstractSet() {
        Computable substractFlag = this.cpu8Bit.getSubstractFlag();
        return this.flagsRegister.and(substractFlag).getValue() == substractFlag.getValue();
    }

    protected boolean is16Bits() {

        if (this.a instanceof Register && this.b instanceof Register) {
            Register localA = (Register) a;
            Register localB = (Register) b;

            return localA.getBits() == 16 && localB.getBits() == 16;
        }
        return false;
    }

    private boolean doNegativeHalfCary(Computable a, Computable b) {
        return false;
    }

    private boolean doPositiveHalfCarry(Computable a, Computable b) {
        return false;
    }

    protected void popValues() {

    }

    protected void pushValues() {

    }

    public Computable handle() {
        if (this.currentFlag == 1) {
            this.set();
        } else if (this.currentFlag == 0) {
            this.clear();
        }
        return flagsRegister;
    }
}
