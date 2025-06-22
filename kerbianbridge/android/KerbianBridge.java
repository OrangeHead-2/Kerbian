package kerbianbridge.android;

import java.io.*;
import java.net.*;
import org.json.JSONObject;

public class KerbianBridge {
    private ServerSocket serverSocket;
    private Socket clientSocket;
    private BufferedReader in;
    private BufferedWriter out;
    private UIManager uiManager;

    public KerbianBridge(int port) throws IOException {
        serverSocket = new ServerSocket(port);
        clientSocket = serverSocket.accept();
        in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
        out = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()));
        uiManager = new UIManager();
    }

    public void start() {
        new Thread(() -> {
            String line;
            try {
                while ((line = in.readLine()) != null) {
                    JSONObject msg = new JSONObject(line);
                    handleMessage(msg);
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }).start();
    }

    private void handleMessage(JSONObject msg) throws Exception {
        String type = msg.getString("type");
        if (type.equals("call") && msg.getString("target").equals("UIManager")) {
            String method = msg.getString("method");
            JSONObject args = msg.getJSONObject("args");
            if (method.equals("create_view")) {
                int viewId = uiManager.createView(args.getString("type"), args.getJSONObject("props"));
                JSONObject resp = new JSONObject();
                resp.put("type", "response");
                resp.put("id", msg.optInt("id"));
                resp.put("result", new JSONObject().put("view_id", viewId));
                send(resp);
            }
            // ... handle other methods
        }
        // ... handle other targets and message types
    }

    private void send(JSONObject resp) throws IOException {
        out.write(resp.toString());
        out.write("\n");
        out.flush();
    }
}