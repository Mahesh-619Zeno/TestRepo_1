package utils;

public class EnvironmentUtil {

    public static String getEnv(String name, String defaultValue) {
        String value = System.getenv(name);
        if (value == null || value.isEmpty()) {
            Logger.warn("Environment variable '" + name + "' not found. Using default value: '" + defaultValue + "'");
            return defaultValue;
        }
        return value;
    }

    public static String getRequiredEnv(String name) {
        String value = System.getenv(name);
        if (value == null || value.isEmpty()) {
            throw new RuntimeException("Required environment variable '" + name + "' is not set.");
        }
        return value;
    }

    public static int getIntEnv(String name, int defaultValue) {
        String value = System.getenv(name);
        if (value == null || value.isEmpty()) {
            return defaultValue;
        }
        try {
            return Integer.parseInt(value);
        } catch (NumberFormatException e) {
            Logger.error("Environment variable '" + name + "' has an invalid integer format: '" + value + "'. Using default value: " + defaultValue);
            return defaultValue;
        }
    }

    public static boolean getBooleanEnv(String name, boolean defaultValue) {
        String value = System.getenv(name);
        if (value == null || value.isEmpty()) {
            return defaultValue;
        }
        return value.equalsIgnoreCase("true") || value.equalsIgnoreCase("1");
    }
}