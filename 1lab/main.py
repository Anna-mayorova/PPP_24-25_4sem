from threading import Thread

from server import start

import client


def main():
    client.main()


def server():
    start()


if __name__ == '__main__':
    Thread(target=start).start()
    Thread(target=main).start()
