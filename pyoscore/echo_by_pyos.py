from pyos import *
import socket


def handle_client(sock, addr):
    print 'connection from', addr
    while True:
        data = sock.recv(65535)
        if not data:
            break
        print data
        sock.send(data)
    sock.close()
    print 'Client closed'
    yield


def server(port):
    print 'server has started at port: %s' % str(port)
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind(('', port))
    srv.listen(10)
    while True:
        client, addr = srv.accept()
        yield NewTask(handle_client(client, addr))


def start():
    yield NewTask(server(8888))

def alive():
    while True:
        print 'I am alive'
        yield

if __name__ == '__main__':
    schedule = Scheduler()
    schedule.new(start())
    schedule.new(alive())
    schedule.mainloop()