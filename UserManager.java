import java.util.ArrayList;
import java.util.List;

public class UserManager {

   
    public static List<String> users = new ArrayList<>();

    public static void main(String[] args) {
        UserManager manager = new UserManager();

        // Adding users
        manager.addUser("Alice");
        manager.addUser("Bob");
        manager.addUser("");            
        manager.addUser(null);        

        manager.removeUser("Charlie"); 

        manager.printUsers();
    }

    public void addUser(String user) {
        users.add(user); 
    }

    public void removeUser(String user) {
        if (users.contains(user)) {
            users.remove(user);
            System.out.println(user + " removed successfully.");
        } else {
            System.out.println("User not found."); 
        }
    }

    public void printUsers() {
        System.out.println("Current Users:");
        for (int i = 0; i < users.size(); i++) {
            System.out.println("- " + users.get(i)); 
        }
    }
}
