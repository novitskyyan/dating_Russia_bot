import json


class Cities:
    def __init__(self, filename):
        self.data = json.loads(open(filename, "r", encoding="utf-8").read())

    def get_cities(self):
        c = []
        for pairs in self.data:
            c.append(pairs["city"])
        return c