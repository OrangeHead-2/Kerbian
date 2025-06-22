package kerbianbridge.android;

import org.json.JSONObject;

public class ErrorReporter {
    public static NativeEventSink eventSink;

    public static void report(String errorType, String message, JSONObject details) {
        try {
            if (eventSink != null) {
                JSONObject errorMsg = new JSONObject();
                errorMsg.put("type", "error");
                errorMsg.put("error_type", errorType);
                errorMsg.put("message", message);
                errorMsg.put("details", details != null ? details : new JSONObject());
                eventSink.send(errorMsg.toString());
            }
        } catch (Exception e) {
            System.err.println("Bridge error: " + errorType + " " + message);
            e.printStackTrace();
        }
    }
}