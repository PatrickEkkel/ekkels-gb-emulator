package core.cpu.registers.utils;

import core.cpu.CPU;
import core.cpu.registers.Register;
import core.cpu.registers.Registers;

/**
 * A collection of methods that make working with Register values a little less tedious
 */
public class RegisterHelper {

    private CPU cpu;
    public RegisterHelper(CPU cpu) {
        this.cpu = cpu;
    }

    /**
     * do a primitive int comparison from the values of 2 registers
     */
    public boolean isEqual(Registers a, Registers b) {

        Register left = this.cpu.readRegister(a);
        Register right = this.cpu.readRegister(b);
        return left.getValue() == right.getValue();
    }

    /**
     * Compare register value with int
     */
    public boolean isEqual(Registers a, int b) {
        return this.toInt(a) == b;
    }

    /**
     * Get value as Int value
     */
    public int toInt(Registers a) {
       return this.cpu.readRegister(a).getValue();
    }

    /**
     * Set Register value
     */
    public void setRegister(Registers a, int value) {
        this.cpu.readRegister(a).setValue(value);
    }

    public Register getRegister(Registers a) {
        return this.cpu.readRegister(a);
    }

    /**
     * Get The string represention from a register
     */
    public String toString(Registers a) {
        return this.cpu.readRegister(a).toString();
    }

}
