import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

public class BankingApp {

    // Global Variables fetched from the configuration file
    private static String apiUrl;
    private static String apiKey;
    private static double maxWithdrawalLimit;
    private static double transactionFee;
    private static String databaseUrl;
    private static String dbUser;
    private static String dbPassword;

    // Static block to load configuration from the file
    static {
        try {
            loadConfiguration();
        } catch (IOException e) {
            System.err.println("Error loading configuration: " + e.getMessage());
            System.exit(1); // Exit if configuration cannot be loaded
        }
    }

    // Method to load configuration from a properties file
    private static void loadConfiguration() throws IOException {
        Properties properties = new Properties();
        FileInputStream fis = new FileInputStream("bank_config.properties");
        properties.load(fis);

        // Assign the properties to global variables
        apiUrl = properties.getProperty("api_url");
        apiKey = properties.getProperty("api_key");
        maxWithdrawalLimit = Double.parseDouble(properties.getProperty("max_withdrawal_limit"));
        transactionFee = Double.parseDouble(properties.getProperty("transaction_fee"));
        databaseUrl = properties.getProperty("database_url");
        dbUser = properties.getProperty("database_user");
        dbPassword = properties.getProperty("database_password");

        fis.close(); // Close the file input stream
    }

    // A method to simulate withdrawal processing
    public static void processWithdrawal(double amount) {
        if (amount > maxWithdrawalLimit) {
            System.out.println("Error: Withdrawal amount exceeds the maximum limit of " + maxWithdrawalLimit);
            return;
        }

        // Calculate the transaction fee
        double fee = (amount * transactionFee) / 100;
        double totalAmount = amount + fee;

        System.out.println("Processing withdrawal...");
        System.out.println("Amount: " + amount);
        System.out.println("Transaction Fee: " + fee);
        System.out.println("Total Amount to be Withdrawn: " + totalAmount);
    }

    // A method to simulate fetching account details using the bank API
    public static void fetchAccountDetails(String accountNumber) {
        System.out.println("Fetching account details from API...");
        System.out.println("API URL: " + apiUrl);
        System.out.println("API Key: " + apiKey);
        // Simulate making an API call to fetch account details
        // In a real app, you'd use an HTTP client like HttpURLConnection or HttpClient here
        System.out.println("Account details for account: " + accountNumber);
    }

    // Method to simulate connecting to a database (e.g., to store transaction data)
    public static void connectToDatabase() {
        System.out.println("Connecting to the database...");
        System.out.println("Database URL: " + databaseUrl);
        System.out.println("Database User: " + dbUser);
        // Simulate database connection logic (this would typically use JDBC)
        System.out.println("Connected to the database successfully.");
    }

    // Main method
    public static void main(String[] args) {
        System.out.println("Starting the Banking Application...");

        // Simulate processing a withdrawal
        processWithdrawal(1000);

        // Simulate fetching account details
        fetchAccountDetails("123456789");

        // Simulate connecting to the database
        connectToDatabase();
    }
}
