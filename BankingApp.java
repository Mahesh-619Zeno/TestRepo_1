import java.util.Scanner;

public class BankingApp {

    // Global (instance) variables
    private String accountHolderName;
    private double accountBalance;

    // Static (class-level) variable - shared among all instances of the class
    private static int totalAccounts = 0;

    // Constructor to initialize the account details
    public BankingApp(String accountHolderName, double initialDeposit) {
        this.accountHolderName = accountHolderName;
        this.accountBalance = initialDeposit;
        totalAccounts++;  // Increment total account count whenever a new account is created
    }

    // Instance method to deposit money
    public void deposit(double amount) {
        if (amount > 0) {
            accountBalance += amount;
            System.out.println("Deposited: $" + amount);
        } else {
            System.out.println("Invalid deposit amount.");
        }
    }

    // Instance method to withdraw money
    public void withdraw(double amount) {
        if (amount > 0 && amount <= accountBalance) {
            accountBalance -= amount;
            System.out.println("Withdrew: $" + amount);
        } else {
            System.out.println("Insufficient funds or invalid withdrawal amount.");
        }
    }

    // Instance method to check the balance
    public void checkBalance() {
        System.out.println(accountHolderName + "'s Account Balance: $" + accountBalance);
    }

    // Static method to get the total number of accounts
    public static void totalAccounts() {
        System.out.println("Total Accounts in the Bank: " + totalAccounts);
    }

    // Main method to drive the program
    public static void main(String[] args) {
        // Scanner for user input
        Scanner scanner = new Scanner(System.in);

        // Prompt the user for account creation
        System.out.print("Enter Account Holder's Name: ");
        String name = scanner.nextLine();
        System.out.print("Enter Initial Deposit: ");
        double depositAmount = scanner.nextDouble();

        // Create a new bank account
        BankingApp account = new BankingApp(name, depositAmount);

        // Show initial balance
        account.checkBalance();

        // Banking operations menu
        boolean running = true;
        while (running) {
            System.out.println("\n--- Banking Menu ---");
            System.out.println("1. Deposit");
            System.out.println("2. Withdraw");
            System.out.println("3. Check Balance");
            System.out.println("4. View Total Accounts");
            System.out.println("5. Exit");
            System.out.print("Select an option: ");
            int choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    System.out.print("Enter deposit amount: ");
                    double deposit = scanner.nextDouble();
                    account.deposit(deposit);
                    break;
                case 2:
                    System.out.print("Enter withdrawal amount: ");
                    double withdrawal = scanner.nextDouble();
                    account.withdraw(withdrawal);
                    break;
                case 3:
                    account.checkBalance();
                    break;
                case 4:
                    BankingApp.totalAccounts();  // Call static method to get total accounts
                    break;
                case 5:
                    running = false;
                    System.out.println("Thank you for using the Banking App!");
                    break;
                default:
                    System.out.println("Invalid option, please try again.");
            }
        }

        scanner.close();
    }
}
