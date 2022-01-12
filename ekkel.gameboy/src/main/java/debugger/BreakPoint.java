package debugger;

public class BreakPoint {
    private int pcValue;
    public BreakPoint(int pcValue) {
        this.pcValue = pcValue;
    }

    public int getValue() {
        return this.pcValue;
    }

}
