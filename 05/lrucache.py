"""Module for algorithm for storing a limited amount of data"""


class ListNode:
    """
    A class representing a node in a doubly-linked list.
    """

    def __init__(self, key, value):
        """
        Initialize a new node with the given key and value.

        Args:
            key: The key associated with this node.
            value: The value associated with this node.
        """
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """
    A class implementing the LRU Cache algorithm with
    constant average-time complexity operations.
    """

    def __init__(self, limit=42):
        """
        Initialize a new LRUCache with the given capacity.

        Args:
            limit: The maximum number of elements the cache can store.
        """
        self.cache = {}
        self.limit = limit
        self.head = ListNode(0, 0)
        self.tail = ListNode(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """
        Remove the given node from the doubly-linked list.

        Args:
            node: The node to be removed.
        """
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node):
        """
        Add the given node to the end of the doubly-linked list.

        Args:
            node: The node to be added.
        """
        prev_node = self.tail.prev
        prev_node.next = node
        node.prev = prev_node
        node.next = self.tail
        self.tail.prev = node

    def set(self, key, value):
        """
        Set the value for the given key in the cache.
        If the key already exists, update its value.
        If the cache is full,
        remove the least recently used item before adding the new item.

        Args:
            key: The key to be set or updated.
            value: The value to be associated with the key.
        """
        if key in self.cache:
            self._remove(self.cache[key])

        node = ListNode(key, value)
        self.cache[key] = node
        self._add(node)

        if len(self.cache) > self.limit:
            del_node = self.head.next
            self._remove(del_node)
            del self.cache[del_node.key]

    def get(self, key):
        """
        value associated with the given key in the cache.
         If the key does not exist, return None.

        Args:
            key: The key to retrieve the value for.

        Returns:
            The value associated with the key,
            or None if the key does not exist.
        """

        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.value

        return None
