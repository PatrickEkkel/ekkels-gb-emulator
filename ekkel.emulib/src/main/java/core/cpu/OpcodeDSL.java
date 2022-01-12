package core.cpu;
import java.util.Stack;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.Computable;
import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;

public interface OpcodeDSL {

    boolean isPipelineEmpty();


    Stack<Computable> getInternalStack();

    /**
     * Indicated if the dsl has entered the branch, usefull to determine the amount of clockcycles
     * @return
     */
    boolean hasBranched();

    /**
     * will clear any remaining computables
     */
    void flush();

    void setInternalStack(Stack<Computable> stack);
    /**
     * Load explicit Address value into the pipeline
     */
    OpcodeDSL load(MemoryAddress address);

    /**
     * Load a value of a register into the pipeline
     *
     * @param reg
     * @return
     */
    OpcodeDSL load(Registers reg);

    /**
     * Standard 8 bit load but with a predefined Offset
     * @param offset
     * @return
     */
    OpcodeDSL loadD8WithOffset(MemoryAddress offset) throws NotImplementedException, IllegalAccessException;

    /**
     * Load 8 bit value from opcode into the pipeline
     *
     * @return
     * @throws NotImplementedException
     * @throws IllegalAccessException
     */
    OpcodeDSL loadD8() throws NotImplementedException, IllegalAccessException;

    /**
     * Load 8 bit signed value from opcode into the pipeline and increment the PC by one
     * @return
     */
    OpcodeDSL loadS8() throws NotImplementedException, IllegalAccessException;

    /**
     * Load a 8 bit signed value from opcode into the pipeline but don't increment the PC
     * @return
     */
    OpcodeDSL peekS8() throws NotImplementedException, IllegalAccessException;

    /**
     * get the 8 bit value from the opcode
     * @return
     */
    Computable getD8() throws NotImplementedException, IllegalAccessException;
    /**
     * get the 16 bit value from the opcode
     * @return
     */
    Computable getD16() throws NotImplementedException, IllegalAccessException;

    /**
     * get 8 bit signed value from the opcode
     * @return
     */
    Computable getS8() throws NotImplementedException, IllegalAccessException;

    /**
     * Store the value that is currently in the pipeline in the selected Register
     *
     * @param reg
     * @return
     */
    OpcodeDSL storeRD8(Registers reg);

    /**
     * Add 2 value that are currently in the pipeline and push the result on the pipeline
     * @return
     */
    OpcodeDSL add();

    /**
     * Decrement the value that is currently in the pipeline and push the decremented value on the pipeline
     * @return
     */
    OpcodeDSL dec();

    /**
     *  Xor 2 values that are currently in the pipeline and push the result on the pipeline
     * @return
     */
    OpcodeDSL xor();

    /**
     * shift the value that is currently in the pipeline n positions to right
     * @param position
     * @return
     */
    OpcodeDSL shiftRight(int position);

    /**
     * shift the value that is currently in the pipeline n positions to left
     * @param position
     * @return
     */
    OpcodeDSL shiftLeft(int position);

    /**
     * take the value from the pipeline and move 2 bits around, first operand can also be CARRY flag
     * @param p1
     * @param p2
     * @return
     */
    OpcodeDSL rotate(int p1, int p2);

    /**
     * Take the value from the carry flag and add it to the current value in the pipeline
     * @return
     */
    OpcodeDSL adc();

    /**
     * Take the value from the carry flag and substract in from current value in the pipeline
     * @return
     */
    OpcodeDSL sbc();

    /**
     * in case of 8-bit swap MSB nibble to LSB nibble and vice versa, in case of 16-bit swap MSB word to LSB word and vice versa
     * @return
     */
    OpcodeDSL bitwiseSwap();

    /**
     * Take 2 values from the pipe and do a bitwse or on the pushing the result on the pipeline
     * @return
     */
    OpcodeDSL bitwiseOr();

    /** take 2 values from the pipe and do a bitwise and and push the result on the pipeline
     *
     * @return
     */
    OpcodeDSL bitwiseAnd();
    /**
     * store explicit Memory value into loaded Address value
     *
     * @param r
     * @return
     */
    OpcodeDSL store(MemoryValue r) throws NotImplementedException;

    /**
     * Store loaded value from pipeline into loaded address from pipeline
     * @return
     */
    OpcodeDSL store() throws NotImplementedException;


    /**
     * Load adresss from opcode into the pipeline
     *
     * @return
     */
    OpcodeDSL loadA16() throws NotImplementedException, IllegalAccessException;

    /**
     * Load adresss from opcode into the pipeline
     *
     * @return
     */
    OpcodeDSL loadD16() throws NotImplementedException, IllegalAccessException;

    /**
     * Load  load indirect 16 bit value into pipeline. take value of memory address stored at r1
     * @return
     */
    OpcodeDSL loadIR16(Registers r) throws NotImplementedException, IllegalAccessException;

    /**
     * Load indirect 16 bit value into the pipeline. Take the value from the pipeline and interpret is as a memory address
     * @return
     */
    OpcodeDSL loadIV16() throws NotImplementedException, IllegalAccessException;


    /**
     * Store value that is provided by the pipeline into the selected register
     *
     * @param r
     * @return
     */
    OpcodeDSL store(Registers r);

    /**
     * Store 8 BIT register value into memory location provided by the pipeline
     *
     * @return
     * @throws NotImplementedException
     */
    OpcodeDSL storeA8() throws NotImplementedException;

    /**
     * Store 16 BIT register value into memory location providied by the pipeline
     * @return
     */
    OpcodeDSL storeA16() throws NotImplementedException;

    /**
     * Load PC register and increment by 1 and store it
     * @return
     */
    OpcodeDSL incPC();

    /**
     * Increment current value that is in the pipeline
     *
     * @return
     */
    OpcodeDSL inc();

    /** sustract the second value from the first value in the pipeline
     *
     * @return
     */
    OpcodeDSL sub();

    /**
     * Add an integer value to the value that is loaded into the pipeline
     *
     * @param value
     * @return
     */
    OpcodeDSL add(int value);


    /**
     * push value on the stack
     * @param c
     * @return
     */
    OpcodeDSL push(Computable c) throws NotImplementedException;

    /**
     * pop value from the stack
     * @return
     */
    OpcodeDSL pop() throws NotImplementedException, IllegalAccessException;

    /**
     * Set CPU flags
     * @return
     */
    OpcodeDSL flags(int... flags);

    /**
     * put the value of the least significant bit of the value that currently in the pipeline in the carryflag
     * @return
     */
    OpcodeDSL carryLsb();

    /**
     * put the value of the most significant bit of the value that is currently in the pipeline in the carryflag
     * @return
     */
    OpcodeDSL carryMsb();


    /**
     * if condition is met, than execute the branch otherwise emit NOPs
     * @param condition
     * @param flag
     * @return
     */
    OpcodeDSL exprIf(BranchCondition condition,Registers flag);

    OpcodeDSL exprElse();

    /**
     * Block execution until interrupt is detected (to be implemented)
     * @return
     */
    OpcodeDSL stop();
}
