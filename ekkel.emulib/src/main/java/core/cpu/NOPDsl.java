package core.cpu;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.*;

import java.util.Stack;

public class NOPDsl implements OpcodeDSL {

    OpcodeDSL parent;
    CPU8Bit cpu;
    public NOPDsl(CPU8Bit cpu, MMU mmuImpl, OpcodeDSL parent) {
        this.parent = parent;
        this.cpu = cpu;
    }

    @Override
    public boolean isPipelineEmpty() {
        return false;
    }

    @Override
    public Stack<Computable> getInternalStack() {
        return null;
    }

    @Override
    public boolean hasBranched() {
        return false;
    }

    @Override
    public void flush() {

    }

    @Override
    public void setInternalStack(Stack<Computable> stack) {

    }

    @Override
    public OpcodeDSL load(MemoryAddress address) {
        return null;
    }

    @Override
    public OpcodeDSL load(Registers reg) {
        return this;
    }

    @Override
    public OpcodeDSL loadD8WithOffset(MemoryAddress offset) throws NotImplementedException, IllegalAccessException {
        return null;
    }

    @Override
    public OpcodeDSL loadD8() throws NotImplementedException, IllegalAccessException {
        return null;
    }

    @Override
    public OpcodeDSL loadS8() throws NotImplementedException, IllegalAccessException {
        return null;
    }

    @Override
    public OpcodeDSL peekS8() throws NotImplementedException, IllegalAccessException {
        return null;
    }

    @Override
    public Computable getD8() {
        return null;
    }

    @Override
    public Computable getD16() throws NotImplementedException, IllegalAccessException {
        return null;
    }

    @Override
    public Computable getS8() throws NotImplementedException, IllegalAccessException {
        return null;
    }

    @Override
    public OpcodeDSL storeRD8(Registers reg) {
        return null;
    }

    @Override
    public OpcodeDSL add() {
        return this;
    }

    @Override
    public OpcodeDSL dec() {
        return null;
    }

    @Override
    public OpcodeDSL xor() {
        return null;
    }

    @Override
    public OpcodeDSL shiftRight(int position) {
        return null;
    }

    @Override
    public OpcodeDSL shiftLeft(int position) {
        return null;
    }

    @Override
    public OpcodeDSL rotate(int p1, int p2) {
        return null;
    }

    @Override
    public OpcodeDSL adc() {
        return null;
    }

    @Override
    public OpcodeDSL sbc() {
        return null;
    }

    @Override
    public OpcodeDSL bitwiseSwap() {
        return null;
    }

    @Override
    public OpcodeDSL bitwiseOr() {
        return null;
    }

    @Override
    public OpcodeDSL bitwiseAnd() {
        return null;
    }

    @Override
    public OpcodeDSL store(MemoryValue r) throws NotImplementedException {
        return null;
    }

    @Override
    public OpcodeDSL store() throws NotImplementedException {
        return null;
    }

    @Override
    public OpcodeDSL loadA16() throws NotImplementedException, IllegalAccessException {
        return null;
    }

    @Override
    public OpcodeDSL loadD16() throws NotImplementedException, IllegalAccessException {
        return null;
    }

    @Override
    public OpcodeDSL loadIR16(Registers r) throws NotImplementedException, IllegalAccessException {
        return null;
    }

    @Override
    public OpcodeDSL loadIV16() throws NotImplementedException, IllegalAccessException {
        return null;
    }

    @Override
    public OpcodeDSL store(Registers r) {
        return this;
    }

    @Override
    public OpcodeDSL storeA8() throws NotImplementedException {
        return null;
    }

    @Override
    public OpcodeDSL storeA16() throws NotImplementedException {
        return null;
    }

    @Override
    public OpcodeDSL incPC() {
        return this;
    }

    @Override
    public OpcodeDSL inc() {
        return null;
    }

    @Override
    public OpcodeDSL sub() {
        return null;
    }

    @Override
    public OpcodeDSL add(int value) {
        return this;
    }

    @Override
    public OpcodeDSL push(Computable c) throws NotImplementedException {
        return this;
    }

    @Override
    public OpcodeDSL pop() throws NotImplementedException, IllegalAccessException {
        return this;
    }

    @Override
    public OpcodeDSL flags(int... flags) {
        return null;
    }

    @Override
    public OpcodeDSL carryLsb() {
        return null;
    }

    @Override
    public OpcodeDSL carryMsb() {
        return null;
    }

    @Override
    public OpcodeDSL exprIf(BranchCondition condition, Registers flag) {
        return null;
    }

    @Override
    public OpcodeDSL exprElse() {
        return this.parent;
    }

    @Override
    public OpcodeDSL stop() {
        return null;
    }
}
