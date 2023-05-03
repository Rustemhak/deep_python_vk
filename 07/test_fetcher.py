import os

import unittest
from unittest.mock import patch
import asyncio
import aiohttp
from fetcher import get_urls, fetch_url, fetch_batch_urls


class TestFetcher(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_urls.txt"
        self.test_urls = [
            "https://httpbin.org/get",
            "https://httpbin.org/status/404",
            "https://httpbin.org/status/500",
        ]

        with open(self.test_file, "w", encoding="utf-8") as file:
            for url in self.test_urls:
                file.write(f"{url}\n")

    def tearDown(self):
        os.remove(self.test_file)

    def test_get_urls(self):
        urls = list(get_urls(self.test_file))
        expected_urls = [url + "\n" for url in self.test_urls]
        self.assertEqual(urls, expected_urls)

    async def async_fetch_url(self, url):
        async with aiohttp.ClientSession() as session:
            return await fetch_url(url, session, 0)

    @patch("aiohttp.ClientSession.get")
    def test_fetch_url(self, mock_get):
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.read = asyncio.coroutine(
            lambda: b"dummy content"
        )

        url = self.test_urls[0]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        status, length, num = loop.run_until_complete(
            self.async_fetch_url(url)
        )
        self.assertEqual(status, 200)
        self.assertGreater(length, 0)
        self.assertEqual(num, 0)

    @patch("aiohttp.ClientSession.get")
    def test_fetch_batch_urls(self, mock_get):
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.read = asyncio.coroutine(
            lambda: b"dummy content"
        )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        queue = asyncio.Queue()
        for url in self.test_urls:
            loop.run_until_complete(queue.put(url))
        loop.run_until_complete(fetch_batch_urls(queue, 3))


if __name__ == "__main__":
    unittest.main()
