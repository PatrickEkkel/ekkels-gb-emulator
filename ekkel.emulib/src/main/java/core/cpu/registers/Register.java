package core.cpu.registers;

import core.mmu.Computable;
import core.mmu.ComputableImpl;

public class  Register extends ComputableImpl {
    int bits = 0;
    private Registers reg;

    public Register(int value, int bits, Registers reg) {
        super(value);
        this.bits = bits;
        this.reg = reg;
    }

    public int getBits() {
        return this.bits;
    }

    @Override
    public Computable newInstance() {
        return new Register(this.value,this.bits,this.reg);
    }


    @Override
    public Computable add(Computable v) {
        int result = this.value;
        result += v.getValue();

        if(this.bits == 8)  {
            result &= 0xFF;
        }
        return new ComputableImpl(result);
    }

    @Override
    public Computable sub(Computable v) {
        int result = this.value;
        result -= v.getValue();

        if(this.bits == 8 && result < 0) {

            result = v.getValue() - this.value;
            result = (0xFF + 1) - result;
        }

        return new ComputableImpl(result);
    }

    public void setValue(int value) {

        if(this.bits ==  8 && value > 0xFF) {
            this.value = 0x0;
            return;
        }
        else if(this.bits == 16 && value > 0xFFFF) {
            this.value = 0x0;
            return;
        }
        this.value = value;
    }

    @Override
    public boolean is16Bit() {
        return this.bits == 16;
    }

    public boolean is8Bit() {
        return this.bits == 8;
    }
}
