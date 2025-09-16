import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

public class InventoryManagerWithUserPreferences {

    // Global variables for inventory
    static String inventoryName;
    static double itemPrice;
    static int totalItems;

    // Global variables for user preferences
    static String language;
    static String theme;
    static boolean notifications;

    public static void main(String[] args) {
        // Load configuration from the properties files
        loadInventoryConfig();
        loadUserPreferencesConfig();

        // Display the inventory information
        displayInventory();

        // Display user preferences
        displayUserPreferences();

        // Add items to the inventory
        addItems(50);

        // Sell some items and display the updated inventory
        sellItems(30);

        // Check the current inventory status
        displayInventory();
    }

    // Function to load inventory configuration from the properties file
    public static void loadInventoryConfig() {
        Properties prop = new Properties();
        try (FileInputStream input = new FileInputStream("config.properties")) {
            // Load the configuration file
            prop.load(input);

            // Set global variables from the config file
            inventoryName = prop.getProperty("inventoryName");
            itemPrice = Double.parseDouble(prop.getProperty("itemPrice"));
            totalItems = Integer.parseInt(prop.getProperty("totalItems"));

        } catch (IOException ex) {
            System.err.println("Error loading inventory config file: " + ex.getMessage());
            System.exit(1); // Exit if there is an error reading the config file
        }
    }

    // Function to load user preferences configuration from the properties file
    public static void loadUserPreferencesConfig() {
        Properties prop = new Properties();
        try (FileInputStream input = new FileInputStream("userpreferences.properties")) {
            // Load the user preferences config file
            prop.load(input);

            // Set global variables from the user preferences config file
            language = prop.getProperty("language");
            theme = prop.getProperty("theme");
            notifications = Boolean.parseBoolean(prop.getProperty("notifications"));

        } catch (IOException ex) {
            System.err.println("Error loading user preferences config file: " + ex.getMessage());
            System.exit(1); // Exit if there is an error reading the config file
        }
    }

    // Function to display the current inventory status
    public static void displayInventory() {
        System.out.println("Inventory at " + inventoryName + ":");
        System.out.println("Total items: " + totalItems);
        System.out.println("Price per item: $" + itemPrice);
        System.out.println("Total inventory value: $" + (totalItems * itemPrice));
    }

    // Function to display user preferences
    public static void displayUserPreferences() {
        System.out.println("User Preferences:");
        System.out.println("Language: " + language);
        System.out.println("Theme: " + theme);
        System.out.println("Notifications Enabled: " + (notifications ? "Yes" : "No"));
    }

    // Function to add items to the inventory
    public static void addItems(int itemsToAdd) {
        totalItems += itemsToAdd;  // Increase the total items
        System.out.println("Added " + itemsToAdd + " items to the inventory.");
    }

    // Function to sell items and update the inventory
    public static void sellItems(int itemsSold) {
        if (itemsSold <= totalItems) {
            totalItems -= itemsSold;  // Decrease the total items
            System.out.println("Sold " + itemsSold + " items.");
        } else {
            System.out.println("Not enough items in inventory to sell.");
        }
    }
}
