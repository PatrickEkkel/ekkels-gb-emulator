package debug;

import core.cpu.CPU;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.opcodes.exceptions.UnknownOpcodeException;
import core.mmu.MMU;
import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;
import core.mmu.memorymap.MemoryMap;
import core.mmu.memorymap.exceptions.MemoryRegionDescriptionNotFound;

import java.util.ArrayList;
import java.util.List;

/**
 * Generic dissasembler that interfaces with the emulib to generate a mapping that can be used for the debugger
 */
public class Disassembler {

    private MMU mmu;
    private CPU cpu;
    private List<String[]> rows;

    public Disassembler(MMU mmu, CPU cpu) {
        this.mmu = mmu;
        this.cpu = cpu;
        this.rows = new ArrayList<>();
    }


    public List<String[]> getRows() {
        return this.rows;
    }


    public void run(DisassemblerConfig config) throws MemoryRegionDescriptionNotFound, NotImplementedException, IllegalAccessException, UnknownOpcodeException {
        // should retrieve the entire memorymap from all connected components
        MemoryMap memoryMap = this.cpu.getMemoryMap();

        int start = config.getStartAddress();
        int end = config.getEndAddress();
        this.cpu.setPC(start);
        while(this.cpu.getPC() < end) {
            String [] row = new String[4];
            MemoryAddress memoryAddress = MemoryAddress.fromValue(this.cpu.getPC());
            row[0] = memoryMap.getMemoryRegionDescription(memoryAddress);
            row[1] = memoryAddress.toString();

            int instructionLength = 1;
            if(memoryMap.isData(memoryAddress)) {
                MemoryValue memoryValue = mmu.read(memoryAddress);
                row[2] =  memoryValue.toString();
            } else {
                Opcode opcode = this.cpu.getFetcher().fetch().decode();
                opcode.dryRun();
                instructionLength = opcode.toBinary().length;

            // decode instruction
                if(instructionLength > 0) {
                    row[2] = String.format("0x%s", Integer.toHexString(opcode.toBinary()[0]));

                    if (instructionLength == 2) {
                        row[2] += ", " + String.format("0x%s", Integer.toHexString(opcode.toBinary()[1]));
                    }
                    if (instructionLength == 3) {
                        row[2] += ", " + String.format("0x%s", Integer.toHexString(opcode.toBinary()[2]));
                    }
                }
                else {
                    row[2] = "NAN";
                }
                row[3] = opcode.toString();
            }

            // instruction with one parameter


            this.rows.add(row);
            this.cpu.setPC(this.cpu.getPC() + instructionLength);
        }

    }
}
