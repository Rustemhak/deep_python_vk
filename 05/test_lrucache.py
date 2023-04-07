"""Module for testing LRUCache"""
from lrucache import LRUCache


def test_base_limit_0():
    """test LRUCache limit 0"""
    cache = LRUCache(0)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    assert cache.get("k3") is None
    assert cache.get("k2") is None
    assert cache.get("k1") is None

    cache.set("k3", "val3")

    assert cache.get("k3") is None
    assert cache.get("k2") is None
    assert cache.get("k1") is None


def test_base_limit_1():
    """test LRUCache limit 1"""

    cache = LRUCache(1)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    assert cache.get("k3") is None
    assert cache.get("k2") == "val2"
    assert cache.get("k1") is None

    cache.set("k3", "val3")

    assert cache.get("k3") == "val3"
    assert cache.get("k2") is None
    assert cache.get("k1") is None


def test_base_limit_2():
    """test LRUCache limit 2"""

    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    assert cache.get("k3") is None
    assert cache.get("k2") == "val2"
    assert cache.get("k1") == "val1"

    cache.set("k3", "val3")

    assert cache.get("k3") == "val3"
    assert cache.get("k2") is None
    assert cache.get("k1") == "val1"


def test_base_limit_3():
    """test LRUCache limit 3"""

    cache = LRUCache(3)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    assert cache.get("k3") is None
    assert cache.get("k2") == "val2"
    assert cache.get("k1") == "val1"

    cache.set("k3", "val3")

    assert cache.get("k3") == "val3"
    assert cache.get("k2") == "val2"
    assert cache.get("k1") == "val1"


def test_count_cache():
    """test count in LRUCache"""

    cache = LRUCache(2)
    cache.set("a", "a")
    assert len(cache.cache) == 1
    cache.set("b", "b")
    assert len(cache.cache) == 2
    cache.set("c", "c")
    assert len(cache.cache) == 2


def test_insert_twice():
    """test two insert"""

    cache = LRUCache(3)

    cache.set("k1", "val1")
    cache.set("k1", "val1_1")

    assert cache.get("k1") == "val1_1"
