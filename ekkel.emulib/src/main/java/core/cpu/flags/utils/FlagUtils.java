package core.cpu.flags.utils;

import core.cpu.registers.Register;
import core.mmu.Computable;
import core.mmu.ComputableImpl;

public class FlagUtils {

    public static boolean isFlagSet(Computable flag, Computable register) {
       return  register.and(flag).equals(flag);
    }

    public static boolean isFlagSet(int value, Computable flag, Computable register) {
        return ComputableImpl.fromValue(value).and(flag).equals(flag);
    }

    public static void setFlag(Register flagsRegister, Computable flagValue) {
        flagsRegister.setValue(flagsRegister.or(flagValue).getValue());
    }
}
