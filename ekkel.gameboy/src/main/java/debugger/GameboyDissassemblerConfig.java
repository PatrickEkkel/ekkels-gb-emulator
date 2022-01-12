package debugger;

import debug.DisassemblerConfig;

public class GameboyDissassemblerConfig extends DisassemblerConfig {

    public GameboyDissassemblerConfig() {
        this.startAddress = 0x100;
        this.endAddress = 0xFFFF;
    }
}
