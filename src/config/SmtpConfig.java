package config;

import utils.EnvironmentUtil;

public class SmtpConfig {
    public final String host;
    public final int port;
    public final String username;
    public final String password;
    public final boolean useTls;

    public SmtpConfig() {
        this.host = EnvironmentUtil.getRequiredEnv("SMTP_HOST");
        this.port = EnvironmentUtil.getIntEnv("SMTP_PORT", 587);
        this.username = EnvironmentUtil.getRequiredEnv("SMTP_USERNAME");
        this.password = EnvironmentUtil.getRequiredEnv("SMTP_PASSWORD");
        this.useTls = EnvironmentUtil.getBooleanEnv("SMTP_USE_TLS", true);
    }

    public void printConfig() {
        System.out.println("--- SMTP Configuration ---");
        System.out.println("Host: " + host);
        System.out.println("Port: " + port);
        System.out.println("Username: " + username);
        System.out.println("Password: [HIDDEN]");
        System.out.println("Use TLS: " + useTls);
    }
}