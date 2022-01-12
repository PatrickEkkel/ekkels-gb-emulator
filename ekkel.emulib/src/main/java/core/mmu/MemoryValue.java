package core.mmu;

public class MemoryValue extends ComputableImpl{
    private MemoryValue(int value) {
        super(value);
        this.value = value;
    }
    private MemoryValue(byte value) {
        super(Byte.toUnsignedInt(value));
    }

    public static MemoryValue empty() {
        return new MemoryValue(0xFFFF);
    }
    public static MemoryValue fromValue(int value) {
        return new MemoryValue(value);
    }
    public static MemoryValue fromComputable(Computable computable) { return new MemoryValue(computable.getValue()); }
    public static MemoryValue fromByte(byte value) {
        return new MemoryValue(value);
    }

    public MemoryValue getLowByteAsComputable() {
        return MemoryValue.fromValue(this.getLowByte());
    }
    public MemoryValue getHighByteAsComputable() {
        return MemoryValue.fromValue(this.getHighByte());
    }

    public int getValue() {
        return this.value;
    }


}
