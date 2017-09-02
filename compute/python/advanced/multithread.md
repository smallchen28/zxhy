# 多线程编程

## 基本概念

### 线程和进程

程序是存储在磁盘上的可执行文件，实际运行时操作系统将程序文件读入内存并分配相关的资源。此时构成了一个进程。

进程可以通过fork/spawn方式派生出新的进程，但进程之间资源相互独立，只能通过进程间通信(IPC)方式共享信息。

线程是在同一个进程下运行的代码部分，线程可以共享进程的资源。线程一般是以并发的方式执行实现多任务之间的协同。

由于多个线程可以访问同一数据，当访问的顺序不同时可能造成最终结果不同，这就需要线程之间有某种同步机制以保证访问数据的可控性。

### python中的线程

python支持多线程编程，但还要和具体的操作系统有关。python使用兼容POSIX的线程，即pthread。

python提供了标准模块threading，thread，Queue，multiprocessing等来支持多线程编程。还有一些第三方模块和python3中的新概念协程。

### 全局解释锁

### 应用场景

## thread模块

thread模块在python3中被命名为_thread。该模块是更底层的实现，提供了派生线程的方法和一个基本的锁对象。建议使用threading模块。

|函数或方法|说明|
|--------|--------|
|thread模块的函数|
|start_new_thread(function, args, kwargs=None)|派生一个新的线程，给定参数执行function|
|allocate_lock()| 分配LockType对象 |
|exit()| 线程退出|
|LockType锁对象方法|
|acquire(wait=None)| 尝试获取锁对象 |
|locked()| 是否获取了锁对象 |
|release()| 锁释放 |

 - 示例代码
```
import thread
from time import sleep,ctime

def task1(lock):
    print 'start task1 @', ctime()
    sleep(4)
    lock.release()
    print 'end task1 @', ctime()

def task2(lock):
    print 'start task2 @', ctime()
    sleep(2)
    lock.release()
    print 'end task2 @', ctime()


if __name__ == '__main__':
    print 'all begin @', ctime()

    # 分配锁对象
    lock1 = thread.allocate_lock()
    lock2 = thread.allocate_lock()
    lock1.acquire()
    lock2.acquire()
    
    # 启动了两个线程
    thread.start_new_thread(task1,(lock1,))
    thread.start_new_thread(task2,(lock2,))

    # 通过锁对象释放判断线程结束
    while lock1.locked():
        pass
    while lock2.locked():
        pass

    print 'all done @', ctime()

# 执行结果可以看到task2先结束，但总时间和最长任务task1相当。
[root@zxdb97 ptest]# python mtb.py 
all begin @ Sat Sep  2 11:28:43 2017
start task1 @ Sat Sep  2 11:28:43 2017
start task2 @ Sat Sep  2 11:28:43 2017
end task2 @ Sat Sep  2 11:28:45 2017
end task1 @ Sat Sep  2 11:28:47 2017
all done @ Sat Sep  2 11:28:47 2017
```

## threading模块

### 生成器表达式

|对象|说明|
|--------|--------|
|Thread|表示一个执行线程的对象|
|Lock| 锁原语对象|
|RLock| 可重入锁对象 |
|Condition| 条件变量对象，使得一个线程等待另一个线程满足特定条件 |
|Event| 条件变量的通用版|
|Semaphore| 资源上的信号量，没有可用资源时会被阻塞 |
|BoundedSemaphore|  |
|Timer| 与Thread相似，要在运行前等待一段时间|
|Barrier| 创建一个障碍，必须达到指定数量的线程后才开始(python3.2引入)|

### 生成器的send()和close()方法
- send(value):

Python 2.5中，yield语句变成了yield表达式，也就是说yield可以有一个值，而这个值就是send()方法的参数。
所以send(None)和next()是等效的。同样，next()和send()的返回值都是yield语句处的参数（yielded value）

关于send()方法需要注意的是：调用send传入非None值前，生成器必须处于挂起状态，否则将抛出异常。
也就是说，第一次调用时，要使用next()语句或send(None)，因为没有yield语句来接收这个值。

- close():

这个方法用于关闭生成器，对关闭的生成器后再次调用next或send将抛出StopIteration异常。

示例
```
>>> def consumer():
... while True:
... d = yield
... if not d: break
... print "consumer:", d
>>> c = consumer() # 创建消费者
>>> c.send(None)  # 启动消费者
>>> c.send(1)  # 生产数据，并提交给消费者。
consumer: 1
>>> c.send(2)
consumer: 2
>>>c.send(3)
consumer: 3
>>> c.send(None) # 生产结束，通知消费者结束。
StopIteration
```