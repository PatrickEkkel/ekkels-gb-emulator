package ekkel.gameboy.cpu.opcodes.branch;

import core.cpu.BranchCondition;

public class JR_C_r8 extends JR_c_r8 {

    public JR_C_r8() {
        this.instr = 0x38;
        this.setBranchCondition(BranchCondition.C);
        this.mnemonic.setMnemonic("JRC");
    }

}
