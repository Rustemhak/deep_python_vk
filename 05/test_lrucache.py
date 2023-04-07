"""Module for testing LRUCache"""
import unittest

from lrucache import LRUCache


class TestLRUCache(unittest.TestCase):
    "class for test LRUCache"

    def test_base_limit_0(self):
        """test LRUCache limit 0"""
        cache = LRUCache(0)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertIsNone(cache.get("k3"))
        self.assertIsNone(cache.get("k2"))
        self.assertIsNone(cache.get("k1"))

        cache.set("k3", "val3")

        self.assertIsNone(cache.get("k3"))
        self.assertIsNone(cache.get("k2"))
        self.assertIsNone(cache.get("k1"))

    def test_base_limit_1(self):
        """test LRUCache limit 1"""

        cache = LRUCache(1)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertIsNone(cache.get("k3"))
        self.assertEqual(cache.get("k2"), "val2")
        self.assertIsNone(cache.get("k1"))

        cache.set("k3", "val3")

        self.assertEqual(cache.get("k3"), "val3")
        self.assertIsNone(cache.get("k2"))
        self.assertIsNone(cache.get("k1"))

    def test_base_limit_2(self):
        """test LRUCache limit 2"""

        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertIsNone(cache.get("k3"))
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")

        cache.set("k3", "val3")

        self.assertEqual(cache.get("k3"), "val3")
        self.assertIsNone(cache.get("k2"))
        self.assertEqual(cache.get("k1"), "val1")

    def test_base_limit_3(self):
        """test LRUCache limit 3"""

        cache = LRUCache(3)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertIsNone(cache.get("k3"))
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")

        cache.set("k3", "val3")

        self.assertEqual(cache.get("k3"), "val3")
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")

    def test_count_cache(self):
        """test count in LRUCache"""

        cache = LRUCache(2)
        cache.set("a", "a")
        self.assertEqual(len(cache.cache), 1)
        cache.set("b", "b")
        self.assertEqual(len(cache.cache), 2)
        cache.set("c", "c")
        self.assertEqual(len(cache.cache), 2)

    def test_insert_twice(self):
        """test two insert"""

        cache = LRUCache(3)

        cache.set("k1", "val1")
        cache.set("k1", "val1_1")

        self.assertEqual(cache.get("k1"), "val1_1")
