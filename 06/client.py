"""Module client"""

import sys
import socket
import threading

import click


class Client:
    """create client"""

    def __init__(self, n_threads, file):
        self.n_threads = n_threads
        self.file = file
        self.host = socket.gethostname()
        self.port = 5000
        self.client_socket = None

    def get_urls(self):
        """get urls"""
        urls = []
        with open(self.file, "r", encoding="utf-8") as filed:
            for line in filed.readlines():
                urls.append(line)

        return urls

    def get_client_socket(self):
        """create connect"""
        client_socket = socket.socket()
        client_socket.connect((self.host, self.port))
        return client_socket

    def start(self):
        """start client"""
        self.client_socket = self.get_client_socket()
        urls = self.get_urls()

        threads = [
            threading.Thread(target=self.process, args=(chunk,),)
            for chunk in self.chunks(urls, self.n_threads)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self.client_socket.close()

    @classmethod
    def chunks(cls, lst, count):
        """create generator"""
        start = 0
        for i in range(count):
            stop = start + len(lst[i::count])
            yield lst[start:stop]
            start = stop

    def process(self, urls):
        """recv send"""
        for url in urls:
            self.client_socket.send(url.encode())
            data = self.client_socket.recv(1024).decode()
            if data:
                print(data, flush=True)


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
