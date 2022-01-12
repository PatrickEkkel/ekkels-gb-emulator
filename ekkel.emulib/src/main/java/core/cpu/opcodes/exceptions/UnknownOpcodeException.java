package core.cpu.opcodes.exceptions;

public class UnknownOpcodeException extends Exception{

    public UnknownOpcodeException(String message) {
        super(message);
    }
}
