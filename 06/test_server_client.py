"""module for testing server / client"""
import unittest

from server import Server
from client import Client

TEXT_TMP = "https://www.avito.ru\nhttps://www.ya.ru\nhttps://www.ozon.ru"
FILE_TMP = "urls_test.txt"
ADDRESS = "https://www.ya.ru"


class TestLRUCache(unittest.TestCase):
    def test_connection_settings(self):
        server = Server(10, 7)
        client = Client(10, "urls.txt")

        assert server.host == client.host
        assert server.port == client.port

    def test_read_file(self):
        with open(FILE_TMP, "w", encoding="utf-8") as file:
            file.write(TEXT_TMP)

        client = Client(10, FILE_TMP)
        n_urls = len(TEXT_TMP.split("\n"))
        assert n_urls == len(client.get_urls())

    def test_client_chunk(self):
        with open(FILE_TMP, "w", encoding="utf-8") as file:
            file.write(TEXT_TMP)

        client = Client(10, FILE_TMP)
        urls = client.get_urls()
        chunks = client.chunks(urls, 3)

        urls_from_client = []
        for chunk in chunks:
            urls_from_client.extend([i.strip() for i in chunk])

        real_urls = TEXT_TMP.split("\n")
        assert urls_from_client == real_urls

    def test_request_processing(self):
        k = 7
        server = Server(10, 7)
        result = server.get_most_common_words(ADDRESS)
        assert k == len(result)
