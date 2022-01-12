package tools.tracing;

public class TraceLine {

    private String[] elements;
    private TraceFormat traceFormat;

    public TraceLine(TraceFormat traceFormat, String line) {
        this.traceFormat = traceFormat;
        this.elements = line.split(traceFormat.getElementSeperator());
    }

    public static String toHex(int val) {
       return String.format("0x%s", Integer.toHexString(val).toUpperCase());
    }
    public static String toHex(String val) {
         int intVal = Integer.parseInt(val);
        return String.format("0x%s", Integer.toHexString(intVal));
    }
    public String getOpcodeCounter() {
        try {
            return this.getElement(this.traceFormat.getOpcodeCounterIndex()).getValue();
        } catch (Exception e) {
            System.out.printf("error: %s%n", e);
            return "";
        }
    }
    public String getOpcode() {
        try {
            return String.format("0x%s", this.getElement(this.traceFormat.getOpcodeIndex()).getValue());
        } catch (Exception e) {
            System.out.printf("error: %s%n", e);
            return "";
        }
    }

    public boolean isTruncated() {
        return this.elements.length < this.traceFormat.getLength();
    }

    public String getPC() {
        try {
            return this.getElement(this.traceFormat.getPCIndex()).getValue();
        } catch (Exception e) {
            System.out.printf("error: %s%n", e);
            return "";
        }
    }

    public TraceElement getElement(int i) {
        String seperator = null;
        try {
            seperator = this.traceFormat.getTraceElementSeperator();
        } catch (Exception e) {
           System.out.printf("error: %s%n", e);
        }



        String[] element = this.elements[i].split(seperator);
        
        String key = element[0];
        String value = element[1];
        return new TraceElement(key, value);
    }

}
