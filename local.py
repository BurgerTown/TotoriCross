import logging
fmt="%(funcName)s():%(lineno)i: %(message)s "

logging.basicConfig(level=logging.DEBUG, format=fmt)
logger = logging.getLogger(__name__)

import threading
import socket
import struct
import multiprocessing

VER = 5
METHOD = 0

# Define HOST Struct
class HOST:
    def __init__(self, port = 80, addr = "127.0.0.1"):
        self.ADDR = addr
        self.PORT = port

local = HOST(port = 2333)
server = HOST(port = 3333)

def _recv(s):
    '''
        A wrapper to recv undefined length data
    '''
    ret = b""
    while True:
        tmp = s.recv(1024)
        ret += tmp
        if len(tmp) < 1024:
            break

    # logger.debug(ret)
    return ret

def newConnection(sock, addr):
    '''
        When Server got a new connection, start this function
    '''
    global VER, METHOD

    # Recieve Data
    data = _recv(sock)

    # Send Protocol Data
    cmd = struct.pack('bb',VER,METHOD)
    sock.send(cmd)
    # logger.info(cmd)

    # Get Protocol Data
    data = _recv(sock)
    logger.info(data)

    data = [i for i in data]
    remote = HOST()
    ATYP = data[3]

    # Get the remote server info
    if ATYP == 1:
        # print("Currently we dont support ipv4 ip access")
        remote.ADDR = "".join([chr(i) for i in data[5:-2]])
    elif ATYP == 3:
        remote.ADDR = "".join([chr(i) for i in data[5:-2]])
    elif ATYP == 4:
        print("Currently we dont support ipv6 ip access")
        return
    remote.ADDR = str(remote.ADDR)   # For str output, please use repr
    remote.PORT = int(data[-2]*16*16+data[-1])


    # Send successful code
    data = struct.pack("bbbb4sh",5,0,0,1,socket.inet_aton(local.ADDR),local.PORT)
    # logger.info(data)
    sock.send(data)

    # Get Http Request
    data = _recv(sock)
    logger.info(data)

    # Todo: obfs data

    # Todo: send the data to remote server
    try:
        logger.debug("connect to {0} {1}".format(repr(remote.ADDR), remote.PORT))

        s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
        s.connect((remote.ADDR, remote.PORT))
        s.send(data)

        # Get data from remote
        data = _recv(s)
        logger.debug("{0} -- {1}".format(remote.ADDR, data))

        # Todo Send the package back to broswer
        # This is just an example
        sock.send(data)

        s.close()
    except Exception as e:
        logger.critical("CRITICAL EXCEPTION: %s -- %s" % (remote.ADDR, e))

    logger.info("THREADING STOPPED")

    sock.close()

    return

def main():
    '''
        main function
    '''
    logger.info("local server Started")
    global PORT

    server.ADDR = "127.0.0.1"
    server.PORT = 3333
    local.ADDR = "127.0.0.1"
    local.PORT = 2333

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((local.ADDR, local.PORT))
        s.listen(10)

        logger.info("Socket Established")
        logger.info("Waiting For Connections")

        while True:
            sock, addr = s.accept()
            t = multiprocessing.Process(target=newConnection, args=(sock,addr))
            t.start()

    except Exception as e:
        logger.critical("MAIN EXCEPTION: %s" % e)
        s.close()

    return

if __name__ == "__main__":
    main()