class SyncAdapter:
    def __init__(self, db_conn, remote_url):
        self.db = db_conn
        self.remote_url = remote_url

    def push(self, model_cls):
        # Upload all local rows to remote
        rows = model_cls.all(self.db.conn)
        import requests
        for row in rows:
            requests.post(f"{self.remote_url}/{model_cls.__name__.lower()}", json=row.__dict__)

    def pull(self, model_cls):
        import requests
        r = requests.get(f"{self.remote_url}/{model_cls.__name__.lower()}")
        remote_data = r.json()
        for rd in remote_data:
            obj = model_cls()
            for k, v in rd.items():
                setattr(obj, k, v)
            obj.save(self.db.conn)