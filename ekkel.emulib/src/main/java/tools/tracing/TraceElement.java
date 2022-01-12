package tools.tracing;

public class TraceElement {

    private final String name;
    private final String value;


    public TraceElement(String name, String value) {
        this.name = name;
        this.value = value;
    }


    public String getName() {
        return this.name;
    }

    public String getValue() {
        return this.value;
    }

}
