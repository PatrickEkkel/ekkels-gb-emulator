package core.cpu.registers;

import core.mmu.ComputableImpl;

public class RegisterFlag extends ComputableImpl {

    private String name;

    public RegisterFlag(String name, int value) {
        super(value);
        this.name = name;
        this.value = value;
    }

    @Override
    public String toString() {
        return String.format(" %s: 0x%s", this.name, Integer.toHexString(this.value));
    }
}
