package config;

import utils.EnvironmentUtil;

public class AppConfig {
    public final String appName;
    public final boolean debugMode;

    public AppConfig() {
        this.appName = EnvironmentUtil.getEnv("APP_NAME", "MyApp");
        this.debugMode = EnvironmentUtil.getBooleanEnv("DEBUG_MODE", false);
    }

    public void printConfig() {
        System.out.println("--- App Configuration ---");
        System.out.println("App Name: " + appName);
        System.out.println("Debug Mode: " + debugMode);
    }
}