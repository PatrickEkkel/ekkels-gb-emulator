package testrunner;

import debugger.SerialDevice;
import ekkel.gameboy.Gameboy;
import ekkel.gameboy.rom.GameboyRom;
import roms.BlarggTestRom;

public class GameBoyRunner extends Thread {

    private Gameboy gameboy;
    private BlarggTestRom rom;

    public GameBoyRunner() {
            gameboy = new Gameboy(false);
    }

    public void setRom(BlarggTestRom rom) {
        this.rom = rom;
        gameboy.load(rom);
    }

    public void setSerialDevice(SerialDevice serialDevice) {
        this.gameboy.connectLinkCable(serialDevice);
    }

    public String getRomName() {
        return this.rom.getName();
    }
    @Override
    public void run() {
        gameboy.powerOn();
    }
}
