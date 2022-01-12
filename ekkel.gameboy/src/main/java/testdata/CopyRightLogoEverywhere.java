package testdata;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.MMU;
import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;

import java.util.HashMap;

public class CopyRightLogoEverywhere {
    private MMU mmu;
    public CopyRightLogoEverywhere(MMU mmu) {
        this.mmu = mmu;
    }


    public void writeVram(int [] values,int start) throws NotImplementedException {
        int addressVram = start;

        for(int i=0;i<values.length;i++) {
            mmu.write(MemoryAddress.fromValue(addressVram), MemoryValue.fromValue(values[i]));
            addressVram += 1;
        }
    }

    public void loadTestData() throws NotImplementedException {

        HashMap<Integer,int[]> bgMap = new HashMap<>() {
            {
                put(0x9800,new int[] {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00});
                put(0x9810,new int[] {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00});
                put(0x9820,new int[] {0x50,0x00,0x00,0x50,0x50,0x50,0x00,0x00,0x00,0x00,0x50,0x00,0x00,0x00,0x00,0x50});
                put(0x9830,new int[] {0x50,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00});
                put(0x9840,new int[] {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00});
                put(0x9850,new int[] {0x50,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x50});
                put(0x9860,new int[] {0x50,0x50,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00});
                put(0x9870,new int[] {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00});
                put(0x9880,new int[] {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00});
                put(0x9890,new int[] {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00});
                put(0x98A0,new int[] {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00});
                put(0x98B0,new int[] {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00});
                put(0x98C0,new int[] {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00});
                put(0x98D0,new int[] {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00});
                put(0x98E0,new int[] {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00});
                put(0x98F0,new int[] {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00});
                put(0x9900,new int[] {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00});
                put(0x9910,new int[] {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00});
                put(0x9920,new int[] {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00});
                put(0x9930,new int[] {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00});
            }
        };
        for(int x=0x9800;x<0x9940;x+=16) {
            writeVram(bgMap.get(x),x);
        }


        int [] P = new int [] {0x7C,0x7C,0x66,0x66,0x66,0x66,0x7C,0x7C,0x60,0x60,0x60,0x60,0x60,0x60,0x00,0x00};
        int [] A =new int [] {0x66,0x66,0x66,0x66,0x66,0x66,0x66,0x66,0x3C,0x3C,0x3C,0x3C,0x18,0x18,0x00,0x00};

        writeVram(P,0x8500);


          //  writeVram(tiles.get(x),x);
    }



}
