package core.cpu;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Register;
import core.cpu.registers.Registers;
import core.mmu.*;

public class Stack {

    private MMU mmuImpl;
    private CPU cpu;
    public Stack(MMU mmuImpl, CPU cpu) {
        this.mmuImpl = mmuImpl;
        this.cpu = cpu;
    }

    private void incSP() {
        Register SP = this.cpu.reg.get(Registers.SP);
        Computable value = SP.inc();
        SP.set(value);
    }
    private void decSP() {
        Register SP = this.cpu.reg.get(Registers.SP);
        Computable value = SP.dec();
        SP.set(value);
        // this.cpu.writeRegister(Registers.SP,getSP().dec());
        // this.cpu.reg.get(Registers.SP).dec();
    }
    private MemoryAddress getSP() {
        return MemoryAddress.fromComputable(this.cpu.reg.get(Registers.SP));
    }

    public void push(Computable c) throws NotImplementedException {
        this.mmuImpl.write(getSP(), MemoryValue.fromComputable(c));
        this.decSP();
    }
    public Computable pop() throws NotImplementedException, IllegalAccessException {
        this.incSP();
        return this.mmuImpl.read(getSP());
    }

}
