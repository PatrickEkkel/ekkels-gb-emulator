package core.device;

import core.cpu.CPU;
import core.mmu.MMU;

public interface SimpleDevice {

    CPU getCPU();
    MMU getMMU();
}
