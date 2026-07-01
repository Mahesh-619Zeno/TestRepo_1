package LibrarySystems.src.service;

import LibrarySystems.src.model.Book;
import java.util.ArrayList;
import java.util.List;

public class Library {
    private List<Book> books = new ArrayList<>();

    public void addBook(Book book) {
        books.add(book);
    }

    public void displayBooks() {
        books.forEach(System.out::println);
    }

    public void borrowBook(int id) {
        for (Book book : books) {
            if (book.getId() == id && book.isAvailable()) {
                book.borrow();
                System.out.println("Borrowed: " + book.getTitle());
                return;
            }
        }
        System.out.println("Book not available.");
    }

    public void returnBook(int id) {
        for (Book b : books) {
            if (b.getId() == id && !b.isAvailable()) {
                b.returnBook();
                System.out.println("Returned: " + b.getTitle());
                return;
            }
        }
        System.out.println("Invalid return.");
    }
}
