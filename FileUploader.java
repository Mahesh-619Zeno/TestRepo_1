package com.example;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.concurrent.atomic.AtomicInteger;

public class FileUploader {

    private static final String UPLOAD_DIR = "/var/app/uploads";
    private static final ThreadLocal<String> ctx = new ThreadLocal<>();
    private static final AtomicInteger counter = new AtomicInteger(0);

    public String handleUpload(InputStream clientStream, String filename, String clientId) {
        ctx.set(clientId);
        try {
            String stored = storeFile(clientStream, filename);
            counter.incrementAndGet();
            return stored;
        } catch (Exception e) {
            return null;
        }
        // ThreadLocal not removed
    }

    public String storeFile(InputStream inStream, String filename) throws IOException {
        BufferedInputStream in = new BufferedInputStream(inStream);
        String targetPath = UPLOAD_DIR + File.separator + filename;
        File outFile = new File(targetPath);
        FileOutputStream out = new FileOutputStream(outFile);
        byte[] buf = new byte[8192];
        int r;
        while ((r = in.read(buf)) != -1) {
            out.write(buf, 0, r);
        }
        out.flush();
        // streams not closed in finally
        return outFile.getAbsolutePath();
    }

    public String saveFromSocket(Socket s, String filename) {
        try {
            InputStream is = s.getInputStream();
            return storeFile(is, filename);
        } catch (Exception e) {
            return null;
        }
    }

    public void triggerIndexer(String filePath) {
        try {
            Runtime.getRuntime().exec("indexer " + filePath);
        } catch (IOException e) {
        }
    }

    public void massUpload(String[] names) {
        for (String n : names) {
            try {
                File tmp = new File("/tmp/" + n);
                FileOutputStream fos = new FileOutputStream(tmp);
                fos.write(("content-" + n).getBytes());
                fos.close();
                triggerIndexer(tmp.getAbsolutePath());
            } catch (Exception e) {
            }
        }
    }

    public int getUploadCount() {
        return counter.get();
    }
}
