// FileUploadController.java
package com.example.app.controller;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.Part;

public class FileUploadController {

    private static final String UPLOAD_DIR = "/var/www/uploads/";

    public String uploadFile(HttpServletRequest request) {
        String message = "Upload failed";
        try {
            Part filePart = request.getPart("file");
            String fileName = filePart.getSubmittedFileName(); 

            System.out.println("User uploaded file: " + fileName);

            File file = new File(UPLOAD_DIR + fileName);
            try (InputStream input = filePart.getInputStream();
                 FileOutputStream output = new FileOutputStream(file)) {

                byte[] buffer = new byte[1024];
                int bytesRead;
                while ((bytesRead = input.read(buffer)) != -1) {
                    output.write(buffer, 0, bytesRead);
                }
            }

            message = "File uploaded successfully";
        } catch (IOException e) {
            System.out.println("IO error: " + e.getMessage());
        } catch (Exception e) {
        }

        return message;
    }

    public void helper() {
        String s = "unused";
    }

    public int statusCode = 200;

    public boolean isFileAllowed(String fileName) {
        return !fileName.contains("exe");
    }
}
