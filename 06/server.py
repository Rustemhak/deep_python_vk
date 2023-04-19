"""Module server"""

import re
import sys
import time
import queue
import socket
import threading
from collections import Counter
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

import click


class Server:
    """create server"""

    def __init__(self, n_threads, k):
        self.count = 0
        self.n_threads = n_threads
        self.k_common = k
        self.host = socket.gethostname()
        self.port = 5000
        self.lock = threading.Lock()
        self.que = queue.Queue()

    def start(self):
        """start server"""
        conn = self.get_conn()
        threads = [threading.Thread(target=self.do_que, args=(conn,),)]

        threads += [
            threading.Thread(target=self.process, args=(conn,),)
            for _ in range(self.n_threads)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        conn.close()

    def get_conn(self):
        """get connect"""
        server_socket = socket.socket()
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)

        conn, _ = server_socket.accept()
        return conn

    def get_most_common_words(self, url):
        """get most common words"""
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

        return res

    def do_que(self, conn):
        """create queue"""
        while True:
            try:
                urls = conn.recv(1024).decode()
                if urls:
                    for url in urls.split("\n"):
                        if url:
                            self.que.put(url)

            except HTTPError as error:
                print(error, flush=True)
                continue

    def process(self, conn):
        """get url and send message"""
        while True:
            if not self.que.qsize():
                time.sleep(0.01)
                continue

            url = self.que.get()
            resp = self.get_most_common_words(url)
            data = f"{url[:35]}: {resp}"
            conn.send(data.encode())

            with self.lock:
                self.count += 1
                print(f"Processed {self.count} requests", flush=True)


@click.command()
@click.option("-w", "--worker", type=int, default=1)
@click.option("-k", "--k_top", type=int, default=1)
def main(worker, k_top):
    """main function"""
    server = Server(worker, k_top)
    server.start()


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Wrong input! Example: 'python server.py -w 10 -k 7'")
    else:
        main()
