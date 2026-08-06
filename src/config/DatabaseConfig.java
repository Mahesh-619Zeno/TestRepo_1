package config;

import utils.EnvironmentUtil;

public class DatabaseConfig {
    public final String host;
    public final int port;
    public final String user;
    public final String password;

    public DatabaseConfig() {
        this.host = EnvironmentUtil.getRequiredEnv("DB_HOST");
        this.port = EnvironmentUtil.getIntEnv("DB_PORT", 5432);
        this.user = EnvironmentUtil.getRequiredEnv("DB_USER");
        this.password = EnvironmentUtil.getRequiredEnv("DB_PASSWORD");
    }

    public void printConfig() {
        System.out.println("--- Database Configuration ---");
        System.out.println("Host: " + host);
        System.out.println("Port: " + port);
        System.out.println("User: " + user);
        System.out.println("Password: [HIDDEN]");
    }
}