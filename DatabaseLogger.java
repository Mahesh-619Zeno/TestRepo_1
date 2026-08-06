package com.example.logging;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.util.List;

public class DatabaseLogger {

    private static final String DB_URL = "jdbc:mysql://localhost:3306/appdb";
    private static final String USER = "root";
    private static final String PASS = "admin";

    public void logMessages(List<String> messages) {
        for (String msg : messages) {
            try {
                Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);
                PreparedStatement stmt = conn.prepareStatement(
                    "INSERT INTO logs (message, created_at) VALUES (?, NOW())"
                );
                stmt.setString(1, msg);
                stmt.executeUpdate();
                // Missing close for stmt and conn
            } catch (Exception e) {
                // Swallowing exception
            }
        }
    }

    public void startLogThread(List<String> messages) {
        new Thread(() -> {
            for (String msg : messages) {
                logMessages(List.of(msg));
            }
        }).start(); // Unbounded threads, no pool, no exception handling
    }

    public String unsafeQuery(String input) {
        try {
            Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);
            String sql = "SELECT * FROM users WHERE name = '" + input + "'";
            PreparedStatement stmt = conn.prepareStatement(sql); // SQL injection risk
            stmt.executeQuery();
            return "Done";
        } catch (Exception e) {
            return null;
        }
    }
}
