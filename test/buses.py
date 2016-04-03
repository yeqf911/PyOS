# coding=utf-8
import xml.sax
import cothread

# 一个装饰器，工作是为了为有 yield 语句的函数做 f.send(None) 的工作
def coroutine(func):
    def wrapper(*args, **kwargs):
        rs = func(*args, **kwargs)
        rs.send(None)
        return rs

    return wrapper


class Bushandler(xml.sax.ContentHandler):
    def __init__(self, target):
        xml.sax.ContentHandler.__init__(self)
        self.target = target

    def startElement(self, name, attrs):
        self.target.send(('start', (name, attrs)))

    def characters(self, content):
        self.target.send(('content', content))

    def endElement(self, name):
        self.target.send(('end', name))


@coroutine
def buses_to_dict(target):
    try:

        while True:
            event, value = (yield)
            if event == 'start' and value[0] == 'bus':
                buses = {}
                fragment = []
                while True:
                    event, value = (yield)
                    if event == 'start':
                        fragment = []
                    if event == 'content':
                        fragment.append(value)
                    if event == 'end':
                        if value != 'bus':
                            buses[value] = ' '.join(fragment)
                        else:
                            target.send(buses)
                            break
    except GeneratorExit:
        target.close()


@coroutine
def direction_filter(field, value, target):
    d = (yield)
    if d.get(field) == value:
        target.send(d)


@coroutine
def printbus():
    while True:
        bus = (yield)
        print "%(route)s,%(id)s,\"%(direction)s\"," \
              "%(latitude)s,%(longitude)s" % bus


if __name__ == '__main__':
    xml.sax.parse('bus.xml', Bushandler(buses_to_dict(cothread.threaded(direction_filter('route', '22', printbus())))))
