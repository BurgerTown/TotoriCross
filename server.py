import logging
fmt="%(funcName)s():%(lineno)i: %(message)s "

logging.basicConfig(level=logging.INFO, format=fmt)

logger = logging.getLogger(__name__)

import threading
import socket
import struct

VER = 5
METHOD = 0
PORT = 2333

def newConnection(sock, addr):
    '''
        当服务器accept一个新的连接后，启动的处理进程。
    '''
    global VER, METHOD, PORT, cnt

    logging.basicConfig(level=logging.CRITICAL, format=fmt)

    # Recieve Data
    sock.recv(1024)

    # Send Protocol Data
    cmd = struct.pack('bb',VER,METHOD)
    sock.send(cmd)
    logger.info(cmd)

    # Get Protocol Data
    sock.recv(1024)

    # Send successful code
    port = struct.pack("bbbbbbbbh",5,0,0,1,127,0,0,1,PORT)
    logger.info(port)
    sock.send(port)

    # Get Http Request
    data = sock.recv(1024)
    logger.info(data)

    sock.send(bytes("233", "utf-8"))

    logger.info("Threading Stopped")
    sock.close()

    return

def main():
    '''
        主函数
    '''
    logger.info("Main Prog Started")
    global PORT

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", PORT))
        s.listen(5)

        logger.info("Socket Established")
        logger.info("Waiting For Connections")

        while True:
            sock, addr = s.accept()
            t = threading.Thread(target=newConnection, args=(sock,addr))
            t.start()

    except Exception as e:
        logger.debug("Main Exception: %s" % e)
        s.close()

    return

if __name__ == "__main__":
    main()