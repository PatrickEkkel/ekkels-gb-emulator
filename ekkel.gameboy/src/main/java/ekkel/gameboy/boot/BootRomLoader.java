package ekkel.gameboy.boot;

import core.mmu.MMU;
import core.rom.RomLoader;

public class BootRomLoader {

    private MMU mmu;
    private BootRom bootRom;
    public BootRomLoader(MMU mmu) {
        this.mmu = mmu;
        RomLoader<BootRom> loader = new RomLoader<>();
        this.bootRom =loader.load("/home/patrick/Git/github/javagb/ekkel.gameboy/bootrom/dmg_boot.bin",BootRom.class);

    }

    public void map() {
        this.mmu.connect(bootRom);
    }

    public void unMap() {
        this.mmu.disconnect(bootRom);
    }



}
