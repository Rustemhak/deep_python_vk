"""Module for algorithm for storing a limited amount of data"""


class LRUCache:
    """class for implementing LRU Cache algorithm"""

    def __init__(self, limit=42):
        self.cache = {}
        self.stack = []
        self.limit = limit

    def set(self, key, value):
        """set key value"""
        if key in self.cache:
            self.stack.remove(key)

        self.cache[key] = value
        self.stack.append(key)

        if len(self.stack) > self.limit:
            pop_key = self.stack.pop(0)
            self.cache.pop(pop_key)

    def get(self, key):
        """get value by key"""
        if key in self.cache:
            self.stack.remove(key)
            self.stack.append(key)
            return self.cache[key]

        return None
