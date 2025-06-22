package kerbianbridge.android;

public interface NativeEventSink {
    void send(String jsonLine);
}