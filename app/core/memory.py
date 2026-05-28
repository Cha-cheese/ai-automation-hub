class Memory:
    def __init__(self):
        self.store = {}

    def save(self, session_id, data):
        self.store[session_id] = data

    def load(self, session_id):
        return self.store.get(session_id, {})