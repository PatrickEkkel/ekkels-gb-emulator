package tools.tracing;

import java.util.ArrayList;
import java.util.List;

public class TraceComparator {

    private List<String> differences;
    private TraceFormat traceFormat;
    public TraceComparator(TraceFormat traceFormat) {
        this.differences = new ArrayList<>();
        this.traceFormat = traceFormat;
    }



    public boolean compare(TraceFile current, TraceFile expected) {

        TraceLine currentLine = current.getNextLine();
        TraceLine expectedLine = expected.getNextLine();
        boolean result = true;

        for(int i=this.traceFormat.getStartOffset();i<traceFormat.getLength();i++) {
            if(i != this.traceFormat.getLength()) {
                String currentElement = currentLine.getElement(i).getName();
                String expectedElementValue = expectedLine.getElement(i).getValue();
                String currentElementValue = currentLine.getElement(i).getValue();
                if(!currentElementValue.equals(expectedElementValue)) {
                    String messageString = String.format("Difference found on: %s at instruction %s expected %s but got %s at %s",
                            currentElement, currentLine.getOpcodeCounter(), expectedElementValue, currentElementValue, currentLine.getPC());
                    this.differences.add(messageString);
                    result = false;
                }
            }
        }
        return result;
    }


    public List<String> getResults() {
        return this.differences;
    }


}
