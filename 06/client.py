"""Module client"""
import itertools
import sys
import socket
import threading

import click


class Client:
    """create client"""

    def __init__(self, n_threads, file):
        self.n_threads = n_threads
        self.file = file
        self.host = "localhost"
        self.port = 5000

    def get_urls(self):
        """get urls generator"""
        with open(self.file, "r", encoding="utf-8") as filed:
            for line in filed:
                yield line.strip()

    def get_client_socket(self):
        """create connect"""
        client_socket = socket.socket()
        client_socket.connect((self.host, self.port))
        return client_socket

    def process(self, urls):
        """recv send"""
        for url in urls:
            with self.get_client_socket() as client_socket:
                try:
                    client_socket.send(url.encode())
                    data = client_socket.recv(1024).decode()
                    if data:
                        print(data, flush=True)
                except Exception as exception:
                    print(f"Error processing {url}: {exception}", flush=True)

    def start(self):
        """start client"""
        urls = self.get_urls()

        threads = [
            threading.Thread(target=self.process, args=(chunk,), )
            for chunk in self.chunks(urls, self.n_threads)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    @staticmethod
    def chunks(iterable, count):
        """create generator"""
        it_ = iter(iterable)
        item = list(itertools.islice(it_, count))
        while item:
            yield item
            item = list(itertools.islice(it_, count))


@click.command()
@click.argument("worker", type=int)
@click.argument("file_name")
def main(worker, file_name):
    """main function"""
    client = Client(worker, file_name)
    client.start()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Wrong input! Example: 'python client.py 10 urls.txt'")
    else:
        main()
