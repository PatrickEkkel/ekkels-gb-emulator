package core.parser;

public class ArgumentClassifier {

    public static boolean is16BitValue(String address) {
        return address.startsWith("0x") && address.length() == 6;
    }
    public static boolean is8BitValue(String address) {
        return address.startsWith("0x") && address.length() == 4;
    }
    public static boolean isRegister(String register) {
       return (register.length() == 1 || register.length() == 2 || register.length() == 4)
               && (!register.startsWith("0x")) && (!register.startsWith("s"));
    }

    public static boolean is8BitSignedValue(String address) {
        return address.startsWith("s");
    }
}
