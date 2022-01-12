package core.cpu.opcodes;


/**
 * Human readable version of the opcode
 */
public class Instruction {
    private String mnemonic;
    private String register;
    public void setMnemonic(String mnemonic) {
        this.mnemonic = mnemonic;
    }
    public void setRegister(String register) {
        this.register = register;
    }
    public String getMnemonic() {
        return this.mnemonic;
    }
    public String getRegister() { return this.register; }
}

