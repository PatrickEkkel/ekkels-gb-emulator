package ekkel.gameboy.cpu.opcodes.branch;

import core.cpu.BranchCondition;

public class JR_NC_r8 extends JR_c_r8 {

    public JR_NC_r8() {
        this.instr = 0x30;
        this.mnemonic.setMnemonic("JRNC");
        this.setBranchCondition(BranchCondition.NC);
    }

}
