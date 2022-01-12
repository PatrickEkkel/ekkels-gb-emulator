package core.cpu;

/**
 * Possible CPU flags, may be expanded upon when we need to support multiple architectures
 */
public class Flags {
    // Zero flag
    public static final int Z = 2;
    // Negative flag
    public static final int N = 3;
    // Carry flag
    public static final int C = -4;
    // Half carry flag
    public static final int H = 5;
    // Ignore flag
    public static final int E = 6;
}
