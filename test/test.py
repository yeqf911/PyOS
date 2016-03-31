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

if __name__ == '__main__':
    # test_follow()
    test_grep()
    pass


