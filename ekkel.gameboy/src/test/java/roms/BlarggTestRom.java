package roms;

import ekkel.gameboy.rom.GameboyRom;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;

public class BlarggTestRom extends GameboyRom {

    protected final String romBasePath = "/tmp/testroms/cpu_instrs/individual";
    private String name;

    public String getRomFilePath(String filename) {
        return String.format("%s/%s", romBasePath, filename);
    }

    protected void load(String filename) throws IOException {
        InputStream inputStream = new FileInputStream(getRomFilePath(filename));
        this.setRomContents(inputStream.readAllBytes());
        this.name = filename;
    }

    public String getName() {
        return this.name;
    }

    public BlarggTestRom() {

    }

}
