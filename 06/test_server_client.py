import unittest
from unittest.mock import patch

from server import Server
from client import Client

TEXT_TMP = "https://www.avito.ru\nhttps://www.ya.ru\nhttps://www.ozon.ru"
FILE_TMP = "urls_test.txt"
ADDRESS = "https://www.ya.ru"


class TestServerClient(unittest.TestCase):
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

    def setUp(self):
        self.server = Server(1, 5)

    def test_get_most_common_words_with_mock(self):
        fake_html = """
        <html>
        <head>
            <title>Test Page</title>
        </head>
        <body>
            <p>This is a test page with some words for testing purposes.</p>
            <p>These words should appear in the most common words list.</p>
        </body>
        </html>
        """

        def mock_urlopen(*args, **kwargs):
            class MockResponse:
                def read(self):
                    return fake_html.encode()

                def __enter__(self):
                    return self

                def __exit__(self, *args, **kwargs):
                    pass

            return MockResponse()

        with patch("server.urlopen", side_effect=mock_urlopen):
            most_common_words = self.server.\
                get_most_common_words("https://example.com")

            self.assertEqual(most_common_words, [('words', 3),
                                                 ('test', 2),
                                                 ('page', 2),
                                                 ('this', 1),
                                                 ('is', 1)])
