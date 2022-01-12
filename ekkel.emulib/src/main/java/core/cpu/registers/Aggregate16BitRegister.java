package core.cpu.registers;

import core.mmu.Computable;
import core.mmu.ComputableImpl;

public class Aggregate16BitRegister extends Register {

    private Register lsbRegister;
    private Register msbRegister;

    public Aggregate16BitRegister(Registers reg, Register msbRegister, Register lsbRegister) {
        super(0x000,16, reg);

        this.lsbRegister = lsbRegister;
        this.msbRegister = msbRegister;
    }

    @Override
    public int getValue() {
        return msbRegister.getValue() << 8 | lsbRegister.getValue();
    }

    @Override
    public void setValue(int value) {
        Computable register = new ComputableImpl(value);
        this.lsbRegister.setValue(register.getLowByte());
        this.msbRegister.setValue(register.getHighByte());
    }

    @Override
    public String toString() {

        String lsbResult = "00";
        if(this.lsbRegister.getValue() == 0) {

        }
        else {
            if(this.lsbRegister.getValue() < 0x10 && this.msbRegister.getValue() != 0x00) {
                lsbResult = "0" + Integer.toHexString(this.lsbRegister.getValue());
            }
            else {
                lsbResult = Integer.toHexString(this.lsbRegister.getValue());
            }
        }

        String msbResult = Integer.toHexString(this.msbRegister.getValue());

        if(this.msbRegister.getValue() == 0) {
            if(lsbResult.equals("00")) {
                return "0x0";
            }
            else {
                return String.format("0x%S",lsbResult);
            }

        }
        else if(this.msbRegister.getValue() == 0x0 && this.lsbRegister.getValue() == 0x0) {
            return String.format("0x0");
        }
        else {
            return String.format("0x%S%S",msbResult, lsbResult);
        }
    }

    @Override
    public int getLowByte() {
        return lsbRegister.getValue();
    }

    @Override
    public int getHighByte() {
        return msbRegister.getValue();
    }

    @Override
    public Computable inc() {
        int value = this.getValue();
        value += 1;
        this.setValue(value);
        return this;
    }

    @Override
    public Computable add(Computable v) {
        int value = this.getValue();
        value += v.getValue();
        this.setValue(value);
        return this;
    }

    @Override
    public Computable dec() {
        int value = this.getValue();
        value -= 1;
        this.setValue(value);
        return this;
    }

    @Override
    public boolean is16Bit() {
        return true;
    }

    @Override
    public boolean is8Bit() {
        return true;
    }
}
