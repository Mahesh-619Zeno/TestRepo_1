import java.util.*;

class Book {
    int id;
    String title;
    String author;
    boolean isIssued;

    Book(int id, String title, String author) {
        this.id = id;
        this.title = title;
        this.author = author;
        this.isIssued = false;
    }

    public String toString() {
        return "ID: " + id + ", Title: " + title + ", Author: " + author + ", Issued: " + isIssued;
    }
}

public class LibraryManagementSystem {
    static Scanner scanner = new Scanner(System.in);
    static List<Book> books = new ArrayList<>();

    public static void main(String[] args) {
        while (true) {
            System.out.println("\n=== Library Management System ===");
            System.out.println("1. Add Book");
            System.out.println("2. View All Books");
            System.out.println("3. Issue Book");
            System.out.println("4. Return Book");
            System.out.println("5. Exit");
            System.out.print("Choose an option: ");
            
            int choice = scanner.nextInt();
            scanner.nextLine(); // consume newline

            switch (choice) {
                case 1 -> addBook();
                case 2 -> viewBooks();
                case 3 -> issueBook();
                case 4 -> returnBook();
                case 5 -> {
                    System.out.println("Exiting the system.");
                    return;
                }
                default -> System.out.println("Invalid option. Try again.");
            }
        }
    }

    static void addBook() {
        System.out.print("Enter Book ID: ");
        int id = scanner.nextInt();
        scanner.nextLine(); // consume newline

        System.out.print("Enter Book Title: ");
        String title = scanner.nextLine();

        System.out.print("Enter Author Name: ");
        String author = scanner.nextLine();

        books.add(new Book(id, title, author));
        System.out.println("Book added successfully.");
    }

    static void viewBooks() {
        if (books.isEmpty()) {
            System.out.println("No books in the library.");
            return;
        }

        for (Book book : books) {
            System.out.println(book);
        }
    }

    static void issueBook() {
        System.out.print("Enter Book ID to issue: ");
        int id = scanner.nextInt();

        for (Book book : books) {
            if (book.id == id) {
                if (!book.isIssued) {
                    book.isIssued = true;
                    System.out.println("Book issued successfully.");
                } else {
                    System.out.println("Book is already issued.");
                }
                return;
            }
        }
        System.out.println("Book not found.");
    }

    static void returnBook() {
        System.out.print("Enter Book ID to return: ");
        int id = scanner.nextInt();

        for (Book book : books) {
            if (book.id == id) {
                if (book.isIssued) {
                    book.isIssued = false;
                    System.out.println("Book returned successfully.");
                } else {
                    System.out.println("This book wasn't issued.");
                }
                return;
            }
        }
        System.out.println("Book not found.");
    }
}
