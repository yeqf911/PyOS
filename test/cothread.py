# coding=utf-8
from threading import Thread
import Queue

# 一个装饰器，工作是为了为有 yield 语句的函数做 f.send(None) 的工作
def coroutine(func):
    def wrapper(*args, **kwargs):
        rs = func(*args, **kwargs)
        rs.send(None)
        return rs

    return wrapper

@coroutine
def threaded(target):
    message = Queue.Queue()

    def run_task():
        while True:
            item = message.get()
            if item is GeneratorExit:
                target.close()
                return
            target.send(item)

    Thread(target=run_task).start()
    try:
        while True:
            item = yield
            message.put(item)
    except GeneratorExit:
        message.put(GeneratorExit)



