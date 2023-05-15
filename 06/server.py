import re
import sys
import queue
import socket
import threading
from collections import Counter
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

import click


class Server:
    def __init__(self, n_threads, k):
        self.count = 0
        self.n_threads = n_threads
        self.k_common = k
        self.host = "localhost"
        self.port = 5000
        self.lock = threading.Lock()
        self.que = queue.Queue()

    def start(self):
        with ThreadPoolExecutor(max_workers=self.n_threads) as executor:
            with socket.socket() as server_socket:
                server_socket.bind((self.host, self.port))
                server_socket.listen(5)
                print("Server started on", self.host, ":", self.port)

                while True:
                    conn, _ = server_socket.accept()
                    executor.submit(self.handle_connection, conn)

    def handle_connection(self, conn):
        with conn:
            while True:
                try:
                    urls = conn.recv(1024).decode()
                    if not urls:
                        break
                    for url in urls.split("\n"):
                        if url:
                            words = self.get_most_common_words(url)
                            data = f"{url[:35]}: {words}"
                            conn.send(data.encode())
                            with self.lock:
                                self.count += 1
                                print(f"Processed {self.count} requests", flush=True)
                except (HTTPError, URLError) as error:
                    print(error, flush=True)
                except Exception as exception:
                    print("Unexpected error:", exception, flush=True)

    def get_most_common_words(self, url):
        res = None
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            " AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/89.0.4389.82 Safari/537.36 "
        }
        try:
            req = Request(url, headers=headers)
            with urlopen(req, timeout=5) as response:
                html = response.read()
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text()

            words = []

            for line in text.splitlines():
                line = line.strip().lower()
                line = re.sub("[^a-zа-я]", " ", line)
                words.extend(line.split())
            cnt = Counter(words)
            res = cnt.most_common(self.k_common)
        except HTTPError as error:
            print(error, flush=True)
        except URLError as url_error:
            print("Error while reaching the URL:", url_error, flush=True)
        except Exception as exception:
            print("Unexpected error:", exception, flush=True)

        return res


@click.command()
@click.option("-w", "--worker", type=int, default=1)
@click.option("-k", "--k_top", type=int, default=1)
def main(worker, k_top):
    server = Server(worker, k_top)
    server.start()


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Wrong input! Example: 'python server.py -w 10 -k 7'")
    else:
        main()
