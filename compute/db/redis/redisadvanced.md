

## 管道pipelining

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
 
### 管道VS脚本

大量 pipeline 应用场景可通过 Redis 脚本（Redis 版本 >= 2.6）得到更高效的处理，后者在服务器端执行大量工作。脚本的一大优势是可通过最小的延迟读写数据，让读、计算、写等操作变得非常快（pipeline 在这种情况下不能使用，因为客户端在写命令前需要读命令返回的结果）。

## 发布与订阅(Pub/Sub)

通过redis可以实现类似消息服务器的简单发布和订阅系统。

### 命令

SUBSCRIBE channel [channel ...]
UNSUBSCRIBE [channel [channel ...]]
psubscribe chanelpattern
publish chanel messge

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

## 过期expire

## 事务

## 批量操作数据

## 事件通知

## Lua脚本

## 二级索引
