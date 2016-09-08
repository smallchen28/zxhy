# Subprocess management

## 基本概念
像Linux进程那样，一个进程可以fork一个子进程，并让这个子进程exec另外一个程序。在Python中，我们通过标准库中的subprocess包来fork一个子进程，并运行一个外部的程序。

subprocess模块用来创建子进程，并允许通过管道和子进程进行通讯。在python3中建议使用模块subprocess32，subprocess32模块提供了更好的实现

subprocess模块用来替代部分老的模块和方法:os.system;os.spawn*;os.popen*;popen2.*;commands.*


### 模块级方法
这些模块方法其实是对popen对象的封装调用，可以参考方法的具体实现。这些方法使用了最常用的参数，更复杂的使用方法需要直接通过popen实现

1. subprocess.call(args, *, stdin=None, stdout=None, stderr=None, shell=False)
通过args参数运行命令，等待命令执行结束并给出返回值

2. subprocess.check_call(args, *, stdin=None, stdout=None, stderr=None, shell=False)
通过args参数运行命令，等待命令执行结束。如果返回0则正常，其他值则会抛出错误。

3. subprocess.check_output(args, *, stdin=None, stderr=None, shell=False, universal_newlines=False)
通过args参数运行命令，等待命令执行结束。如果返回0则正常，其他值则会抛出错误。命令运行的标准输出值作为bytestring返回.

### Popen对象
```
class subprocess.Popen(args,
                       bufsize=0,
                       executable=None,
                       stdin=None,
                       stdout=None,
                       stderr=None,
                       preexec_fn=None,
                       close_fds=False,
                       shell=False,
                       cwd=None,
                       env=None,
                       universal_newlines=False,
                       startupinfo=None,
                       creationflags=0)
```


| 参数 |说明|
|--------|--------|
|args|字符串或者列表，参见下面的说明|
|bufsize|0 无缓冲 1 行缓冲 其他正值 缓冲区大小 负值 采用默认系统缓冲(一般是全缓冲)|
|executable||
|stdin|None 没有任何重定向，继承父进程|
|stdout|PIPE 创建管道,文件对象,文件描述符(整数)|
|stderr|stderr 还可以设置为 STDOUT|
|preexec_fn|钩子函数， 在fork和exec之间执行。(unix)|
|close_fds|unix 下执行新进程前是否关闭0/1/2之外的文件 windows下不继承还是继承父进程的文件描述符|
|shell|为真的话 unix下相当于args前面添加了 "/bin/sh“ ”-c” window下，相当于添加"cmd.exe /c"|
|cwd|设置工作目录|
|env|设置环境变量，以字典的方式表示内容|
|universal_newlines|各种换行符统一处理成 '\n'|
|startupinfo||
|creationflags||

##### 更多说明
- args可以使用字符串也可以使用列表。例如：
subprocess.Popen(["gedit","abc.txt"])
subprocess.Popen("gedit abc.txt")#这个执行会有问题，当参数shell=true时有效。
因此一般应该使用列表传递命令，使用shell有安全隐患

- 使用subprocess包中的函数创建子进程的时候，要注意:
 在创建子进程之后，父进程是否暂停，并等待子进程运行。模块提供的三个方法是会等待的
 函数返回什么
 当returncode不为0时，父进程如何处理。

- 在模块方法中不要使用stdout/stderr=PIPE，有可能导致死锁。应该使用popen的communicate方法获取stderr

### Popen对象的方法

| 方法或属性 |说明|
|--------|--------|
|Popen.poll() |检查是否结束，设置返回值|
|Popen.wait() |等待结束，设置返回值|
|Popen.communicate(input=None) |参数是标准输入，返回标准输出和标准出错，会阻塞父进程直到返回|
|Popen.send_signal(signal) |发送信号 (主要在unix下有用)|
|Popen.terminate() |终止进程，unix对应的SIGTERM信号，windows下调用api函数TerminateProcess()|
|Popen.kill() |杀死进程(unix对应SIGKILL信号)，windows下同上|
|Popen.stdin  |参数中指定PIPE时，有用|
|Popen.stdout ||
|Popen.stderr ||
|Popen.pid |进程id|
|Popen.returncode |进程返回值|


## 示例

- 模块方法调用比较

```
>>> bb = subprocess.call("ls")
>>> print bb#返回的是命令执行是否成功
0
>>> bb = subprocess.check_output("ls")
>>> print bb#返回的是命令的stdout内容
aa.sql
aes.py
anaconda-ks.cfg
installtecs_el7_noarch.bin
isclean.py
keystonerc_admin
openstack_git_root.tar.gz
pairs.py
```

- 模块方法check_output的实现

```
def check_output(*popenargs, **kwargs):
    process = Popen(*popenargs, stdout=PIPE, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        raise CalledProcessError(retcode, cmd, output=output)
    return output
```

- 通过管道进行子进程间通讯

```
>>> child1 = subprocess.Popen(["my_print_defaults","mysqld"], stdout=subprocess.PIPE)
>>> port = subprocess.check_output(["grep","port"], stdin=child1.stdout)
>>> print port
--port=29998

subprocess.PIPE实际上为文本流提供一个缓存区。child1的stdout将文本输出到缓存区，随后child2的stdin从该PIPE中将文本读取走。
```

- 带环境变量参数的popen

```
>>> print admin
{'OS_PASSWORD': 'keystone', 'OS_AUTH_URL': 'http://locahost:5000/v2.0/', 'OS_USERNAME': 'admin', 'OS_TENANT_NAME': 'admin'}
>>> 
>>> aa=subprocess.Popen(["nova","list"],env=admin)
>>> +--------------------------------------+------+--------+------------+-------------+-----------------------+
| ID                                   | Name | Status | Task State | Power State | Networks              |
+--------------------------------------+------+--------+------------+-------------+-----------------------+
| 17745294-b67f-4bf8-b30e-003d25568fc7 | aaaa | ACTIVE | -          | Running     | subnet_1=192.168.1.18 |
| 91bd01af-8c25-4891-8a20-c3e8c2bfd5c8 | bbbb | ACTIVE | -          | Running     | subnet_1=192.168.1.14 |
+--------------------------------------+------+--------+------------+-------------+-----------------------+
```