# Signal

## 基本概念

本模块为python提供了支持异步系统信号的机制。信号是一个操作系统特性，它提供了一个途径可以通知程序发生了一个事件并异步处理这个事件。信号可以由系统本身生成，也可以从一个进程发送到另一个进程。

信号和其处理器的工作规则一般如下：

- 特定信号的处理程序一旦设置，将保持安装直到它被显式重置，但是跟随底层实现的SIGCHLD处理程序除外。

- 不能在信号处理关键部分再插入处理另一个信号？(UNIX不支持)

- 尽管信号处理称为异步的，但只能在python原子指令直接发生调用。这意味着在长时间原子操作(例如C实现的对大块内容上的正则表达式匹配)发生时信号不会被及时的处理。

- 当I/O操作期间信号到达时，I/O操作可能在信号处理程序返回后引发异常。这个是由具体系统实现决定的。

- 因为C信号处理程序总是返回，所以捕捉同步错误（如SIGFPE或SIGSEGV）没有任何意义。

- 默认情况下，python对应安装了少量的信号处理程序。

- 
如果在同一个程序中使用信号和线程，必须小心。 在同时使用信号和线程时要记住的基本事情是：在执行的主线程中总是执行signal（）操作。 任何线程都可以执行alarm（），getsignal（），pause（），setitimer（）或getitimer（）; 只有主线程可以设置一个新的信号处理程序，而主线程将是唯一一个接收信号（这是由Python信号模块实现的，即使底层线程实现支持向单个线程发送信号）。 这意味着信号不能用作线程间通信的一种手段。 使用锁代替。

## 模块使用

### 常用信号

linux系统中提供的信号
```
[root@db1 ~]# kill -l
 1) SIGHUP       2) SIGINT       3) SIGQUIT      4) SIGILL       5) SIGTRAP
 6) SIGABRT      7) SIGBUS       8) SIGFPE       9) SIGKILL     10) SIGUSR1
11) SIGSEGV     12) SIGUSR2     13) SIGPIPE     14) SIGALRM     15) SIGTERM
16) SIGSTKFLT   17) SIGCHLD     18) SIGCONT     19) SIGSTOP     20) SIGTSTP
21) SIGTTIN     22) SIGTTOU     23) SIGURG      24) SIGXCPU     25) SIGXFSZ
26) SIGVTALRM   27) SIGPROF     28) SIGWINCH    29) SIGIO       30) SIGPWR
31) SIGSYS      34) SIGRTMIN    35) SIGRTMIN+1  36) SIGRTMIN+2  37) SIGRTMIN+3
38) SIGRTMIN+4  39) SIGRTMIN+5  40) SIGRTMIN+6  41) SIGRTMIN+7  42) SIGRTMIN+8
43) SIGRTMIN+9  44) SIGRTMIN+10 45) SIGRTMIN+11 46) SIGRTMIN+12 47) SIGRTMIN+13
48) SIGRTMIN+14 49) SIGRTMIN+15 50) SIGRTMAX-14 51) SIGRTMAX-13 52) SIGRTMAX-12
53) SIGRTMAX-11 54) SIGRTMAX-10 55) SIGRTMAX-9  56) SIGRTMAX-8  57) SIGRTMAX-7
58) SIGRTMAX-6  59) SIGRTMAX-5  60) SIGRTMAX-4  61) SIGRTMAX-3  62) SIGRTMAX-2
63) SIGRTMAX-1  64) SIGRTMAX
[root@db1 ~]# 
```

|常量|说明|
|--------|--------|
|signal.SIG_DFL|默认信号处理函数，传递给hander|
|signal.SIG_IGN|忽略信号处理函数，传递给hander。这两个是标准处理函数|
|signal.CTRL_BREAK_EVENT |对应CTRL+BREAK 键盘事件|
|signal.CTRL_C_EVENT|对应CTRL+C 键盘事件，与os.kill搭配使用|
|signal.NSIG|比最高信号数的数目多一个，用来判断传入的信号值是否异常|


### 重要的函数

#### 1 signal.signal(signalnum, handler) 

signalnum为信号编号，handler指定了处理信号的函数。当进程接收到信号后进行对应的处理

handler的定义是def hanlder(signum, frame)。frame表示接收信号时的栈信息。

#### 2 signal.getsignal(signalnum)

获取对应信号的处理函数

#### 3 signal.setitimer(which, seconds[, interval])

参考C库函数setitimer

#### 4 signal.getitimer(which)

#### 5 signal.set_wakeup_fd(fd)

#### 6 signal.siginterrupt(signalnum, flag)

#### 7 signal.pause()

将本进程进入睡眠状态，直到有接收信号量才转由对应信号处理函数进行处理。

#### 8 signal.alarm(time) 

给本进程发alarm信号，如果是0则取消之前计划的alarm信号，如果是非0则之前的alarm计划被取消重新开始计划。

## 示例

信号处理定义
```
def receive_signal(signum, stack):
    print 'Received:', signum

# 注册信号处理程序
signal.signal(signal.SIGUSR1, receive_signal)
signal.signal(signal.SIGUSR2, receive_signal)

# 显示进程号
print 'My PID is:', os.getpid()

# 后续通过kill命令或python中的os.kill函数发送信号
```

父子进程间通信
```
def signal_usr1(signum, frame):
    "Callback invoked when a signal is received"
    pid = os.getpid()
    print 'Received USR1 in process %s' % pid

print 'Forking...'
child_pid = os.fork()
if child_pid:
    print 'PARENT: Pausing before sending signal...'
    time.sleep(1)
    print 'PARENT: Signaling %s' % child_pid
    # 在父进程中，使用kill()发送一个USR1信号给子进程
    os.kill(child_pid, signal.SIGUSR1)
else:
    print 'CHILD: Setting up a signal handler'
    signal.signal(signal.SIGUSR1, signal_usr1)
    print 'CHILD: Pausing to wait for signal'
    time.sleep(5)
```

