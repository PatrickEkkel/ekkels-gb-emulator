package core.cpu;

import core.cpu.flags.*;
import core.cpu.flags.utils.FlagUtils;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Register;
import core.cpu.registers.Registers;
import core.mmu.*;

import java.util.Stack;

public class Standard8BitDSL implements OpcodeDSL {

    private Stack<Computable> parameters = new Stack<>();
    private final MMU mmuImpl;
    private CPU8Bit cpu;
    private boolean hasBranched;

    private BaseFlagHandler carryFlagHandler;
    private BaseFlagHandler halfCarryFlagHandler;
    private OpcodeDSL parentDsl;
    protected void setParentDsl(OpcodeDSL dsl) {
        this.parentDsl = dsl;
        this.parentDsl.setInternalStack(dsl.getInternalStack());

    }

    public Stack<Computable> getInternalStack() {
        return this.parameters;
    }

    @Override
    public boolean hasBranched() {
        return this.hasBranched;
    }

    @Override
    public void flush() {
        this.parameters.clear();
        this.halfCarryFlagHandler = new HalfCarryFlagHandler(this.cpu.getHalfCarryFlag());
        this.carryFlagHandler = new CarryFlagHandler(this.cpu.getCarryFlag());
    }

    public void setInternalStack(Stack<Computable> parameters) {
        this.parameters = parameters;
    }

    private void read8BitValue() throws NotImplementedException, IllegalAccessException {
        //int PC = this.cpu.readRegister(Registers.PC).getValue();
        int PC = this.parameters.pop().getValue();
        PC += 1;
        // push the 8 bit value on the stack
        this.parameters.push(mmuImpl.read(MemoryAddress.fromValue(PC)));
        // push the program counter on the stack
        this.parameters.push(MemoryAddress.fromValue(PC));
    }

    private void read16BitValue() throws NotImplementedException, IllegalAccessException {
        this.parameters.push(this.cpu.readRegister(Registers.PC)).getValue();
        read8BitValue();
        read8BitValue();

        MemoryAddress PC = (MemoryAddress)parameters.pop();

        MemoryValue msb = (MemoryValue) parameters.pop();
        MemoryValue lsb = (MemoryValue) parameters.pop();

        this.parameters.push(MemoryAddress.combine8BitValues(lsb,msb));
        this.parameters.push(PC);
    }

    public Standard8BitDSL(MMU mmuImpl, CPU8Bit cpu) {
        this.mmuImpl = mmuImpl;
        this.cpu = cpu;
        this.carryFlagHandler = new CarryFlagHandler(cpu.getCarryFlag());
        this.halfCarryFlagHandler = new HalfCarryFlagHandler(cpu.getHalfCarryFlag());
    }

    @Override
    public boolean isPipelineEmpty() {
        return this.parameters.empty();
    }

    @Override
    public OpcodeDSL load(MemoryAddress address) {
        this.parameters.push(address);
        return this;
    }

    @Override
    public OpcodeDSL load(Registers reg) {
        this.parameters.push(cpu.readRegister(reg));
        return this;
    }

    @Override
    public OpcodeDSL loadD8WithOffset(MemoryAddress offset) throws NotImplementedException, IllegalAccessException {
        this.loadD8();
       Computable c =  this.parameters.pop();
       Computable memoryAddress = offset.add(c);
       this.parameters.push(memoryAddress);
       return this;
    }

    public OpcodeDSL loadD8() throws NotImplementedException, IllegalAccessException {
        this.parameters.push(this.cpu.readRegister(Registers.PC)).getValue();
        read8BitValue();
        this.store(Registers.PC);
        return this;
    }

    @Override
    public OpcodeDSL loadS8() throws NotImplementedException, IllegalAccessException {
        this.parameters.push(this.cpu.readRegister(Registers.PC));
        read8BitValue();
        this.store(Registers.PC);
        this.parameters.push(this.parameters.pop().convertToSigned());
        return this;
    }

    @Override
    public OpcodeDSL peekS8() throws NotImplementedException, IllegalAccessException {
        this.parameters.push(this.cpu.readRegister(Registers.PC)).getValue();
        read8BitValue();
        // pop the PC from the stack and discard the value
        this.parameters.pop();
        this.parameters.push(this.parameters.pop().convertToSigned());
        return this;
    }

    @Override
    public Computable getD8() throws NotImplementedException, IllegalAccessException {
        this.parameters.push(this.cpu.readRegister(Registers.PC));
        read8BitValue();
        this.parameters.pop();
        return MemoryAddress.fromComputable(this.parameters.pop());
    }

    @Override
    public Computable getD16() throws NotImplementedException, IllegalAccessException {
        read16BitValue();

        this.parameters.pop();

        return MemoryAddress.fromComputable(this.parameters.pop());

    }

    @Override
    public Computable getS8() throws NotImplementedException, IllegalAccessException {
        this.parameters.push(this.cpu.readRegister(Registers.PC));
        read8BitValue();
        this.parameters.pop();
        return MemoryAddress.fromComputable(this.parameters.pop().convertToSigned());
    }

    public OpcodeDSL storeRD8(Registers reg) {
        Computable computable = this.parameters.pop();
        this.cpu.writeRegister(reg,computable);
        return this;
    }

    @Override
    public OpcodeDSL add() {
       Computable a =  this.parameters.pop();
       Computable b = this.parameters.pop();
       if(a.is16Bit() && b.is16Bit()) {
           this.halfCarryFlagHandler = new Add16BitHalfCarryHandler(this.cpu.getHalfCarryFlag());
       }
       else if(a.is16Bit() && b.is8Bit()) {
           this.carryFlagHandler = new AddD16toS8CarryHandler(this.cpu.getCarryFlag());
       }
       Computable c = a.add(b);
        this.parameters.push(b);
        this.parameters.push(a);
        this.parameters.push(c);
       return this;
    }

    @Override
    public OpcodeDSL dec() {
        Computable a = this.parameters.pop();
        Computable b =  a.dec();
        Computable c = b;

        this.parameters.push(b);
        this.parameters.push(a);
        this.parameters.push(c);
        return this;
    }

    @Override
    public OpcodeDSL xor() {
        Computable a = this.parameters.pop();
        Computable b = this.parameters.pop();
        this.parameters.push(a.xor(b));
        return this;
    }

    @Override
    public OpcodeDSL shiftRight(int position) {
        Computable a = this.parameters.pop();
        Computable b = a;
        Computable c = a.shiftRight(position);

        this.parameters.push(b);
        this.parameters.push(a);
        this.parameters.push(c);
        return this;
    }

    @Override
    public OpcodeDSL shiftLeft(int position) {
        Computable a = this.parameters.pop();
        Computable b = a;
        Computable c = a.shiftLeft(position);
        this.parameters.push(b);
        this.parameters.push(a);
        this.parameters.push(c);
        return this;
    }

    @Override
    public OpcodeDSL rotate(int p1, int p2) {

        Computable c = this.parameters.pop();

        Computable result = null;

        if(p1 == Flags.C) {

            Register flagRegister = this.cpu.readRegister(Registers.F);
            Computable carryFlag = this.cpu.getCarryFlag();
            // check if carryflag is set
            if(flagRegister.and(carryFlag).getValue() == carryFlag.getValue()) {

                this.parameters.push(c.setBit(p2,0x1));
            }
            else {
                this.parameters.push(c.setBit(p2, 0x0));
            }
        }
        return this;
    }

    @Override
    public OpcodeDSL adc() {

        Computable a = this.parameters.pop();
        Computable carryFlag = this.cpu.getCarryFlag();
        Computable flagsRegister = this.cpu.readRegister(Registers.F);

        // check if carry is set
        if(flagsRegister.and(carryFlag).equals(carryFlag)) {
           Computable d = a.add(ComputableImpl.fromValue(0x1));
           this.parameters.push(a);
           this.parameters.push(d);
           this.halfCarryFlagHandler = new ADCHalfCarryHandler(this.cpu.getHalfCarryFlag());
           this.carryFlagHandler = new ADCCarryHandler(this.cpu.getCarryFlag());
        }
        else {
           this.parameters.push(a);
        }

        return this;
    }

    @Override
    public OpcodeDSL sbc() {
        Computable a = this.parameters.pop();
        Computable carryFlag = this.cpu.getCarryFlag();
        Computable flagsRegister = this.cpu.readRegister(Registers.F);

        if(flagsRegister.and(carryFlag).equals(carryFlag))  {
           Computable d = a.sub(ComputableImpl.fromValue(0x1));
            this.parameters.push(a);
            this.parameters.push(d);
            this.halfCarryFlagHandler = new SBCHalfCarryHandler(this.cpu.getHalfCarryFlag());
            this.carryFlagHandler = new SBCCarryHandler(this.cpu.getCarryFlag());

        }
        else {
            this.parameters.push(a);
        }
        return this;
    }

    @Override
    public OpcodeDSL bitwiseSwap() {
        Computable a = this.parameters.pop();
        Computable msbNibble = a.and(ComputableImpl.fromValue(0xF));
        Computable lsbNibble = a.and(ComputableImpl.fromValue(0xF0)).shiftRight(4);
        this.parameters.push(msbNibble.shiftLeft(4).or(lsbNibble));
        return this;
    }

    @Override
    public OpcodeDSL bitwiseOr() {
        Computable value_a = this.parameters.pop();
        Computable value_b = this.parameters.pop();
        Computable c = value_a.or(value_b);
        this.parameters.push(value_b);
        this.parameters.push(value_a);
        this.parameters.push(c);
        return this;
    }

    @Override
    public OpcodeDSL bitwiseAnd() {
        Computable value_a = this.parameters.pop();
        Computable value_b = this.parameters.pop();
        Computable c = value_a.and(value_b);
        this.parameters.push(value_b);
        this.parameters.push(value_a);
        this.parameters.push(c);
        return this;
    }

    public OpcodeDSL loadD16() throws NotImplementedException, IllegalAccessException {
        read16BitValue();
        return this.store(Registers.PC);
    }

    @Override
    public OpcodeDSL loadIR16(Registers r) throws NotImplementedException, IllegalAccessException {
        this.load(r);
        Computable  value = this.mmuImpl.read(MemoryAddress.fromComputable(this.parameters.pop()));
        this.parameters.push(value);
        return this;
    }

    @Override
    public OpcodeDSL loadIV16() throws NotImplementedException, IllegalAccessException {
        Computable c = this.parameters.pop();
        Computable value = this.mmuImpl.read(MemoryAddress.fromComputable(c));
        this.parameters.push(value);
        return this;
    }


    @Override
    public OpcodeDSL loadA16() throws NotImplementedException, IllegalAccessException {
        read16BitValue();
        this.store(Registers.PC);
        return this;
    }

    @Override
    public OpcodeDSL store(Registers r) {
        Computable value = this.parameters.pop();
        this.cpu.writeRegister(r,value);
        return this;
    }

    public OpcodeDSL storeA8() throws NotImplementedException {
        Computable value = this.parameters.pop();
        MemoryAddress address = (MemoryAddress)this.parameters.pop();
        this.mmuImpl.write(address,MemoryValue.fromComputable(value));
        return this;
    }

    @Override
    public OpcodeDSL storeA16() throws NotImplementedException {
        Computable value = this.parameters.pop();
        MemoryAddress lowByteAddress = (MemoryAddress)this.parameters.pop();
        MemoryAddress highByteAddress = MemoryAddress.fromComputable(lowByteAddress.inc());

        MemoryValue memoryValue = MemoryValue.fromComputable(value);

        MemoryValue lowByte = memoryValue.getLowByteAsComputable();
        MemoryValue highByte = memoryValue.getHighByteAsComputable();

        this.mmuImpl.write(lowByteAddress, lowByte);
        this.mmuImpl.write(highByteAddress, highByte);
        return this;
    }

    @Override
    public OpcodeDSL incPC() {
        Computable PC = this.cpu.readRegister(Registers.PC);
        PC.set(PC.inc());
        this.cpu.writeRegister(Registers.PC,PC);
        return this;
    }

    @Override
    public OpcodeDSL inc() {
        Computable a = this.parameters.pop();
        Computable b = a;
        this.halfCarryFlagHandler = new IncHalfCarryHandler(this.cpu.getHalfCarryFlag());
        this.parameters.push(b);
        this.parameters.push(a);
        this.parameters.push(a.inc());
        return this;
    }

    @Override
    public OpcodeDSL sub() {
        Computable v1 = this.parameters.pop();
        Computable v2 = this.parameters.pop();
        this.parameters.push(v2);
        this.parameters.push(v1);
        this.parameters.push(v1.sub(v2));
        return this;
    }

    @Override
    public OpcodeDSL add(int value) {
        Computable c = this.parameters.pop();
        c.add(value);
        this.parameters.push(c);
        return this;
    }

    @Override
    public OpcodeDSL push(Computable c) throws NotImplementedException {
        Computable lsb = new ComputableImpl(c.getLowByte());
        Computable msb = new ComputableImpl(c.getHighByte());
        this.cpu.getStack().push(msb);
        this.cpu.getStack().push(lsb);
        return this;
    }

    @Override
    public OpcodeDSL pop() throws NotImplementedException, IllegalAccessException {

        Computable lsb = this.cpu.getStack().pop();
        Computable msb = this.cpu.getStack().pop();
        Computable c =MemoryAddress.combine8BitValues(MemoryValue.fromComputable(lsb),MemoryValue.fromComputable(msb));
        this.parameters.push(c);
        return this;
    }

    @Override
    public OpcodeDSL flags(int... flags) {
        // the mapping is Z N H C
        final int ZERO = 0;
        final int SUBSTRACT = 1;
        final int HALF_CARRY = 2;
        final int CARRY = 3;

        for(int i=0;i<flags.length;i++) {
            int currentFlag = flags[i];
            Computable flagsRegister = this.cpu.readRegister(Registers.F);
            switch (i) {
                case ZERO:
                    ZeroFlagHandler zeroFlagHandler = new ZeroFlagHandler(this.cpu.getZeroFlag());
                    zeroFlagHandler.setFlagsRegister(flagsRegister);
                    zeroFlagHandler.setParameters(parameters);
                    zeroFlagHandler.setCurrentFlag(currentFlag);
                    this.cpu.writeRegister(Registers.F,zeroFlagHandler.handle());
                break;
                case SUBSTRACT:
                    SubstractFlagHandler substractFlagHandler = new SubstractFlagHandler(this.cpu.getSubstractFlag());
                    substractFlagHandler.setFlagsRegister(flagsRegister);
                    substractFlagHandler.setCurrentFlag(currentFlag);
                    this.cpu.writeRegister(Registers.F,substractFlagHandler.handle());
                    break;
                case HALF_CARRY:
                    halfCarryFlagHandler.setCurrentFlag(currentFlag);
                    halfCarryFlagHandler.setCPU(this.cpu);
                    halfCarryFlagHandler.setFlagsRegister(flagsRegister);
                    halfCarryFlagHandler.setParameters(parameters);
                    this.cpu.writeRegister(Registers.F,halfCarryFlagHandler.handle());
                //    this.halfCarryFlagHandler = new HalfCarryFlagHandler(this.cpu.getHalfCarryFlag());

                    break;
                case CARRY:
                    carryFlagHandler.setCurrentFlag(currentFlag);
                    carryFlagHandler.setCPU(this.cpu);
                    carryFlagHandler.setFlagsRegister(flagsRegister);
                    carryFlagHandler.setParameters(parameters);
                    this.cpu.writeRegister(Registers.F,carryFlagHandler.handle());
                    // reset to default handler after every flag operation
             //       this.carryFlagHandler = new CarryFlagHandler(this.cpu.getCarryFlag());
                    break;

            }

        }
        return this;
    }

    @Override
    public OpcodeDSL carryLsb() {
        this.carryFlagHandler = new LsbCarryHandler(this.cpu.getCarryFlag());
        return this;
    }

    @Override
    public OpcodeDSL carryMsb() {
        this.carryFlagHandler = new MsbCarryHandler(this.cpu.getCarryFlag());
        return this;
    }


    @Override
    public OpcodeDSL exprIf(BranchCondition condition, Registers flag) {
        this.load(flag);

        Register c = (Register) this.parameters.pop();
        boolean result = false;
        Computable zeroFlag = cpu.getZeroFlag();
        Computable carryFlag = cpu.getCarryFlag();

        switch (condition) {
            case Z:
                result = FlagUtils.isFlagSet(zeroFlag,c);
                break;
            case NZ:
                result = !FlagUtils.isFlagSet(zeroFlag, c);
                break;
            case NC:
                result = !FlagUtils.isFlagSet(carryFlag,c);
                break;
            case C:
                result = FlagUtils.isFlagSet(carryFlag, c);
        }
        this.hasBranched = result;
        if(result) {
            return this;
        }
        else  {
            return new NOPDsl(cpu, mmuImpl,this);
        }

    }

    @Override
    public OpcodeDSL exprElse() {
        return new NOPDsl(cpu, mmuImpl,this);
    }

    @Override
    public OpcodeDSL stop() {
        while (true) {
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public OpcodeDSL store(MemoryValue r) throws NotImplementedException {
        MemoryAddress address = (MemoryAddress) this.parameters.pop();

        this.mmuImpl.write(address,r);
        return this;
    }

    @Override
    public OpcodeDSL store() throws NotImplementedException {
        Computable address = this.parameters.pop();
        Computable value = this.parameters.pop();
        this.mmuImpl.write(MemoryAddress.fromComputable(address),MemoryValue.fromComputable(value));
        return this;
    }
}
