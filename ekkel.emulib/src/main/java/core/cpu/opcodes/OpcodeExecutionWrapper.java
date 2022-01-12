package core.cpu.opcodes;

import core.cpu.opcodes.exceptions.NotImplementedException;

public class OpcodeExecutionWrapper extends Opcode {


    private Opcode opcode;
    public OpcodeExecutionWrapper(Opcode opcode) {
        this.opcode = opcode;
    }

    @Override
    public int[] toBinary() {
        return this.opcode.toBinary();
    }

    @Override
    public String toString() {
        return this.opcode.toString();
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        this.opcode.dryRun();
    }

    @Override
    public int getInstr() {
        return this.opcode.getInstr();
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        this.opcode.flush();
        return this.opcode.execute();
    }
}
