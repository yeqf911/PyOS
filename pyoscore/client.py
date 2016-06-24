from pyos import *
import socket
import time


def client(addr):
    clt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clt.connect(addr)
    print 'one client'
    clt.send(b'hello')
    try:
        while True:
            data = clt.recv(65535)
            if not data:
                break
            print data
            clt.send(data)
            time.sleep(0.5)
    except KeyboardInterrupt as e:
        raise e
    clt.close()
    print 'connection has closed'
    yield


def main():
    yield NewTask(client(('127.0.0.1', 8888)))


if __name__ == '__main__':
    schedule = Scheduler()
    schedule.new(main())
    schedule.mainloop()
