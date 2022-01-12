package ekkel.gameboy;

import core.cpu.CPU;
import core.cpu.Clock;
import core.cpu.opcodes.exceptions.DivergedCPUStateException;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.opcodes.exceptions.UnknownOpcodeException;
import core.cpu.registers.Registers;
import core.device.SimpleDevice;
import core.mmu.ComputableImpl;
import core.mmu.MMUImpl;
import core.rom.RomLoader;
import debugger.SerialDevice;
import ekkel.gameboy.cpu.sharpLR35902.SharpLR35902;
import ekkel.gameboy.interrupts.InterruptFlag;
import ekkel.gameboy.ram.HRAM;
import ekkel.gameboy.ram.WRAM_BANK_0;
import ekkel.gameboy.ram.WRAM_BANK_1;
import ekkel.gameboy.rom.GameboyRom;
import ekkel.gameboy.rom.TestRom;
import ekkel.gameboy.screen.Screen;
import ekkel.gameboy.serial.SerialPort;
import ekkel.gameboy.timer.TAC;
import gui.Display;
import gui.DisplayDevice;

public class Gameboy implements DisplayDevice, SimpleDevice {

    protected GameboyRom rom;
    protected CPU cpu;
    protected MMUImpl mmuImpl;
    protected Screen screen;
    protected SerialDevice serialDevice;
    // 4.1MHZ
    private Clock clock = new Clock(4194304);

    public Gameboy(boolean dmgBootRom) {

        this.mmuImpl = new MMUImpl();
        SharpLR35902 sharpLR35902 = new SharpLR35902(this.mmuImpl, dmgBootRom);
        this.screen = new Screen();
        sharpLR35902.connectToPPU(this.screen);
        this.cpu = sharpLR35902;

        this.mmuImpl.connect(new InterruptFlag());
        this.mmuImpl.connect(new TAC());
        this.mmuImpl.connect(new WRAM_BANK_0());
        this.mmuImpl.connect(new WRAM_BANK_1());
        this.mmuImpl.connect(new HRAM());
        this.mmuImpl.connect(this.cpu);
    }


    public void connectLinkCable(SerialDevice serialDevice) {
        this.mmuImpl.connect(new SerialPort(serialDevice));
    }

    public void attachDebugger(CPU debugger) {
        this.cpu = debugger;
    }

    public Clock getClock() {
        return this.clock;
    }


    public MMUImpl getMMU() {
        return this.mmuImpl;
    }

    public void load(String path) {
        RomLoader<GameboyRom> romLoader = new RomLoader<>();
        this.rom = romLoader.load(path, GameboyRom.class);
        this.mmuImpl.connect(rom);
    }

    public void load(GameboyRom rom) {
        this.mmuImpl.connect(rom);
    }

    public CPU getCPU() {
        return this.cpu;
    }

    public void load(int[] program) {
        this.rom = new TestRom(program);
        this.mmuImpl.connect(rom);
    }

    /**
     * Set the base values of the registers the same as CoffeeGB
     */
    private void initCoffeeGbStyleRegisters() {
        this.cpu.writeRegister(Registers.AF, new ComputableImpl(0x11B0));
        this.cpu.writeRegister(Registers.BC, new ComputableImpl(0x13));
        this.cpu.writeRegister(Registers.DE, new ComputableImpl(0x0D8));
        this.cpu.writeRegister(Registers.HL, new ComputableImpl(0x14D));
        this.cpu.writeRegister(Registers.SP, new ComputableImpl(0xFFFE));
    }

    public void powerOn() {
        this.cpu.initRegisterStartValues();
        this.run();
    }

    private void run() {
        long maxCyclesPerUpdate = clock.getMaxCyclesPerUpdate();
        do {
            while (clock.getCycle() < maxCyclesPerUpdate) {
                int cycles = 0;
                try {
                    cycles = this.cpu.tick(cycles);
                } catch (NotImplementedException | IllegalAccessException | UnknownOpcodeException | DivergedCPUStateException e) {
                    System.out.println(e.getMessage());
                    e.printStackTrace();

                    return;
                }
                clock.update(cycles);
            }

            this.clock.reset();
            // update screen
        } while (true);
    }

    @Override
    public Display getDisplay() {
        return this.screen.getDisplay();
    }
}
