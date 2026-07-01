package LibrarySystems.src.main;


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
        for (Book book : books) {
            if (book.getId() == id && !book.isAvailable()) {
                book.returnBook();
                System.out.println("Returned: " + book.getTitle());
                return;
            }
        }
        System.out.println("Invalid return.");
    }
}

