
public class Logger {
    public static void info(String message) {
        System.out.println("[INFO] " + message.replace('\n', '_').replace('\r', '_'));
    }

    public static void warn(String message) {
        System.out.println("[WARN] " + message.replace('\n', '_').replace('\r', '_'));
    }

    public static void error(String message) {
        System.err.println("[ERROR] " + message.replace('\n', '_').replace('\r', '_'));
    }
}