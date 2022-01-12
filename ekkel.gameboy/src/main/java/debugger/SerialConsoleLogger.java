package debugger;

public class SerialConsoleLogger implements SerialDevice {
    @Override
    public void logData(String data) {
        System.out.print(data);
    }
}
