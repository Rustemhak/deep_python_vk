import unittest
from unittest.mock import patch, mock_open
import itertools

from server import Server
from client import Client

TEXT_TMP = "https://www.avito.ru\nhttps://www.ya.ru\nhttps://www.ozon.ru"
FILE_TMP = "urls.txt"


class TestServerClient(unittest.TestCase):
    def setUp(self):
        self.server = Server(10, 7)

    def test_connection_settings(self):
        server = Server(10, 7)
        client = Client(10, "urls.txt")
        self.assertEqual(server.host, client.host)
        self.assertEqual(server.port, client.port)

    def test_client_chunk(self):
        with patch("builtins.open", mock_open(read_data=TEXT_TMP)):
            client = Client(10, FILE_TMP)
            chunks = client.chunks(client.get_urls(), 3)

            urls_from_client = []
            for chunk in chunks:
                urls_from_client.extend([i.strip() for i in chunk])

            real_urls = TEXT_TMP.split("\n")
            self.assertEqual(urls_from_client, real_urls)

    def test_client_socket_handling(self):
        with patch("builtins.open", mock_open(read_data=TEXT_TMP)), patch(
            "socket.socket"
        ) as mock_socket:
            mock_socket_instance = mock_socket.return_value
            mock_socket_instance.recv.return_value = b"OK"
            client = Client(10, FILE_TMP)
            client.process(itertools.islice(client.get_urls(), 1))

            self.assertEqual(mock_socket_instance.connect.call_count, 1)

    def test_read_file(self):
        with patch("builtins.open", mock_open(read_data=TEXT_TMP)):
            client = Client(10, FILE_TMP)
            n_urls = len(TEXT_TMP.split("\n"))
            self.assertEqual(n_urls, len(list(client.get_urls())))

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
            most_common_words = self.server.get_most_common_words("https://example.com")

            self.assertEqual(
                most_common_words,
                [
                    ("words", 3),
                    ("test", 2),
                    ("page", 2),
                    ("this", 1),
                    ("is", 1),
                    ("a", 1),
                    ("with", 1),
                ],
            )


if __name__ == "__main__":
    unittest.main()
