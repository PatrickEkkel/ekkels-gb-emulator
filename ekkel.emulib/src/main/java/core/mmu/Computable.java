package core.mmu;

public interface Computable {
    int getValue();
    int getUnsignedValue();
    void setValue(int value);
    Computable convertToSigned();

    Computable newInstance();

    Computable inc();
    Computable dec();

    Computable xor(Computable v);

    Computable shiftRight(int position);

    Computable shiftLeft(int position);

    Computable set(Computable c);

    void add(int value);
    Computable or(Computable v);
    boolean isZero();
    Computable add(Computable v);
    void invert();
    Computable and(Computable v);
    Computable sub(Computable v);

    boolean getBit(int p);

    Computable setBit(int p,int v);

    boolean is16Bit();

    boolean is8Bit();
    int getHighByte();
    int getLowByte();
}
