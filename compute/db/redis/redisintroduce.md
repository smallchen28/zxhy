# Redis介绍

## 简介

REmote DIctionary Server(Redis) 是一个由Salvatore Sanfilippo写的key-value存储系统。

Redis是一个开源的使用ANSI C语言编写、遵守BSD协议、支持网络、可基于内存亦可持久化的日志型、Key-Value数据库，并提供多种语言的API。

它通常做为数据结构存储服务器，也可以作为数据缓存或简单消息中间件。

Redis 与其他 key - value 缓存产品有以下三个特点：

- Redis支持数据的持久化，可以将内存中的数据保存在磁盘中，重启的时候可以再次加载进行使用。

- Redis不仅仅支持简单的key-value类型的数据，同时还提供list，set，zset，hash，geo等数据结构的存储。

- Redis支持数据的备份，即master-slave模式的数据备份。

### Redis 优势

- 性能极高 – Redis能读的速度是110000次/s,写的速度是81000次/s 。

- 丰富的数据类型 – Redis支持二进制案例的 Strings, Lists, Hashes, Sets 及 Ordered Sets 数据类型操作。

- 原子性 - Redis的所有操作都是原子性的，意思就是要么成功执行要么失败完全不执行。单个操作是原子性的。多个操作也支持事务，即原子性，通过MULTI和EXEC指令包起来。

- 丰富的特性 – Redis还支持 publish/subscribe,批量执行,通知,key过期等等特性。

## 数据类型

Redis当前支持的数据类型包括：string,hash,list,set,zset(sorted set),bitmaps,hyperloglogs,geospatial.

### keys关键字

Redis中的关键字是二进制安全的，这意味着你可以使用任意二进制序列作为关键字，例如字符串或一个JPEG图片内容或空字符串，空字符串也可以关键字。

关于key的几个原则:

- 太长的键值不是一个好的实践，对内存空间和操作时间都会产生大量消耗。

- 太短的键值也不是一个好的主意，容易造成关键字的冲突或歧意。

- 最好使用一种固定命名模式，例如"aaa:bbb:ccc"或"aaa.bbb.ccc"。

### String字符串

最简单的一种数据类型，可以是字符串或二进制数据(图片，序列化的对象等)，也可以存储数值(整形，小数等)。值的长度不超过512M。

### Hash哈希

hash类型代表了一系列的键值对，非常适合于表达一个对象objects，这个对象的属性作为键值对存储。

聚合类型当插入元素时，如果目标键不存在会创建一个空的聚合类型。当所有元素被移除时，键自动被销毁。

### List列表

常见的list有两种实现机制，双向链表linked list或数组array。这两种列表在某些操作中复杂度是不同的。Redis中基于的是linkedlist实现。

Redis Lists用linked list实现的原因是：对于数据库系统来说，至关重要的特性是：能非常快的在很大的列表上添加元素，还能在常数时间取得列表长度。

如果要快速访问某个大元素集合中的某个元素更重要，使用zset是更好的选择。

### Set集合

set是string的无序排列，能够表达数学概念上的集合，能够实现并集，交集，差集，获取随机内容等操作。

Redis集合有着不允许相同成员存在的优秀特性。向集合中多次添加同一元素，在集合中最终只会存在一个此元素。实际上这就意味着，在添加元素前，你并不需要事先进行检验此元素是否已经存在的操作。

### zset有序集合

Redis有序集合和Redis集合类似，是不包含相同字符串的合集。

每个有序集合的成员都关联着一个评分(可以是浮点数)，这个评分用于把有序集合中的成员按最低分到最高分排列。

## 基本命令

Redis命令十分丰富，包括的命令组有Cluster、Connection、Geo、Hashes、HyperLogLog、Keys、Lists、Pub/Sub、Scripting、Server、Sets、Sorted Sets、Strings、Transactions一共14个redis命令组两百多个redis命令。

### keys

| 命令 | 说明 |
|--------|--------|
|keys pattern   | 按模式匹配返回关键字  |
|dbsize         | 返回键的总个数        |
|del key[key]   | 根据键删除            |
|exists key[key]| 根据键判断是否存在    |
|randomkey      | 返回一个随机的key     |
|rename key nkey| 重新命名一个key       |
|renamenx key nkey| 重命令一个key       |
|expire key sec | 根据键设置按秒过期    |
|expireat key ts| 根据键设置按时间戳过期|
|persist key    | 移除键的过期设置      |
|pexpire key ms | 根据键设置按毫秒过期  |
|pexpireat key mts| 根据键设置过期      |
|ttl key        | 获取key的有效秒数     |
|pttl key       | 获取key的有效毫秒数   |
|migrate        | 原子性的将key从一个实例迁移到另一个实例|
|move key db    | 将key从实例中一个库迁移到另一个库|
|type key       | 获取key对应的存储类型 |
|objcect        | 获取内部的存储对象    |
|sort           | 排序                  |
|scan cursor [pattern][count]| 增量迭代遍历|

示例
```
127.0.0.1:6379> set key1 hello
OK
127.0.0.1:6379> set key2 world
OK
127.0.0.1:6379> keys *
1) "key1"
2) "key2"
127.0.0.1:6379> dbsize
(integer) 2
127.0.0.1:6379> exists key1
(integer) 1
127.0.0.1:6379> exists key3
(integer) 0
127.0.0.1:6379> randomkey
"key1"
127.0.0.1:6379> rename key1 key0
OK
127.0.0.1:6379> renamenx key2 key0
(integer) 0
127.0.0.1:6379> type key1
string
127.0.0.1:6379> del key1
(integer) 1
127.0.0.1:6379> expire key0 10
(integer) 1
127.0.0.1:6379> ttl key0
(integer) 4
127.0.0.1:6379> ttl key0
(integer) -2
127.0.0.1:6379> exists key0
(integer) 0
127.0.0.1:6379> set key1 hello
OK
127.0.0.1:6379> expire key1 20
(integer) 1
127.0.0.1:6379> ttl key1 
(integer) 16
127.0.0.1:6379> persist key1
(integer) 1
127.0.0.1:6379> ttl key1
(integer) -1
```

### strings

| 命令 | 说明 |
|--------|--------|
|set key value [ex][px][nx|xx] | 设置关键字和值   |
|get key                       | 根据关键字获取值 |
|mset key value [key value]    | 批量设置键值     |
|mget key [key]                | 批量获取         |
|setrange key start end        | 覆盖字符串部分   |
|getrange key start end        | 获取一个子字符串 |
|getset key nvalue             | 获取旧值并设新值 |
|append key value              | 追加一个值到key上|
|incr key                      | 数值执行原子加1  |
|incrby key mount              | 增加指定值       |
|incrbyfloat key mount         | 增加浮点数       |
|decr key                      | 数值减1          |
|decrby key mount              | 减指定值         |
|descbyfloat key mount         | 减指定浮点数     |
|strlen key                    | 获取指定键值长度 |

示例
```
127.0.0.1:6379> set key1 hello
OK
127.0.0.1:6379> set key2 world ex 20
OK
127.0.0.1:6379> set key2 world nx
OK
127.0.0.1:6379> set key2 world2 nx
(nil)
127.0.0.1:6379> get key2
"world"
127.0.0.1:6379> set key2 world xx
OK
127.0.0.1:6379> set key2 world2 xx
OK
127.0.0.1:6379> get key2
"world2"
127.0.0.1:6379> mset key3 python key4 java
OK
127.0.0.1:6379> mget key1 key3
1) "hello"
2) "python"
127.0.0.1:6379> set key5 11
OK
127.0.0.1:6379> get key5
"11"
127.0.0.1:6379> incr key5
(integer) 12
127.0.0.1:6379> incrby key5 4
(integer) 16
127.0.0.1:6379> incrby key5 -2
(integer) 14
127.0.0.1:6379> decr key5
(integer) 13
127.0.0.1:6379> append key3 2
(integer) 7
127.0.0.1:6379> get key3
"python2"
127.0.0.1:6379> getrange key1 2 4
"llo"
127.0.0.1:6379> getrange key1 2 -1
"llo"
```

### Hashes

| 命令 | 说明 |
|--------|--------|
|hset key field value    | 设置hash里一个字段的值 |
|hsetnx key field value  | 字段不存在时设置       |
|hget key field          | 获取hash里一个字段的值 |
|hexists key field       | 判断hash里一个字段是否存在 |
|hdel key field [f]      | 删除hash里一个字段的值 |
|hmset key field value [f v]| 批量设置hash里字段的值 |
|hmget key field [f]     | 批量获取hash里字段的值 |
|hstrlen key field       | 获取hash里字段值长度   |
|hincrby key field mount | 整数增                 |
|hincrbyfloat key field f| 浮点数增               |
|hlen key                | 获取hash里对应字段数   |
|hkeys key               | 获取hash里所有的字段   |
|hvals key               | 获取hash里所有的值     |
|hgetall key             | 获取hash里一个关键字下所有字段和值 |
|hscan key cursor [pattern]| 迭代hash里的元素     |

示例
```
127.0.0.1:6379> hset u1 name jack
(integer) 1
127.0.0.1:6379> hset u1 age 33
(integer) 1
127.0.0.1:6379> hkeys u1
1) "name"
2) "age"
127.0.0.1:6379> hvals u1
1) "jack"
2) "33"
127.0.0.1:6379> hgetall u1
1) "name"
2) "jack"
3) "age"
4) "33"
127.0.0.1:6379> hlen u1
(integer) 2
127.0.0.1:6379> hmset u1 addr tianjin page 33
OK
127.0.0.1:6379> hmget u1 name page
1) "jack"
2) "33"
127.0.0.1:6379> hexists u1 name
(integer) 1
127.0.0.1:6379> hincrby u1 page 3
(integer) 36
```

### Lists

| 命令 | 说明 |
|--------|--------|
|lpush key value [v]  | 在队列左边插入一个或多个元素 |
|rpush key value [v]  | 在队列右边插入一个或多个元素 |
|lpop key             | 队列左边弹出一个元素         |
|rpop key             | 队列右边弹出一个元素         |
|lpushx key value     | 当队列存在时插入一个元素     |
|rpushx key value     | 当队列存在时插入一个元素     |
|lrange key start stop| 从队列指定范围返回元素       |
|lindex key index     | 通过下标获取一个列表的元素   |
|lset key index value | 通过下标替换一个列表的元素   |
|ltrim key start stop | 裁剪保留一段范围内的列表元素 |
|lrem key count value | 删除一个列表里的元素         |
|linsert key before|after pivot value| 在某个元素前或后插入新元素 |
|llen key             | 返回列表长度                 |
|blpop key [k] timeout| 带阻塞的左侧弹出元素操作     |
|brpop key [k] timeout| 带阻塞的右侧弹出元素操作     |
|brpoplpush src dst tout| 带阻塞的弹出元素插入另一个队列  |
|rpoplpush src dst    | 非阻塞的，同上               |

示例
```
127.0.0.1:6379> rpush key1 a
(integer) 1
127.0.0.1:6379> rpush key1 b
(integer) 2
127.0.0.1:6379> rpush key1 c
(integer) 3
127.0.0.1:6379> rpush key1 d
(integer) 4
127.0.0.1:6379> rpush key1 e
(integer) 5
127.0.0.1:6379> lrange key1 0 -1
1) "a"
2) "b"
3) "c"
4) "d"
5) "e"
127.0.0.1:6379> lpush key2 a
(integer) 1
127.0.0.1:6379> lpush key2 b
(integer) 2
127.0.0.1:6379> lpush key2 c
(integer) 3
127.0.0.1:6379> lpush key2 d
(integer) 4
127.0.0.1:6379> lpush key2 e
(integer) 5
127.0.0.1:6379> lrange key2 0 -1
1) "e"
2) "d"
3) "c"
4) "b"
5) "a"
127.0.0.1:6379> lindex key1 0
"a"
127.0.0.1:6379> lindex key1 4
"e"
127.0.0.1:6379> lindex key1 5
(nil)
127.0.0.1:6379> llen key2
(integer) 5
127.0.0.1:6379> linsert key1 before x a
(integer) -1
127.0.0.1:6379> linsert key1 before e a
(integer) 6
127.0.0.1:6379> lrange key1 0 -1
1) "a"
2) "b"
3) "c"
4) "d"
5) "a"
6) "e"
127.0.0.1:6379> rpop key1
"e"
127.0.0.1:6379> lset key1 4 e
OK
127.0.0.1:6379> ltrim key2 1 3
OK
127.0.0.1:6379> lrange key2 0 -1
1) "d"
2) "c"
3) "b"
127.0.0.1:6379> RPOPLPUSH key1 key2 
"e"
```

### Sets

| 命令 | 说明 |
|--------|--------|
|sadd key member [m]   | 添加一个或多个元素到集合 |
|srem key member [m]   | 删除一个或多个元素       |
|scard key             | 获得集合里的元素数       |
|smembers key          | 获取集合里的所有元素     |
|sismember key member  | 判断一个元素是否是集合成员|
|spop key [count]      | 从集合中随机弹出某个元素 |
|srandmember key [count]| 从集合中随机返回某个元素|
|smove src dest member | 从集合移动到另一个集合   |
|sdiff key [key]       | 两个集合的差集           |
|sinter key [key]      | 两个集合的交集           |
|sunion key [key]      | 两个集合的并集           |
|sdiffstore dest key k | 差集保存                 |
|sunionstore dest k k  | 并集保存                 |
|sinterstore dest k k  | 交集保存                 |
|sscan key cursor [pattern]| 迭代遍历集合         |

示例
```
127.0.0.1:6379> sadd key1 1 2 3 4 5 6 7 8 9 
(integer) 9
127.0.0.1:6379> smembers key1
1) "1"
2) "2"
3) "3"
4) "4"
5) "5"
6) "6"
7) "7"
8) "8"
9) "9"
127.0.0.1:6379> SRANDMEMBER key1 
"5"
127.0.0.1:6379> Spop key1 
"5"
127.0.0.1:6379> sadd key1 5
(integer) 1
127.0.0.1:6379> scard key1
(integer) 9
127.0.0.1:6379> sadd key2 1 3 5 7 9
(integer) 5
127.0.0.1:6379> sdiff key2 key1
(empty list or set)
127.0.0.1:6379> sdiff key1 key2
1) "2"
2) "4"
3) "6"
4) "8"
127.0.0.1:6379> sinter key1 key2
1) "1"
2) "3"
3) "5"
4) "7"
5) "9"
127.0.0.1:6379> sismember key1 10
(integer) 0
```

### Sorted Sets

| 命令 | 说明 |
|--------|--------|
|zadd key [NX|XX] [CH] [INCR] score member [s m| 向有序集合添加元素和对应分数 |
|zcard key                     | 返回集合中成员数量                           |
|zscore key member             | 返回成员对应的分数                           |
|zcount key min max            | 返回集合中分数范围内成员数量                 |
|zlexcount key min max         | 返回成员之间的成员数量                       |
|zincrby key increment member  | 增加成员的分数                               |
|zrange key start stop[withscores]| 根据指定的下标返回成员                    |
|zrevrange key start stop      | 反序返回成员                                 |
|zrangebyscore key min max     | 返回成员                                     |
|zrevrangebyscore key min max  | 反序返回成员                                 |
|zrangebylex key min max       | 根据指定的成员内容字典排序返回成员，集合中的成员分数要一样，成员内容是ASIIC字符集|
|zrevrangebylex key min max    | 反序返回成员                                 |
|zrank key member              | 确定在序列中的排名                           |
|zrevrank key member           | 反序排名                                     |
|zrem key member [member]      | 删除集合中元素                               |
|zremrangebylex key min max    | 删除范围内元素                               |
|zremrangebyrank key start stop| 删除范围内元素                               |
|zremrangebyscore key min max  | 删除范围内元素                               |
|zinterstore key key           | 多个排序集的交集并保存                       |
|zunionstore key key           | 多个排序集的并集并保存                       |
|zscan key cursor [pattern]    | 迭代遍历集合                                 |

示例
```
127.0.0.1:6379> zadd key1 1 a 2 b 3 c 4 d 5 e
(integer) 5
127.0.0.1:6379> zadd key1 ch 1 a 3 c
(integer) 0
127.0.0.1:6379> zcard key1
(integer) 5
127.0.0.1:6379> zcount key1 2 4
(integer) 3
127.0.0.1:6379> zscore key1 b
"2"
127.0.0.1:6379> zrank key1 b
(integer) 1
127.0.0.1:6379> zrevrank key1 b
(integer) 3
127.0.0.1:6379> zrange key1 0 -1 withscores
 1) "a"
 2) "1"
 3) "b"
 4) "2"
 5) "c"
 6) "3"
 7) "d"
 8) "4"
 9) "e"
10) "5"
127.0.0.1:6379> zrangebyscore key1 2 4
1) "b"
2) "c"
3) "d"
127.0.0.1:6379> zrangebyscore key1 (2 4
1) "c"
2) "d"
# 根据分数删除大于等于2的所有成员
127.0.0.1:6379> zremrangebyscore key1 2 +inf
(integer) 4
```

