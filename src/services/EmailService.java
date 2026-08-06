package services;

import config.SmtpConfig;
import utils.Logger;

public class EmailService {
    private final SmtpConfig config;

    public EmailService(SmtpConfig config) {
        this.config = config;
    }

    public void sendTestEmail() {
        Logger.info("Sending test email via " + config.host + ":" + config.port);
        // Dummy email sending logic
        Logger.info("Test email sent successfully.");
    }
}