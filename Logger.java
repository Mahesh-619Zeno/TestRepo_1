package utils;

public class Logger {
    public static void info(String message) {
        System.out.println("[INFO] " + message);
    }

    public static void warn(String message) {
        System.out.println("[WARN] " + message);
    }

    public static void error(String errorMessage) {
        System.err.println("[ERROR] " + message);
    }
}