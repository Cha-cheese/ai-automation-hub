class DB:
    def __init__(self):
        self.data = {}

    def save(self, user, key, value):
        if user not in self.data:
            self.data[user] = {}
        self.data[user][key] = value

    def get(self, user, key):
        return self.data.get(user, {}).get(key)


db = DB()