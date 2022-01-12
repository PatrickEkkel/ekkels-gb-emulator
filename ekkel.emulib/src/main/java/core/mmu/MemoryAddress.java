package core.mmu;

import core.cpu.registers.Register;

public class MemoryAddress extends ComputableImpl {
    private MemoryAddress(int value) {
        super(value);
    }

    public static MemoryAddress fromString(String value) {
        return new MemoryAddress(Integer.parseInt(value));
    }
    public static MemoryAddress fromValue(int value) {
        return new MemoryAddress(value);
    }
    public static MemoryAddress fromComputable(Computable value) { return  new MemoryAddress(value.getValue());}
    public static MemoryAddress fromHexString(String string) {
        return MemoryAddress.fromValue(Integer.decode(string));
    }
    public static MemoryAddress fromRegister(Register register) {
        return new MemoryAddress(register.getValue());
    }
    /**
     Combine 2 8 bit values in Little Endian
     **/
    public static MemoryAddress combine8BitValues(MemoryValue msb, MemoryValue lsb) {
        int lsb_value = lsb.getValue();
        int msb_value = msb.getValue();
        int combined_16bit_value = (msb_value & 0xFF) | (lsb_value & 0xFF) << 8;
        return new MemoryAddress(combined_16bit_value);

    }



    public int getValue() {
        return this.value;
    }

}
