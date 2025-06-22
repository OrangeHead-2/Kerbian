# KerbianCore Device — Push Notifications, Background Tasks, Device APIs

Production-grade Python APIs for push notifications, background jobs, sensors, secure storage, and device info.

---

## Push Notifications

- Register device, manage tokens
- Send or receive push via custom protocol/server
- Display notifications, handle user actions (background or foreground)

```python
from kerbiancore.device.push import PushTokenManager, PushServer, NotificationManager

tm = PushTokenManager()
tm.register("device1", "tokenABC")
srv = PushServer(send_fn=lambda token, msg: print("Send", token, msg))
srv.send("tokenABC", {"title": "Hello", "body": "Message"})
nm = NotificationManager()
nm.display("Title", "Body")
```

---

## Background Tasks

- Schedule periodic or deferred tasks, retries, constraints
- Run jobs only on WiFi, battery, or idle

```python
from kerbiancore.device.background import BackgroundScheduler, BackgroundTask

def sync():
    print("Syncing in background...")

sched = BackgroundScheduler()
sched.add_task(BackgroundTask(sync, interval=300, constraints={"network": True}))
sched.start()
```

---

## Sensors

- Camera, GPS, accelerometer, gyroscope, microphone
- Permission abstraction, event listeners

```python
from kerbiancore.device.sensors import PermissionManager, Camera

pm = PermissionManager()
cam = Camera(pm)
cam.add_listener(lambda img: print("Captured", img))
cam.start(); cam.capture()
```

---

## Secure Storage

- File storage with encryption-at-rest
- Quota, sandboxing, background sync

```python
from kerbiancore.device.storage import SecureStorage

storage = SecureStorage("myappdata")
storage.save("userpic", b"...")
print(storage.list_keys())
```

---

## Device Info

- Fingerprinting, OS/version, battery, network, locale, screen, feature detection

```python
from kerbiancore.device.deviceinfo import get_device_info, runtime_hardware_checks

print(get_device_info())
print(runtime_hardware_checks())
```

---

## Best Practices

- Always check/request permissions for sensors
- Use secure storage for sensitive data
- Schedule background jobs with proper constraints
- Handle push in both foreground and background

---