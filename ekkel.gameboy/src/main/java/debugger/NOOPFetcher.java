package debugger;

import core.cpu.CPU;
import core.cpu.opcodes.Decoder;
import core.cpu.opcodes.Fetcher;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.Computable;
import core.mmu.MMU;
import ekkel.gameboy.cpu.sharpLR35902.decoders.StandardDecoder;

public class NOOPFetcher extends Fetcher {
    private Decoder decoder;
    private CPU cpu;
    public NOOPFetcher(MMU mmuImpl, CPU cpu) {
        super(mmuImpl, cpu, null);
        this.cpu = cpu;
        this.decoder = new StandardDecoder(cpu,mmuImpl);
    }

    @Override
    public Decoder fetch() throws NotImplementedException, IllegalAccessException {
        /*
            Let the CPU loop endlessy between 0x100 and 0x200 by doing NOP
         */
        Computable c = this.cpu.readRegister(Registers.PC);

        if(c.getValue() == 0x200) {
            this.cpu.readRegister(Registers.PC).setValue(0x100);
        }


        this.decoder.setOpcode(0x00);
        return decoder;
    }
}
