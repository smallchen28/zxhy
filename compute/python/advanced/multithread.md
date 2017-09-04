# 多线程编程

## 基本概念

### 线程和进程

程序是存储在磁盘上的可执行文件，实际运行时操作系统将程序文件读入内存并分配相关的资源。此时构成了一个进程。

进程可以通过fork/spawn方式派生出新的进程，但进程之间资源相互独立，只能通过进程间通信(IPC)方式共享信息。

线程是在同一个进程下运行的代码部分，线程可以共享进程的资源。线程一般是以并发的方式执行实现多任务之间的协同。

由于多个线程可以访问同一数据，当访问的顺序不同时可能造成最终结果不同，这就需要线程之间有某种同步机制以保证访问数据的可控性。

### python中的线程

python支持多线程编程，但还要和具体的操作系统有关。python使用兼容POSIX的线程，即pthread。

python提供了标准模块threading，thread，Queue，multiprocessing等来支持多线程编程。还有一些第三方模块和python3中的新模块。

### 全局解释锁

The mechanism used by the CPython interpreter to assure that only one thread executes Python bytecode at a time. 
This simplifies the CPython implementation by making the object model (including critical built-in types such as dict) implicitly safe against concurrent access. 
Locking the entire interpreter makes it easier for the interpreter to be multi-threaded, at the expense of much of the parallelism afforded by multi-processor machines.

However, some extension modules, either standard or third-party, are designed so as to release the GIL when doing computationally-intensive tasks such 
as compression or hashing. Also, the GIL is always released when doing I/O.

Past efforts to create a “free-threaded” interpreter (one which locks shared data at a much finer granularity) have not been successful 
because performance suffered in the common single-processor case. It is believed that overcoming this performance issue 
would make the implementation much more complicated and therefore costlier to maintain.

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

### 模块下的方法和类

|对象|说明|
|--------|--------|
|Thread|表示一个执行线程的对象|
|Lock| 锁原语对象|
|RLock| 可重入锁对象 |
|Condition| 条件变量对象，使得一个线程等待另一个线程满足特定条件 |
|Event| 条件变量的通用版|
|Semaphore| 资源上的信号量，没有可用资源时会被阻塞 |
|BoundedSemaphore| 有界信号量 |
|Timer| 与Thread相似，要在运行前等待一段时间|
|Barrier| 创建一个障碍，必须达到指定数量的线程后才开始(python3.2引入)|

### Thread类

使用Thread类，一般有三种方法来创建线程。创建Thread的实例，传给一个函数作为线程主体。派生Thread的子类，并创建子类的实例。
还有一种不常见的模式是将实现了__call__方法的类实例作为target参数传递给Thread类实例。

Thread类支持守护线程概念，常用的一种模式是后台服务开启为守护线程，每接受一个请求就开启一个新线程进行业务处理。整个python程序在所有非守护线程退出后才退出。

|Thread对象属性和方法|说明|
|--------|--------|
|name| 线程名|
|ident| 线程标识符 |
|daemon| 布尔型，是否守护线程 |
|_init_(group=None,target=None,name=None,args=(),kwargs={},verbose=None,daemon=None)| 实例化一个线程对象 |
|start()| 开始执行该线程 |
|run()| 该线程主运行逻辑，一般作为子类要覆盖实现|
|join(timeout=None)| 直至启动的线程终止之前一直挂起；除非给了timeout，否则会一直阻塞|

示例

```
# 创建一个Thread实例，传递方法

import threading

def task1(sec):
    print 'start task1 @', ctime()
    sleep(sec)    
    print 'end task1 @', ctime()
	
if __name__ == '__main__':
    print 'all begin @', ctime()
	t = threading.Thread(target=task1, args=(3,))
	# 启动线程
	t.start()
	# 主线程等待t线程结束
	t.join()
	print 'all done @', ctime()
```


```
# 实现一个Thread子类

class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
	    threading.Thread.__init__(self)
        self.name = name
		self.func = func
		self.args = args
		
	def getResult(self):
	    return self.result

	def run(self):
	    self.result = self.func(*self.args)
```

### Lock类

原子锁是一个同步原语，是python中提供的最底层的同步原语。一个原子锁只有locked/unlocked两种状态，通过两个基本方法acquire/release进行锁的申请和释放。

当多个线程由于acquire动作等待锁时被阻塞，一旦锁被释放只有某一个线程能获取到锁；具体哪个线程能获得锁是不确定的，并不依赖申请锁时的顺序，其依赖于具体的os和python实现。

|方法|说明|
|--------|--------|
|acquire([blocking])| blocking参数为True(默认值)时会被阻塞 |
|release()| 释放锁 |

示例代码

未加锁控制并发访问
```
# 对set内容输出调整
class CleanOutputSet(set):
    def __str__(self):
        return ','.join(x for x in self)

# 随机分配一组随机时间
loops = (randrange(2,6) for x in xrange(randrange(3,8)))
remaining = CleanOutputSet()
lock = Lock()

def loopwithoutlock(nsec):
    tname = currentThread().name
    remaining.add(tname)
    print 'start thread %s,%d' % (tname,nsec)
    sleep(nsec)
    remaining.remove(tname)
    print 'end thread %s' % tname
    print 'remaining:%s' % (remaining or None)

if __name__ == '__main__':
    for pause in loops:
        Thread(target=loopwithoutlock, args=(pause,)).start()

[root@zxdb97 ptest]# python mtc.py 
start thread Thread-1,4
start thread Thread-2,3
start thread Thread-3,2
start thread Thread-4,2
start thread Thread-5,3
end thread Thread-3
remaining:Thread-5,Thread-4,Thread-2,Thread-1
end thread Thread-4
remaining:Thread-5,Thread-2,Thread-1
# 可以看到2/5同时结束，对set并发操作所以出现了不希望的结果
end thread Thread-2
end thread Thread-5
remaining:Thread-1
remaining:Thread-1
end thread Thread-1
remaining:None
```

加锁控制并发访问
```
def loopwithlock(nsec):
    tname = currentThread().name
    lock.acquire()
    remaining.add(tname)
    lock.release()
    print 'start thread %s,%d' % (tname,nsec)
    sleep(nsec)
    lock.acquire()
    remaining.remove(tname)	
    print 'end thread %s' % tname
    print 'remaining:%s' % (remaining or None)
    lock.release()

[root@zxdb97 ptest]# python mtc.py 
start thread Thread-1,3
start thread Thread-2,2
start thread Thread-3,5
start thread Thread-4,5
start thread Thread-5,2
start thread Thread-6,2
start thread Thread-7,3
end thread Thread-2
remaining:Thread-7,Thread-6,Thread-5,Thread-4,Thread-3,Thread-1
end thread Thread-5
remaining:Thread-7,Thread-6,Thread-4,Thread-3,Thread-1
end thread Thread-6
remaining:Thread-7,Thread-4,Thread-3,Thread-1
end thread Thread-1
remaining:Thread-7,Thread-4,Thread-3
end thread Thread-7
remaining:Thread-4,Thread-3
end thread Thread-3
remaining:Thread-4
end thread Thread-4
remaining:None
```

### RLock对象

一个可重入锁是一个同步原语，它可以被相同的线程获得多次。

### Semaphore对象

信号量是很早就有的同步原语。可以当作是一个计数器，资源消耗时减小，释放后增加。常称之为P/V操作。

|方法|说明|
|--------|--------|
|class threading.Semaphore([value])|信号量|
|acquire([blocking])| 计数器减一 |
|release()| 计数器加一 |
|class threading.BoundedSemaphore(value)| 有边界的信号量，释放超过边界时抛出ValueError |

### Timer对象

这个计时器类表示一个线程在指定时间间隔后开始执行函数。Timer是Thread的子类，可以自定义。

注意timer在执行它的动作之前等待的时间间隔可能与用户指定的时间间隔不完全相同。另外可以通过cancel()取消计划执行。

```
def hello():
    print "hello, world"

t = Timer(30.0, hello)
t.start() 
```

### 使用上下文管理

threading模块中提供的具有acquire/release方法的对象，可以用做with语句的上下文管理器。进入代码的地方调用acqurie，退出代码执行relase

目前，Lock、RLock、Condition、Semaphore和BoundedSemaphore对象可以用作with语句的上下文管理器

示例代码

```
import threading

some_rlock = threading.RLock()

with some_rlock:
    print "some_rlock is locked while this executes"
```

## Queue模块

python2提供了Queue模块来提供线程间通信的机制，让线程间可以分享数据。在python3中命名为queue。

Queue 模块实现了多生产者、多消费者队列。它特别适用于信息必须在多个线程间安全地交换的多线程程序中。这个模块中的 Queue 类实现了所有必须的锁语义。

模块中定义

|类和异常|说明|
|--------|--------|
| class Queue.Queue(maxsize=0)| 构造一个FIFO队列。maxsize是个整数，指明了队列中能存放的数据个数的上限。maxsize小于或者等于0，队列大小没有限制。|
|class Queue.LifoQueue(maxsize=0)| 构造一个LIFO队列。后入先出队列，当队列没有空间时插入会被阻塞。 |
|class Queue.PriorityQueue(maxsize=0)| 构造一个优先队列。|
|exception Queue.Empty| 当对空队列调用get方法时抛出异常。|
|exception Queue.Full | 当对满队列调用put方法时抛出异常。|

### Queue对象

|对象方法|说明|
|--------|--------|
|qsize()| 队列近似大小|
|empty()| 队列为空返回True |
|full() | 队列为满返回True|
|put(item, block=True, timeout=None)| 向队列中插入元素，如果timeout有值，则最多阻塞timeout秒，如果block为False，队列空则抛出Empty异常|
|put_nowait(item)| 相当于put(item, False)|
|get(block=True, timeout=None)| 从队列中获取元素，如果block且没有元素会被阻塞至到可以获取到|
|get_nowait()| 相当于get(False)|
|task_done()| 表示队列中某个元素执行完，由消费者线程调用|
|join() | 阻塞调用线程，直到队列中的所有任务被处理taskdone掉。|

示例代码

```
def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()

q = Queue()
for i in range(num_worker_threads):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

for item in source():
    q.put(item)

q.join()
```

# 更多解决方案

多线程是一个很好的并发执行方案，但由于GIL的限制，python中的多线程更适合于I/O密集型任务。对应计算密集型任务还有其他的并发执行机制。

## subprocess模块

这个参见基础模块subprocess。创建多个子进程实现并发操作。

## multiprocessing模块

这个参见基础模块multiprocessing模块。提供了一系列类似threading模块的方法实现子进程操作。

## concurrent.futures模块

这个参见python3的知识点