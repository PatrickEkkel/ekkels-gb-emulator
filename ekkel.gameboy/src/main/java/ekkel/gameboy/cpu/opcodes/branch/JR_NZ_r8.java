package ekkel.gameboy.cpu.opcodes.branch;

import core.cpu.BranchCondition;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class JR_NZ_r8  extends JR_c_r8 {

    public JR_NZ_r8() {
        this.mnemonic.setMnemonic("JRNZ");
        this.setBranchCondition(BranchCondition.NZ);
        this.instr = 0x20;
    }
}
