# coding=utf-8
import time


def fun():
    for i in range(5):
        print(i)
        yield


# 一个装饰器，工作是为了为有 yield 语句的函数做 f.send(None) 的工作
def coroutine(func):
    def wrapper(*args, **kwargs):
        rs = func(*args, **kwargs)
        rs.send(None)
        return rs

    return wrapper


@coroutine
def follow(filename):  # 实现linux的  tail -f <file> 命令的功能
    filename.seek(0, 2)
    while True:
        line = filename.readline()
        if not line:
            time.sleep(1)
            continue
        yield line


def test_follow():
    with open('/home/idouby/test.log1') as filee:
        for line in follow(filee):
            print(line)


@coroutine  # 上面定义的coroutine就是帮函数做了f.next(None)的工作
def grep(kw):
    print 'finding the kw %s' % kw
    try:
        while True:
            line = (yield)
            if kw in line:
                print line
    except GeneratorExit:
        print 'Good By'
    except RuntimeError as e:
        print('catch the RuntimeError')
        # raise e


def test_grep():
    g = grep('python')
    # g.next()
    # g.send(None)  # 说明send(None)和next()是一样的
    g.send('dsff dasda')
    g.send('python is shit')
    g.send('python id good')
    # g.close()
    # g.send()
    g.throw(RuntimeError, 'you are hosed')


@coroutine
def follow2(fileitem, target):
    fileitem.seek(0, 2)
    try:
        while True:
            line = fileitem.readline()
            if not line:
                time.sleep(0.1)
                continue
            target.send(line)
    except GeneratorExit:
        print('Bye Bye')


@coroutine
def filter_line(target):
    while True:
        line = yield
        if '4' in line:
            target.send(line)


@coroutine
def printer(ids):
    print ids
    while True:
        line = yield
        time.sleep(1)
        print line


def test_follow2():
    with open('/home/idouby/test.log1') as f:
        follow2(f, filter_line(printer()))


def follow_line_x(fileitem, target):
    fileitem.seek(0, 2)
    try:
        while True:
            line = fileitem.readline()
            if not line:
                time.sleep(0.1)
                continue
            target.send(line)
    except GeneratorExit:
        print 'ByeBye'


# send给多个接收器
@coroutine
def broadcast(targets):
    line = yield
    for target in targets:
        target.send(line)
        print 'send'  # 证明send也是要的等的，并不能真正的多个一起执行


def test_follow_x():
    with open('/home/idouby/test.log1') as f:
        a = printer(1)
        b = printer(2)
        c = printer(3)
        follow_line_x(f, broadcast([a, b, c]))


if __name__ == '__main__':
    # test_follow()
    # test_grep()
    # test_follow2()
    # test_follow_x()
    # def lala():
    #     print('1')
    #     yield
    #     print('2')
    #     yield
    #     print('3')
    #     yield
    #
    # f = lala()
    # f.send('sada')
    # f.next('dsadsa')
    # def foo():
    #     print '1'
    #     a = yield
    #     print '2', a
    #     b = yield
    #     print '3', b
    #     yield
    #
    # f = foo()
    # f.send('I am 2')
    # f.send('I am 3')
    # def fun():
    #     while True:
    #         print('lalasa')
    #         import time
    #         time.sleep(0.5)
    #         yield
    #
    # f = fun()
    # f.send(None)
    # f.send(None)
    # f.send('sad')
    pass
    # import re
    # url = 'dsgfbhfsdlovedgsdfdsg'
    #
    # s = re.match(r'.*love.*', url)
    # print(s.group())
    # def bar():
    #     yield 1
    #
    # def foo():
    #     yield bar()
    #     print 'hello'
    #
    # foo()
    while True:
        print 'iii'
