# Redis进阶

## 慢查询分析

由于redis采用单线程响应命令，某些命令如keys获取所有关键字可能导致处理流程被阻塞。慢查询日志是用来记录服务端执行命令时存在性能瓶颈的机制，redis提供了一系列命令和配置进行管理

### 配置和命令

| 命令/配置 | 说明 |
|--------|--------|
|slowlog-log-slower-than| 单位为us，默认值是10000。=0记录所有<0则不记录 |
|slowlog-max-len        | 日志队列长度，默认128。日志以队列形式保存     |
|confg set slowlog-max-len 100 | 动态设置日志队列长度                   |
|config rewrite         |  将当前配置保存到配置文件                     |
|slowlog get [n]        |  获取某条慢日志记录                           |
|slowlog len            |  当前日志队列记录的长度                       |
|slowlog reset          |  重置日志队列                                 |

### 最佳实践

- 在实际运行环境中可以适当增大slowlog-max-len以便保存更多有效信息。

- 在高流量场景下，需要调低slowlog-log-slower-than参数。例如每个命令都需要1ms，则1s只能只能响应1000次操作。

- 慢查询只记录了操作的时间，而影响客户端的感受还包括网络传输，命令队列等待等因素。

- 慢查询队列内容记录会随着时间而冲掉，可以通过某些定期采集机制获取队列内容并转存。

## 客户端工具

### redis-cli

```
[root@db3 ~]# redis-cli --help
redis-cli 3.2.8

Usage: redis-cli [OPTIONS] [cmd [arg [arg ...]]]
  -h <hostname>      Server hostname (default: 127.0.0.1).
  -p <port>          Server port (default: 6379).
  -s <socket>        Server socket (overrides hostname and port).
  -a <password>      Password to use when connecting to the server.
  -r <repeat>        Execute specified command N times.
  -i <interval>      When -r is used, waits <interval> seconds per command.
                     It is possible to specify sub-second times like -i 0.1.
  -n <db>            Database number.
  -x                 Read last argument from STDIN.
  -d <delimiter>     Multi-bulk delimiter in for raw formatting (default: \n).
  -c                 Enable cluster mode (follow -ASK and -MOVED redirections).
  --raw              Use raw formatting for replies (default when STDOUT is
                     not a tty).
  --no-raw           Force formatted output even when STDOUT is not a tty.
  --csv              Output in CSV format.
  --stat             Print rolling stats about server: mem, clients, ...
  --latency          Enter a special mode continuously sampling latency.
  --latency-history  Like --latency but tracking latency changes over time.
                     Default time interval is 15 sec. Change it using -i.
  --latency-dist     Shows latency as a spectrum, requires xterm 256 colors.
                     Default time interval is 1 sec. Change it using -i.
  --lru-test <keys>  Simulate a cache workload with an 80-20 distribution.
  --slave            Simulate a slave showing commands received from the master.
  --rdb <filename>   Transfer an RDB dump from remote server to local file.
  --pipe             Transfer raw Redis protocol from stdin to server.
  --pipe-timeout <n> In --pipe mode, abort with error if after sending all data.
                     no reply is received within <n> seconds.
                     Default timeout: 30. Use 0 to wait forever.
  --bigkeys          Sample Redis keys looking for big keys.
  --scan             List all keys using the SCAN command.
  --pattern <pat>    Useful with --scan to specify a SCAN pattern.
  --intrinsic-latency <sec> Run a test to measure intrinsic system latency.
                     The test will run for the specified amount of seconds.
  --eval <file>      Send an EVAL command using the Lua script at <file>.
  --ldb              Used with --eval enable the Redis Lua debugger.
  --ldb-sync-mode    Like --ldb but uses the synchronous Lua debugger, in
                     this mode the server is blocked and script changes are
                     are not rolled back from the server memory.
  --help             Output this help and exit.
  --version          Output version and exit.

Examples:
  cat /etc/passwd | redis-cli -x set mypasswd
  redis-cli get mypasswd
  redis-cli -r 100 lpush mylist x
  redis-cli -r 100 -i 1 info | grep used_memory_human:
  redis-cli --eval myscript.lua key1 key2 , arg1 arg2 arg3
  redis-cli --scan --pattern '*:12345*'

  (Note: when using --eval the comma separates KEYS[] from ARGV[] items)

When no command is given, redis-cli starts in interactive mode.
Type "help" in interactive mode for information on available commands
and settings.
```

### redis-benchmark

benchmark可以为redis进行基准性能测试。

```
[root@db3 ~]# redis-benchmark --help
Usage: redis-benchmark [-h <host>] [-p <port>] [-c <clients>] [-n <requests]> [-k <boolean>]

 -h <hostname>      Server hostname (default 127.0.0.1)
 -p <port>          Server port (default 6379)
 -s <socket>        Server socket (overrides host and port)
 -a <password>      Password for Redis Auth
 -c <clients>       Number of parallel connections (default 50)
 -n <requests>      Total number of requests (default 100000)
 -d <size>          Data size of SET/GET value in bytes (default 2)
 -dbnum <db>        SELECT the specified db number (default 0)
 -k <boolean>       1=keep alive 0=reconnect (default 1)
 -r <keyspacelen>   Use random keys for SET/GET/INCR, random values for SADD
  Using this option the benchmark will expand the string __rand_int__
  inside an argument with a 12 digits number in the specified range
  from 0 to keyspacelen-1. The substitution changes every time a command
  is executed. Default tests use this to hit random keys in the
  specified range.
 -P <numreq>        Pipeline <numreq> requests. Default 1 (no pipeline).
 -e                 If server replies with errors, show them on stdout.
                    (no more than 1 error per second is displayed)
 -q                 Quiet. Just show query/sec values
 --csv              Output in CSV format
 -l                 Loop. Run the tests forever
 -t <tests>         Only run the comma separated list of tests. The test
                    names are the same as the ones produced as output.
 -I                 Idle mode. Just open N idle connections and wait.

Examples:

 Run the benchmark with the default configuration against 127.0.0.1:6379:
   $ redis-benchmark

 Use 20 parallel clients, for a total of 100k requests, against 192.168.1.1:
   $ redis-benchmark -h 192.168.1.1 -p 6379 -n 100000 -c 20

 Fill 127.0.0.1:6379 with about 1 million keys only using the SET test:
   $ redis-benchmark -t set -n 1000000 -r 100000000

 Benchmark 127.0.0.1:6379 for a few commands producing CSV output:
   $ redis-benchmark -t ping,set,get -n 100000 --csv

 Benchmark a specific command line:
   $ redis-benchmark -r 10000 -n 10000 eval 'return redis.call("ping")' 0

 Fill a list with 10000 random elements:
   $ redis-benchmark -r 10000 -n 10000 lpush mylist __rand_int__

 On user specified command lines __rand_int__ is replaced with a random integer
 with a range of values selected by the -r option.
```


## 管道Pipeline

### 请求响应和RTT

Redis是一种基于客户端-服务端模型以及请求/响应协议的TCP服务

这意味着通常情况下一个请求会遵循以下步骤：

- 客户端向服务端发送一个查询请求，并监听Socket返回，通常是以阻塞模式，等待服务端响应。

- 服务端处理命令，并将结果返回给客户端。

客户端和服务器通过网络进行连接。无论网络延如何延时，数据包总是能从客户端到达服务器，并从服务器返回数据回复客户端。

这个时间被称之为 RTT (Round Trip Time - 往返时间). 当RTT性能较差时将严重的影响服务的实际表现


### pipelining

一次请求/响应服务器能实现处理新的请求即使旧的请求还未被响应。这样就可以将多个命令发送到服务器，而不用等待回复，最后在一个步骤中读取该答复。

Redis很早就支持管道（pipelining）技术，因此无论你运行的是什么版本，你都可以使用管道（pipelining）操作Redis。下面是一个使用的例子：

```
$ (printf "PING\r\nPING\r\nPING\r\n"; sleep 1) | nc localhost 6379
+PONG
+PONG
+PONG
```

重要说明:

使用管道发送命令时，服务器将被迫回复一个队列答复，占用很多内存。所以，如果你需要发送大量的命令，最好是把他们按照合理数量分批次的处理，例如10K的命令，读回复，然后再发送另一个10k的命令，等等。这样速度几乎是相同的，但是在回复这10k命令队列需要非常大量的内存用来组织返回数据内容。
 
### 管道VS脚本VS批量命令

批量命令是原子性的，只能作用于一个关键字。管道不是原子性的，而且可以作用于不同关键字。

大量pipeline应用场景可通过Redis脚本(Redis版本>=2.6)得到更高效的处理，后者在服务器端执行大量工作。

脚本的一大优势是可通过最小的延迟读写数据，让读、计算、写等操作变得非常快（pipeline在这种情况下不能使用，因为客户端在写命令前需要读命令返回的结果）。


## 发布与订阅(Pub/Sub)

通过redis可以实现类似消息服务器的简单发布和订阅系统。

### 命令

| 命令   | 说明   |
|--------|--------|
|subscribe channel [channel]     | 订阅频道       |
|unsubscribe [channel [channel ]]| 解定阅频道     |
|psubscribe chanelpattern        | 批量订阅       |
|punsubscribe changepattern      | 批量解订阅     |
|publish chanel messge           | 向频道发送消息 |
|pubsub subcommand               | 查询订阅信息   |

示例

```
订阅频道，注意返回的消息内容
127.0.0.1:6379> SUBSCRIBE fm97.5 fm101.1
Reading messages... (press Ctrl-C to quit)
1) "subscribe"
2) "fm97.5"
3) (integer) 1
1) "subscribe"
2) "fm101.1"
3) (integer) 2
接收publish内容
1) "message"
2) "fm97.5"
3) "hello"
1) "message"
2) "fm101.1"
3) "nnnn"
另一个客户端发送消息
127.0.0.1:6379> PUBLISH fm97.5 hello
(integer) 1
127.0.0.1:6379> publish fm101.1 nnnn
(integer) 1
模式匹配订阅
127.0.0.1:6379> PSUBSCRIBE fm*
Reading messages... (press Ctrl-C to quit)
1) "psubscribe"
2) "fm*"
3) (integer) 1
模式匹配接收的消息
1) "pmessage"
2) "fm*"
3) "fm97.5"
4) "heagain"
```

### 一些概念

消息格式:

订阅/注销，接收消息时会收到特定格式的消息。一般是一个三元组

第一个元素是消息类型：例如subscribe，unsubscribe，message，pmessage

第二个元素是频道名称：模式匹配时还包括模式频道名称

第三个元素是消息内容或频道数

作用域:

发布/订阅与key所在空间没有关系。如果你需要区分某些频道，可以通过在频道名称前面加上所在环境的名称(命名空间)区分

同时匹配:

当订阅频道和模式匹配订阅频道相当时会接收到多个消息。但消息类型区分为pmessage和message

## 事件通知

## Lua脚本

## 事务与Lua

## BitMaps

## HyperLogLog

hyperloglog实际存储的是字符串类型，通过一种基数算法完成一些统计上的功能。

### 命令

| 命令   | 说明   |
|--------|--------|
|pfadd key element [e]   |  添加元素     |
|pfcount key [key]       |  计算独立总数 |
|pfmerge destkey srckey [k]| 并集操作    |

示例
```
127.0.0.1:6379> PFADD key1 tom jack lacy jerry 
(integer) 1
127.0.0.1:6379> pfcount key1
(integer) 4
127.0.0.1:6379> pfadd key1 tom cindy pony 
(integer) 1
127.0.0.1:6379> pfcount key1
(integer) 6
```

该数据结构提供了一个空间和时间高度优化的近似统计功能。在100万级数据时能提供基本准确(官方给出的误差率在0.81%)的数据统计，并且占用极小的内存空间。

比较100w记录内容的set和hyperloglog数据结构。set占用100m，而h只有15k左右。

## GEO

redis3.2版本开始提供了GEO(地理信息定位)功能，支持存储地理位置的数据结构来实现相关功能。

### 命令

| 命令   | 说明   |
|--------|--------|
|geoadd key lot lat member [l l m] | 插入一个包含经纬度的地理位置数据 |
|geohash key member [member]       | 返回地理空间的geohash字符串      |
|geopos key member                 | 返回一个地理位置数据             |
|geodist key member1 member2 [unit]| 返回两个地理位置之间的距离       |
|georadius key lot lat rad[unit]   | 基于坐标和半径返回指定元素集合   |
|georadiusbymember key member rad  | 指定半径内最大距离一个地理位置   |
|zrem key member                   | 删除某个位置                     |

示例
```
127.0.0.1:6379> geoadd cn 10 10 city1 14 13 city2 4 7 city3 13 13 city4
(integer) 4
127.0.0.1:6379> geopos cn city2
1) 1) "14.00000184774398804"
   2) "13.00000057302225542"
127.0.0.1:6379> geodist cn city1 city2 km
"548.9651"
127.0.0.1:6379> geodist cn city1 city3 km
"739.5019"
# 根据坐标搜索半径内地理位置
127.0.0.1:6379> GEORADIUS key longitude latitude radius m|km|ft|mi [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count] [ASC|DESC] [STORE key] [STOREDIST key]
127.0.0.1:6379> georadius cn 10 10 500 km withcoord withdist
1) 1) "city1"
   2) "0.0003"
   3) 1) "10.00000208616256714"
      2) "10.00000092823272979"
2) 1) "city4"
   2) "467.1501"
   3) 1) "12.99999922513961792"
      2) "13.00000057302225542"
127.0.0.1:6379> geohash cn city1
1) "s1z0gs3y0z0
```

### geohash

geohash将二维经纬度转换为一维字符串。该值具有以下特点

- geo的实际存储类型是zset，所以使用zrem删除内容。

- 字符串越长，表示的位置精度越高。redis内使用字符串前缀匹配算法实现相关命令。

- 两个字符串越相似，它们之间距离越近。

- geohash编码和经纬度是可以相互转换的。[参见](https://en.wikipedia.org/wiki/Geohash)


## 二级索引
