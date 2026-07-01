import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

public class InventoryManager {

    // Global variables
    static String inventoryName;
    static double itemPrice;
    static int totalItems;

    public static void main(String[] args) {
        // Load configuration from the properties file
        loadConfig();

        // Display the inventory information
        displayInventory();

        // Add items to the inventory
        addItems(50);

        // Sell some items and display the updated inventory
        sellItems(30);

        // Check the current inventory status
        displayInventory();
    }

    // Function to load configuration from the properties file
    public static void loadConfig() {
        Properties prop = new Properties();
        try (FileInputStream input = new FileInputStream("config.properties")) {
            // Load the configuration file
            prop.load(input);

            // Set global variables from the config file
            inventoryName = prop.getProperty("inventoryName");
            itemPrice = Double.parseDouble(prop.getProperty("itemPrice"));
            totalItems = Integer.parseInt(prop.getProperty("totalItems"));

        } catch (IOException ex) {
            System.err.println("Error loading config file: " + ex.getMessage());
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
