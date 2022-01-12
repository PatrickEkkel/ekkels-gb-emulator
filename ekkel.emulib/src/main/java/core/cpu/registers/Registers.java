package core.cpu.registers;

import java.util.Arrays;
import java.util.List;

public enum Registers {
    A("A"),
    B("B"),
    C("C"),
    D("D"),
    E("E"),
    F("F"),
    L("L"),
    H("H"),
    AF("AF"),
    BC("BC"),
    DE("DE"),
    HL("HL","(HL)"),
    SP("SP"),
    PC("PC");
    private List<String> names;
    Registers(String  ...name) {
        this.names = Arrays.asList(name);
    }


    public static Registers getRegister(String name) {

        for(Registers register : Registers.values()) {
            if(register.names.contains(name)) {
                return register;
            }
        }
        return  null;
    }


    @Override
    public String toString() {
        return this.names.get(0);
    }
}
