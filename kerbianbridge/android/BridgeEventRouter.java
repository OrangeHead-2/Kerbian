package kerbianbridge.android;

import org.json.JSONObject;

public class BridgeEventRouter {
    public static NativeEventSink eventSink;

    public static void emit(String event, int viewId, JSONObject data) {
        try {
            if (eventSink != null) {
                JSONObject msg = new JSONObject();
                msg.put("type", "event");
                msg.put("event", event);
                msg.put("view_id", viewId);
                msg.put("data", data != null ? data : new JSONObject());
                eventSink.send(msg.toString());
            }
        } catch (Exception e) {
            ErrorReporter.report("BridgeError", "Failed to emit event: " + event, new JSONObject().put("exception", e.toString()));
        }
    }
}