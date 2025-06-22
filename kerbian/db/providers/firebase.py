import requests

class FirebaseConnection:
    def __init__(self, url, token=None):
        self.url = url.rstrip('/')
        self.token = token

    def cursor(self):
        return self

    def execute(self, q, params=None):
        # Support basic get/post/put/delete for demonstration
        if q.startswith("GET "):
            endpoint = q[4:].strip()
            r = requests.get(f"{self.url}/{endpoint}.json", params={"auth": self.token} if self.token else {})
            return r.json()
        elif q.startswith("PUT "):
            endpoint, data = q[4:].split(" ", 1)
            r = requests.put(f"{self.url}/{endpoint}.json", json=eval(data), params={"auth": self.token} if self.token else {})
            return r.json()
        # ... Add POST/DELETE as needed

    def commit(self): pass
    def close(self): pass