import logging
fmt="%(funcName)s():%(lineno)i: %(message)s "

logging.basicConfig(level=logging.INFO, format=fmt)
logger = logging.getLogger(__name__)

import socket
import multiprocessing

ADDR = "127.0.0.1"
PORT = 3333

def newConnection(sock, addr):
    logger.info("{0}".format(addr))

    data = sock.recv(1024)
    logger.debug(data)

    data = sock.recv(1025)
    logger.debug(data)

    sock.close()
    return

def main():
    logger.info("Server Started")
    try:
        s = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ADDR, PORT))
        s.listen(5)

        while True:
            sock,addr = s.accept()
            t = multiprocessing.Process(target=newConnection, args=(sock, addr))
            t.start()
    except Exception as e:
        print(e)
        s.close()

    return


if __name__ == "__main__":
    main()
else:
    logger.warning("Please run in main mode")