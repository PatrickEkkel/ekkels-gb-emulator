package core.cpu;

import core.cpu.registers.Register;
import core.cpu.registers.Registers;
import core.mmu.Computable;

public interface CPU8Bit {
    Register readRegister(Registers key);
    void writeRegister(Registers key, Computable value);
    Stack getStack();
    Computable getZeroFlag();
    Computable getSubstractFlag();
    Computable getHalfCarryFlag();
    Computable getCarryFlag();
    void setFlag(Computable flag);

}
