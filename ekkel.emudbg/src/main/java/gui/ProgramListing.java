package gui;

import javax.swing.*;

public class ProgramListing extends AppComponent {

    public String[] getColumns() {
        return new String[]{"MEMRANGE", "ADDRESS", "HEX", "OPCODE"};
    }

    public String[] printNop() {
        return new String[]{"ROM0", "0x11AA", "0x00", "NOP"};
    }

    public ProgramListing() {
        // this.setSize(500, 500);

        String data[][] = new String[100][];

        String column[] = getColumns();


        for (int i = 0; i < 100; i++) {
            data[i] = printNop();
        }

        JTable jt = new JTable(data, column);
        jt.setShowGrid(false);
        jt.setBounds(0, 0, 300, 800);
        JScrollPane sp = new JScrollPane(jt);

        this.add(sp);

    }
}
