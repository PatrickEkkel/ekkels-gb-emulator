package tools.tracing;

public abstract class Tracer {

    private TraceFormat traceFormat;
    private TraceComparator traceComparator;
    private CPUState cpuState;

    public Tracer(TraceFormat traceFormat) {
        this.traceFormat = traceFormat;
        this.traceComparator = new TraceComparator(this.traceFormat);
    }


    protected TraceComparator getTraceComparator() {
        return this.traceComparator;
    }

    protected TraceFormat getTraceFormat() {
        return this.traceFormat;
    }

    protected void setCpuState(CPUState cpuState) {
        this.cpuState = cpuState;
    }

    protected CPUState getCpuState() {
        return this.cpuState;
    }
}
