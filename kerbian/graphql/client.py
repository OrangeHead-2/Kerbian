import requests

class GraphQLClient:
    def __init__(self, endpoint, headers=None):
        self.endpoint = endpoint
        self.headers = headers or {}

    def query(self, query, variables=None):
        payload = {"query": query, "variables": variables or {}}
        r = requests.post(self.endpoint, json=payload, headers=self.headers)
        r.raise_for_status()
        return r.json()

    def mutate(self, mutation, variables=None):
        return self.query(mutation, variables)