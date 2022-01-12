package ekkel.gameboy.cpu.sharpLR35902;

import core.cpu.CPU;
import core.cpu.Stack;
import core.cpu.opcodes.Decoder;
import core.cpu.opcodes.Fetcher;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.opcodes.exceptions.UnknownOpcodeException;
import core.cpu.registers.Aggregate16BitRegister;
import core.cpu.registers.Register;
import core.cpu.registers.RegisterFlag;
import core.cpu.registers.Registers;
import core.mmu.*;
import core.mmu.memorymap.MemoryMap;
import core.mmu.memorymap.MemoryMapEntry;
import ekkel.gameboy.boot.BootRomLoader;
import ekkel.gameboy.cpu.IOMap;
import ekkel.gameboy.cpu.sharpLR35902.decoders.CBDecoder;
import ekkel.gameboy.cpu.sharpLR35902.decoders.StandardDecoder;
import ekkel.gameboy.ppu.DummyPPU;
import ekkel.gameboy.ppu.PPU;
import ekkel.gameboy.screen.Screen;

import java.util.ArrayList;
import java.util.List;

public class SharpLR35902 extends CPU {

    private PPU ppu;
    private CGB cgb;
    private BootRomLoader bootRomLoader;
    List<MMUComponent> devices;

    @Override
    public MemoryMap getMemoryMap() {
        // merge memory maps and expose as one
        MemoryMap memoryMap = this.mmuImpl.getMemoryMap();
        memoryMap.merge(ppu);
        return memoryMap;
    }

    private class Fetcher extends core.cpu.opcodes.Fetcher {
        public Fetcher(MMU mmuImpl, CPU cpu, core.cpu.opcodes.Decoder decoder) {
            super(mmuImpl, cpu, decoder);
        }

        int cbOffset = 0;

        @Override
        public core.cpu.opcodes.Decoder fetch() throws NotImplementedException, IllegalAccessException {
            core.cpu.opcodes.Decoder decoder = super.fetch();
            if (this.getCurrentOpcode().getValue() == 0xCB) {
                cbOffset = 1;
                Decoder standarDecoder = super.fetch();
                cbOffset = 0;
                cbDecoder.setOpcode(standarDecoder.getOpcode());
                return cbDecoder;
            } else {
                return decoder;
            }
        }

        @Override
        protected int getPC() {
            return super.getPC() + cbOffset;
        }
    }


    public SharpLR35902(MMU mmuImpl, boolean dmgBootrom) {
        super();
        this.devices = new ArrayList<>();
        this.mmuImpl = mmuImpl;
        this.mmuImpl.flush();
        this.decoder = new StandardDecoder(this, this.mmuImpl);
        this.cbDecoder = new CBDecoder(this, this.mmuImpl);
        this.fetcher = new Fetcher(this.mmuImpl, this, this.decoder);
        this.ppu = new PPU();
        this.stack = new Stack(mmuImpl, this);
        this.cgb = new CGB();

        this.devices.add(cgb);
        this.devices.add(ppu);
        if (dmgBootrom) {
            this.bootRomLoader = new BootRomLoader(mmuImpl);
            // Map the Bootrom on CPU creation.
            bootRomLoader.map();
            this.setPC(0x00);
        } else {
            this.setPC(0x100);
        }

    }

    private MMU mmuImpl;
    private core.cpu.opcodes.Fetcher fetcher;
    private StandardDecoder decoder;
    private CBDecoder cbDecoder;

    public Decoder[] getDecoders() {
        Decoder[] result = {this.decoder, this.cbDecoder};
        return result;
    }

    public core.cpu.opcodes.Fetcher getFetcher() {
        return this.fetcher;
    }

    @Override
    public void setFetcher(core.cpu.opcodes.Fetcher fetcher) {
        this.fetcher = fetcher;
    }

    @Override
    public Computable getZeroFlag() {
        return new RegisterFlag("Z", 0x80);
    }

    @Override
    public Computable getSubstractFlag() {
        return new RegisterFlag("N", 0x40);
    }

    @Override
    public Computable getHalfCarryFlag() {
        return new RegisterFlag("H", 0x20);
    }

    @Override
    public Computable getCarryFlag() {
        return new RegisterFlag("C", 0x10);
    }

    @Override
    public void setFlag(Computable flag) {
        this.readRegister(Registers.F).setValue(this.readRegister(Registers.F).or(flag).getValue());
    }

    protected void defineRegisters() {

        Register A = new Register(0x00, 8, Registers.A);
        Register F = new Register(0x00, 8, Registers.F);

        Register B = new Register(0x00, 8, Registers.B);
        Register C = new Register(0x00, 8, Registers.C);

        Register D = new Register(0x00, 8, Registers.D);
        Register E = new Register(0x00, 8, Registers.E);

        Register H = new Register(0x00, 8, Registers.H);
        Register L = new Register(0x00, 8, Registers.L);

        this.reg.put(Registers.AF, new Aggregate16BitRegister(Registers.AF, A, F));
        this.reg.put(Registers.A, A);
        this.reg.put(Registers.F, F);


        this.reg.put(Registers.BC, new Aggregate16BitRegister(Registers.BC, B, C));
        this.reg.put(Registers.B, B);
        this.reg.put(Registers.C, C);

        this.reg.put(Registers.DE, new Aggregate16BitRegister(Registers.DE, D, E));
        this.reg.put(Registers.D, D);
        this.reg.put(Registers.E, E);

        this.reg.put(Registers.HL, new Aggregate16BitRegister(Registers.HL, H, L));
        this.reg.put(Registers.H, H);
        this.reg.put(Registers.L, L);
        this.reg.put(Registers.SP, new Register(0x00, 16, Registers.SP));
        this.reg.put(Registers.PC, new Register(0x00, 16, Registers.PC));

    }

    @Override
    public void initRegisterStartValues() {
        /**
         * Set the base values of the registers the same as BGB
         */
        this.writeRegister(Registers.AF, new ComputableImpl(0x1180));
        this.writeRegister(Registers.BC, new ComputableImpl(0x0000));
        this.writeRegister(Registers.DE, new ComputableImpl(0xFF56));
        this.writeRegister(Registers.HL, new ComputableImpl(0x000D));
        this.writeRegister(Registers.SP, new ComputableImpl(0xFFFE));
    }

    @Override
    public int tick(long cycles) throws NotImplementedException, IllegalAccessException, UnknownOpcodeException {
        int cycleResult = this.fetcher.fetch().decode().execute();
        this.ppu.tick(cycleResult);
        return cycleResult;
    }

    @Override
    public void write(MemoryAddress memoryAddress, MemoryValue value) throws NotImplementedException {
        for (MMUComponent mmuComponent : this.devices) {
            if (mmuComponent.IsAddressed(memoryAddress)) {
                mmuComponent.write(memoryAddress, value);
                return;
            }
        }
    }

    @Override
    public MemoryValue read(MemoryAddress memoryAddress) throws NotImplementedException, IllegalAccessException {

        for (MMUComponent mmuComponent : this.devices) {
            if (mmuComponent.IsAddressed(memoryAddress)) {
                return mmuComponent.read(memoryAddress);
            }
        }
        throw new IllegalAccessException(String.format("Trying to access memory address that is illigal %s", memoryAddress.getValue()));
    }


    @Override
    public boolean IsAddressed(MemoryAddress memoryAddress) throws NotImplementedException {
        for (MMUComponent mmuComponent : this.devices) {
            if (mmuComponent.IsAddressed(memoryAddress)) {
                return true;
            }
        }
        return false;
    }

    @Override
    public List<MemoryMapEntry> getComponentIds() {
        MemoryMapEntry memoryMapEntry = new MemoryMapEntry("SHARP_LR_35902");
        memoryMapEntry.addRegister(IOMap.DMGROMDISABLE, "Disable Bootrom");

        List<MemoryMapEntry> result = new ArrayList<>();
        result.add(memoryMapEntry);
        return result;
    }

    public void connectToPPU(MMUComponent component) {
        this.ppu.connectToBus(component);
    }
}
