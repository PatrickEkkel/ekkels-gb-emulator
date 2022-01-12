package core.cpu.flags.utils;

import core.cpu.CPU;
import core.cpu.flags.utils.FlagUtils;
import core.cpu.registers.Register;
import core.mmu.Computable;

public class FlagsHelper {

    private CPU cpu;
    private Register flagsRegister;
    public FlagsHelper(CPU cpu, Register flagsRegister) {
        this.cpu = cpu;
        this.flagsRegister = flagsRegister;
    }

    public boolean isZ() {
        return FlagUtils.isFlagSet(this.cpu.getZeroFlag(),this.flagsRegister);
    }

    public boolean isH() {
        return FlagUtils.isFlagSet(this.cpu.getHalfCarryFlag(),this.flagsRegister);
    }

    public boolean isC() {
        return FlagUtils.isFlagSet(this.cpu.getCarryFlag(),this.flagsRegister);
    }
    public boolean isN() {
        return FlagUtils.isFlagSet(this.cpu.getSubstractFlag(),this.flagsRegister);
    }


    public Computable getC() {
        return this.cpu.getCarryFlag();
    }

    public void setC() {
        FlagUtils.setFlag(this.flagsRegister,this.cpu.getCarryFlag());
    }

}
