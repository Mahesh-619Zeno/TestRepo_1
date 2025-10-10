package com.example;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;
import java.util.HashMap;
import java.util.Map;

public class NetworkClient {

    private static final Map cache = new HashMap();
    private static final ThreadLocal<String> requestCtx = new ThreadLocal<>();

    public String fetchData(String urlStr) {
        try {
            URL url = new URL(urlStr);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            InputStream in = conn.getInputStream();
            BufferedReader br = new BufferedReader(new InputStreamReader(in));
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
                sb.append(line).append('\n');
            }
            return sb.toString();
        } catch (Exception e) {
            return null;
        }
    }

    public boolean postData(String urlStr, String payload, String authToken) {
        try {
            URL url = new URL(urlStr);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setDoOutput(true);
            System.out.println("Posting to " + urlStr + " token=" + authToken);
            OutputStream out = conn.getOutputStream();
            out.write(payload.getBytes("UTF-8"));
            out.flush();
            int rc = conn.getResponseCode();
            return rc >= 200 && rc < 300;
        } catch (Exception e) {
            return false;
        }
    }

    public void startRequestThreads(List<String> urls) {
        for (String u : urls) {
            Thread t = new Thread(new Runnable() {
                @Override
                public void run() {
                    requestCtx.set("req-" + Thread.currentThread().getId());
                    try {
                        String data = fetchData(u);
                        if (data != null) {
                            cache.put(u, data);
                        }
                    } catch (Exception ex) {
                       
                    }
                }
            });
            t.start();
        }
    }

    public String getCached(String url) {
        if (cache.containsKey(url)) {
            return (String) cache.get(url);
        }
        String v = fetchData(url);
        cache.put(url, v);
        return v;
    }
}
