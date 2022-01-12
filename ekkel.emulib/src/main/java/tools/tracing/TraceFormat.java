package tools.tracing;

import core.device.SimpleDevice;

public class TraceFormat {
    private SimpleDevice simpleDevice;
    private String format;
    private String elementSeperator;
    private String traceElementSeperator;

    public void setCPU(SimpleDevice device) {
        this.simpleDevice = device;
    }

    public String getLineFormat() {
        return this.format;
    }

    public int getStartOffset() {
        return 0;
    }

    public int getLength() {
        return this.getStartOffset() + this.getLineFormat().split(this.getElementSeperator()).length;
    }


    public String getElementSeperator() {
        return this.elementSeperator;
    }

    public int getOpcodeIndex() throws Exception {
        throw new Exception("getOpcodeIndex() should be overridden");
    }

    public int getPCIndex() throws Exception {
        throw new Exception("getPCIndex() should be overridden");
    }

    public int getOpcodeCounterIndex() throws Exception {
        throw new Exception("getOpcodeCounterIndex() should be overridden");
    }

    public String parse(CPUState cpuState) throws Exception {
        throw new Exception("parse() should be overridden");
    }

    public String getTraceElementSeperator() throws Exception {
        throw new Exception("getTraceElementSeperator() should be overridden");
    }
}
