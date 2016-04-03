# coding:utf-8
from Queue import Queue


# 定义系统调用接口类
class SystemCall(object):
    def handler(self):
        pass


# SystemCall接口的实现
class GetId(SystemCall):
    def handler(self):
        self.task.sendvalue = self.task.tid
        self.schedule.schedule(self.task)


class NewTask(SystemCall):
    def __init__(self, target):
        self.target = target

    def handler(self):
        tid = self.schedule.new(self.target)
        self.task.sendvalue = tid   # 把tid赋值给这个task sendvalue, 以供下一次返回给 yield
        # 所有的 handler() 都有这句话，目的是为了让调度器再次调度
        # 调用 NewTask() 的 函数，即是此处的task，可能会返回一些调度的结果，比如这里的 tid
        self.schedule.schedule(self.task)

class KillTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handler(self):
        task = self.schedule.taskmap.get(self.tid, None)
        if task:
            task.target.close()
            self.task.sendvalue = True
        else:
            self.task.sendvalue = False
        self.schedule.schedule(self.task)


class WaitTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handler(self):
        result = self.schedule.wait_for_exit(self.task, self.tid)
        self.task.sendvalue = result
        if not result:
            self.schedule.schedule(self.task)



# 定义Task类，所有任务统一管理，用taskid 来表示，相当于pid
class Task(object):
    taskid = 0

    def __init__(self, target):
        Task.taskid += 1
        self.tid = Task.taskid
        self.target = target
        self.sendvalue = None

    def run(self):
        return self.target.send(self.sendvalue)


# 全局调度器
class Scheduler(object):
    def __init__(self):
        self.ready = Queue()
        self.taskmap = {}
        self.exit_waiting = {}

    # 创建新任务
    def new(self, target):
        newtask = Task(target)
        self.taskmap[newtask.tid] = newtask  # 用task.tid来当键 ，值就是task实例
        self.schedule(newtask)
        return newtask.tid

    # 将 task 放入队列中等待调度
    def schedule(self, task):
        self.ready.put(task)

    # 退出任务，
    def exit(self, task):
        print 'The task %d terminated' % task.tid
        del self.taskmap[task.tid]  # 退出时将task从taskmap里删除
        # 当一个 task 结束的时候遍历他的 tid 所对应的 wait 列表，如果有等待的 task 需要执行就放到任务队列中等待调度
        for tk in self.exit_waiting.pop(task.tid, []):
            self.schedule(tk)

    def wait_for_exit(self, task, waittid):
        # 如果的等待的任务 waitid 在 taskmap 里，就将需要等待的任务 task 放到 wait 列表里，
        # 等 waitid 所代表的 task 执行完成之后再执行 exit_waiting 中 waitid 对应的 wait 列表里的任务
        # 上面所说的这一步操作是在 exit() 有体现
        if waittid in self.taskmap:
            self.exit_waiting.setdefault(waittid, []).append(task)
            return True
        else:
            return False



    def mainloop(self):
        while self.taskmap:
            runtask = self.ready.get()
            try:
                result = runtask.run()  # 获取 runtask 的返回结果，其实是对应的 yield 表达式后面的东东
                if isinstance(result, SystemCall):  # 如果返回结果是系统调用，则执行系统调用handler()
                    result.task = runtask  # 保存当前环境(上下文)\
                    result.schedule = self  # schedule 和 当前 task
                    result.handler()
                    continue
            except StopIteration:
                self.exit(runtask)
                continue  # 如果检测到了异常, exit后就continue，并不再执行后面的调度器语句
            self.schedule(runtask)  # 再将runtask加入到调度器中，继续下一个yield语句


def foo():
    call = yield GetId()  # 这里的GetId()对象作为send()语句的返回值返回给了相应的地方。
    for i in range(5):
        print 'i am bar', call
        import time
        time.sleep(0.5)
        yield  # 每当遇到yield表达式就返回到上一次send()处


def bar():
    call = yield GetId()
    for i in range(10):
        print 'i am foo', call
        import time
        time.sleep(0.5)
        yield


def foo1():
    for i in range(5):
        print('foo1')
        import time
        time.sleep(0.5)
        yield


def main():
    # 这条语句就是把foo1()放入调度器中等待调度。要求是调度器要先执行调用这句话的函数
    ti = yield NewTask(foo1())
    #
    # t = yield KillTask(ti)
    #
    print('wait for %s' % str(ti))
    rs = yield WaitTask(ti)
    if rs:
        print('Done')

if __name__ == '__main__':
    schedule = Scheduler()
    # schedule.new(foo())
    # schedule.new(bar())
    schedule.new(main())
    schedule.mainloop()
