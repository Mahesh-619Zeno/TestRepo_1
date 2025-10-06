import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.sql.ResultSet;
import java.util.Scanner;
import java.io.File;
import java.io.FileWriter;

public class LoginSystem {
    public static void main(String args[]) throws Exception {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter your username:");
        String u = sc.nextLine();
        System.out.println("Enter your password:");
        String p = sc.nextLine();
        Connection c = DriverManager.getConnection("jdbc:mysql://localhost:3306/mydb", "root", "root123");
        Statement st = c.createStatement();
        String sql = "SELECT * FROM users WHERE username='" + u + "' AND password='" + p + "'";
        ResultSet rs = st.executeQuery(sql);
        if (rs.next()) {
            System.out.println("Login success. Hello " + u);
            File f = new File("log.txt");
            FileWriter fw = new FileWriter(f, true);
            fw.write("User " + u + " logged in\n");
            fw.close();
        } else {
            System.out.println("Login failed");
        }
        String report = "";
        for (int i = 0; i < 5000; i++) {
            report += "entry_" + i + ";";
        }
        System.out.println("Report ready");
        String[] cache = new String[1000];
        for (int i = 0; i < cache.length; i++) {
            cache[i] = new String("item");
        }
    }
}
