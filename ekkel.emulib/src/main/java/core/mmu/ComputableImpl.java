package core.mmu;

import java.util.Objects;

public class ComputableImpl implements Computable {
    protected int value;

    public ComputableImpl() {

    }

    public ComputableImpl(int value) {
        this.value = value;
    }

    @Override
    public int getValue() {
        return this.value;
    }

    @Override
    public int getUnsignedValue() {
        if(this.value < 0) {
            return this.getValue() & 0xFF;
        }
        else {
            return this.getValue();
        }
    }

    @Override
    public void setValue(int value) {
        this.value = value;
    }

    @Override
    public Computable convertToSigned() {
        int result = this.value;
        if ((result & 0x80) > 0) {
            result = (this.value + -0xFF) - 1;
        }
        this.value = result;
        return this;
    }

    @Override
    public Computable newInstance() {
        return new ComputableImpl();
    }

    @Override
    public Computable inc() {
        int result = this.value;
        result += 1;
        Computable computable = this.newInstance();
        computable.setValue(result);
        return computable;
    }

    @Override
    public Computable dec() {
        int result = this.value - 1;
        return new ComputableImpl(result);
    }

    @Override
    public Computable xor(Computable v) {
        int result = this.getUnsignedValue() ^ v.getUnsignedValue();
        return new ComputableImpl(result);
    }

    @Override
    public Computable shiftRight(int position) {
        int result = this.value;

        result = result >> position;
        return new ComputableImpl(result);

    }

    @Override
    // NOTE: Left shift does not seem to respect the boundaries of 8-bit,
    // NOTE: i suspect this method will introduce some unwanted behaviour
    public Computable shiftLeft(int position) {
        int result = this.value;
        result = result << position;
        return new ComputableImpl(result);
    }

    public static Computable fromValue(int val) {
        return new ComputableImpl(val);
    }

    @Override
    public Computable set(Computable c) {
        this.setValue(c.getValue());
        return this;
    }

    public int getHighByte() {
        return (this.value >> 8) & 0xFF;
    }

    public int getLowByte() {
        return value & 0xFF;
    }

    @Override
    public void add(int value) {
        this.value += value;
    }

    // TODO: create a new computable object instead of reusing the old one, do this for all operations
    @Override
    public Computable or(Computable v) {
        int newValue = this.value | v.getValue();
        return new ComputableImpl(newValue);
    }

    @Override
    public boolean isZero() {
        return this.value == 0x00;
    }


    @Override
    public Computable add(Computable v) {
        int result = this.getValue();
        result += v.getValue();
        if(this.is8Bit()) {
                result &= 0xFF;
        }
        return new ComputableImpl(result);
    }

    @Override
    public void invert() {
        this.value = ~this.value;
    }

    @Override
    public Computable and(Computable v) {
        int result = this.value & v.getValue();

        return new ComputableImpl(result);
    }

    @Override
    public Computable sub(Computable v) {
        int result = this.value;
        result -= v.getValue();
        if(this.is8Bit()) {
            result &= 0xFF;
        }
        // TODO: could get a bit crazy when substracting signed values
        return new ComputableImpl(result);
    }

    @Override
    public boolean getBit(int p) {
        int result = (this.value >> p) & 0x01;
        return result == 0x01;
    }

    @Override
    public Computable setBit(int p, int v) {
        // Safeguarding against bogus values
        if (v > 0x01) {
            v = 0x01;
        } else if (v < 0x00) {
            v = 0x00;
        }
        int result = v << p;
        result = this.value | result;
        return new ComputableImpl(result);
    }

    @Override
    public boolean is16Bit() {
        return this.value > 256;
    }

    @Override
    public boolean is8Bit() {
        return this.value <= 0xFF;
    }

    @Override
    public String toString() {
        return String.format("0x%S", Integer.toHexString(this.value));
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        ComputableImpl that = (ComputableImpl) o;
        return value == that.value;
    }

    @Override
    public int hashCode() {
        return Objects.hash(value);
    }
}
