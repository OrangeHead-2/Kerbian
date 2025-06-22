import socket, threading, os

def start_live_reload_server(watch_dir, on_reload, port=5678):
    def file_watcher():
        mtimes = {}
        while True:
            changed = False
            for root, _, files in os.walk(watch_dir):
                for f in files:
                    path = os.path.join(root, f)
                    try:
                        m = os.path.getmtime(path)
                        if path not in mtimes or mtimes[path] != m:
                            mtimes[path] = m
                            changed = True
                    except:
                        continue
            if changed:
                on_reload()
            time.sleep(1)
    threading.Thread(target=file_watcher, daemon=True).start()
    # In production, implement websocket/ws push for remote reload