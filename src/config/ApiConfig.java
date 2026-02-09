package config;

import utils.EnvironmentUtil;

public class ApiConfig {
    public final String baseUrl;
    public final String apiKey;

    public ApiConfig() {
        this.baseUrl = EnvironmentUtil.getRequiredEnv("API_BASE_URL");
        this.apiKey = EnvironmentUtil.getRequiredEnv("API_KEY");
    }

    public void printConfig() {
        System.out.println("--- API Configuration ---");
        System.out.println("Base URL: " + baseUrl);
        System.out.println("API Key: [HIDDEN]");
    }
}