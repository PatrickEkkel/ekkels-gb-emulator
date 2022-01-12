package core.cpu.opcodes;

import core.cpu.CPU;
import core.cpu.OpcodeDSL;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.Computable;
import core.mmu.MemoryAddress;

import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.List;

public abstract class Opcode {
    private Computable data;
    protected CPU cpu;
    protected int instr;
    protected OpcodeDSL dsl;
    protected int length;
    protected List<Computable> computables;
    protected Instruction mnemonic = new Instruction();
    protected Opcode() {

    }

    private void setDSL(OpcodeDSL dsl) {
        this.dsl = dsl;
    }
    private void setCPU(CPU cpu) {
     this.cpu = cpu;
    }

    public void setComputables(List<Computable> computables) {
        this.computables = computables;
        this.setRelevantComputableForByteRepresentation();
    }

    public void flush() {
        this.dsl.flush();
    }

    protected List<Computable> getComputables() {
        return this.computables;
    }

    /**
     * Helper method to generate machine language from this opcode
     * @return
     */
    public abstract int [] toBinary();

    /**
     * Picks out relevant element of the Opcode that is used represent the Opcode in bytes
     */
    private void setRelevantComputableForByteRepresentation() {
        MemoryAddress mem = null;
        for(Computable computable : this.computables) {
            if(computable instanceof MemoryAddress) {
                mem =(MemoryAddress)computable;
            }
        }
        //assert this.computables.isEmpty() || mem != null;
        this.data = mem;
    }

    public Computable getData() {
        return this.data;
    }


    public int getInstr() {
        return this.instr;
    }

    public static Opcode fromClass(Class clazz, CPU cpu, OpcodeDSL dsl) {

        try {
            Opcode opcode = (Opcode) clazz.getDeclaredConstructor().newInstance();
            opcode.setCPU(cpu);
            opcode.setDSL(dsl);

            return  opcode;
        } catch (InstantiationException | NoSuchMethodException | InvocationTargetException | IllegalAccessException e) {
            e.printStackTrace();
            return null;
        }
    }

    public void dryRun() throws NotImplementedException, IllegalAccessException {

    }

    public void loadS8Computables() throws NotImplementedException, IllegalAccessException {
        List<Computable> computables = new ArrayList<>();
        computables.add(dsl.getS8());
        this.setComputables(computables);
    }

    public void loadD8Computables() throws NotImplementedException, IllegalAccessException {
        List<Computable> computables = new ArrayList<>();
        computables.add(dsl.getD8());
        this.setComputables(computables);
    }
    public void loadD16Computables() throws NotImplementedException, IllegalAccessException {
        List<Computable> computables = new ArrayList<>();
        computables.add(dsl.getD16());
        this.setComputables(computables);
    }

    public abstract int execute() throws NotImplementedException, IllegalAccessException;

    @Override
    public String toString() {
        return this.mnemonic.getMnemonic();
    }

}
