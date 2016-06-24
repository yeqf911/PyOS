from pyos import *
import socket
import time


def handle_client(sock, addr):
    print 'connection from', addr
    try:
        while True:
            yield ReadWait(sock)
            data = sock.recv(65535)
            if not data:
                break
            print data
            yield WriteWait(sock)
            sock.send(data)
    except socket.error:
        print 'Client({}, {}) has disconnected'.format(str(addr[0]), str(addr[1]))
    sock.close()
    print 'Client closed'
    yield


def server(port):
    print 'server has started at port: %s' % str(port)
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind(('', port))
    srv.listen(10)
    while True:
        yield ReadWait(srv)
        client, addr = srv.accept()
        yield NewTask(handle_client(client, addr))


def start():
    yield NewTask(server(8888))


def alive():
    while True:
        print 'I am alive'
        yield


def sleep1():
    time.sleep(4)
    print 'after sleep'
    yield


def nosleep():
    print 'no sleep'
    yield


if __name__ == '__main__':
    schedule = Scheduler()
    schedule.new(start())
    schedule.mainloop()
