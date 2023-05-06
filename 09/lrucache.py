import sys
import logging.config
import re


class EvenWordFilter(logging.Filter):
    def filter(self, record):
        word_count = len(re.findall(r'\w+', record.getMessage()))
        return word_count % 2 != 0


log_conf = {
    "version": 1,
    "formatters": {
        "simple": {"format": "%(asctime)s\t%(levelname)s"
                             "\t%(name)s\t%(message)s", },
        "processed": {
            "format": "%(asctime)s\t%(levelname)s\t--%(name)s--\t%(message)s",
        },
    },
    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "filename": "cache.log",
            "formatter": "simple",
        },
        "stream_handler": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "processed",
        },
    },
    "loggers": {
        "": {"level": "INFO", "handlers": ["file_handler"], },
        "add_stream": {"level": "DEBUG", "handlers": ["stream_handler"], },
    },
}

logging.config.dictConfig(log_conf)

root_logger = logging.getLogger()
STREAM_LOGGER = None
if "-s" in sys.argv:
    STREAM_LOGGER = logging.getLogger("add_stream")

if "-f" in sys.argv:
    even_word_filter = EvenWordFilter()
    root_logger.addFilter(even_word_filter)
    if STREAM_LOGGER:
        STREAM_LOGGER.addFilter(even_word_filter)


class ListNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, limit=42):
        self.cache = {}
        self.limit = limit
        self.head = ListNode(0, 0)
        self.tail = ListNode(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        root_logger.debug("Initialization cache")

    def _remove(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node):
        prev_node = self.tail.prev
        prev_node.next = node
        node.prev = prev_node
        node.next = self.tail
        self.tail.prev = node

    def set(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        else:
            node = ListNode(key, value)
            self.cache[key] = node
            self._add(node)
            root_logger.info("Set value to cache")

        if len(self.cache) > self.limit:
            del_node = self.head.next
            self._remove(del_node)
            del self.cache[del_node.key]
            root_logger.debug("Cache value was overwritten")

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            root_logger.info("Get value from cache")
            return node.value

        root_logger.info("Value not in cache")
        return None


if __name__ == "__main__":
    cache = LRUCache(3)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    print(cache.get("k3"))  # None
    print(cache.get("k2"))  # "val2"
    print(cache.get("k1"))  # "val1"

    cache.set("k3", "val3")

    print(cache.get("k3"))  # "val3"
    print(cache.get("k2"))  # "val2"
    print(cache.get("k1"))  # "val1"

    cache.set("k4", "val4")
