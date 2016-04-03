# coding=utf-8
import pickle

# 一个装饰器，工作是为了为有 yield 语句的函数做 f.send(None) 的工作
def coroutine(func):
    def wrapper(*args, **kwargs):
        rs = func(*args, **kwargs)
        rs.send(None)
        return rs

    return wrapper

# 有 yield 语句的函数需要加上
@coroutine
def sendto(f):
    try:
        while True:
            item = yield
            pickle.dump(item, f)
            f.flush()
    except StopIteration:
        f.close()


def rcvfrom(f, target):
    try:
        while True:
            item = pickle.load(f)
            target.send(item)
    except EOFError:
        target.close()


if __name__ == '__main__':
    with open('lalal', 'wb') as f:
        sendto(f)
        rcvfrom(f, lambda x: [i for i in range(x)])
