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

- 丰富的特性 – Redis还支持 publish/subscribe, 通知, key 过期等等特性。

## 数据类型

Redis当前支持的数据类型包括：string,hash,list,set,zset(sorted set),bitmaps,hyperloglogs,geospatial.

### keys关键字

Redis中的关键字是二进制安全的，这意味着你可以使用任意二进制序列作为关键字，例如字符串或一个JPEG图片内容或空字符串。

关于key的几个原则:

- 太长的键值不是一个好的实践，对内存空间和操作时间都会产生大量消耗。

- 太短的键值也不是一个好的主意，容易造成关键字的冲突或歧意。

- 最好使用一种固定命名模式，例如"aaa:bbb:ccc"或"aaa.bbb.ccc"。

### String字符串

最简单的一种数据类型，可以是字符串或二进制数据，也可以存储数值(整形，小数等)。值的长度不超过512M。

### Hash哈希

hash类型代表了一系列的键值对，非常适合于表达一个对象objects，这个对象的属性作为键值对存储。

Redis中对小规模的hashmap进行了优化，以特殊方式编码以优化内存占用

### List列表

常见的list有两种实现机制，双向链表linked list或数组array。这两种列表在某些操作中复杂度是不同的。Redis中基于的是linkedlist实现。

Redis Lists用linked list实现的原因是：对于数据库系统来说，至关重要的特性是：能非常快的在很大的列表上添加元素，还能在常数时间取得列表长度。

如果要快速访问某个大元素集合中的某个元素更重要，使用zset是更好的选择。

### Set集合

set是string的无序排列，能够表达数学概念上的集合，能够实现并集，交集，差集，获取随机内容等操作。

set适合用于表示对象间的关系，

### zset有序集合

## 基本命令

