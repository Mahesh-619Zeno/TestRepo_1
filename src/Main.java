import config.*;
import services.*;
import utils.Logger;

public class Main {
    public static void main(String[] args) {
        Logger.info("Starting application...");
        
        try {
            // Load and display all configurations
            AppConfig appConfig = new AppConfig();
            DatabaseConfig dbConfig = new DatabaseConfig();
            SmtpConfig smtpConfig = new SmtpConfig();
            ApiConfig apiConfig = new ApiConfig();
            
            appConfig.printConfig();
            dbConfig.printConfig();
            smtpConfig.printConfig();
            apiConfig.printConfig();
            
            // Use services that depend on the configuration
            DatabaseService dbService = new DatabaseService(dbConfig);
            dbService.connect();
            
            EmailService emailService = new EmailService(smtpConfig);
            emailService.sendTestEmail();
            
            ApiClient apiClient = new ApiClient(apiConfig);
            apiClient.fetchData();

            Logger.info("Application finished successfully.");
            
        } catch (Exception e) {
            Logger.error("Application failed with an error: " + e.getMessage());
            System.exit(1);
        }
    }
}