
## 事务的基本要素（ACID）

1、原子性（Atomicity）：事务开始后所有操作，要么全部做完，要么全部不做，不可能停滞在中间环节。事务执行过程中出错，会回滚到事务开始前的状态，所有的操作就像没有发生一样。也就是说事务是一个不可分割的整体，就像化学中学过的原子，是物质构成的基本单位。

2、一致性（Consistency）：事务开始前和结束后，数据库的完整性约束没有被破坏 。比如A向B转账，不可能A扣了钱，B却没收到。

3、隔离性（Isolation）：同一时间，只允许一个事务请求同一数据，不同的事务之间彼此没有任何干扰。比如A正在从一张银行卡中取钱，在A取钱的过程结束前，B不能向这张卡转账。

4、持久性（Durability）：事务完成后，事务对数据库的所有更新将被保存到数据库，不能回滚。

## 事务的并发问题

1、脏读：事务A读取了事务B更新的数据，然后B回滚操作，那么A读取到的数据是脏数据

2、不可重复读：事务 A 多次读取同一数据，事务 B 在事务A多次读取的过程中，对数据作了更新并提交，导致事务A多次读取同一数据时，结果 不一致。

3、幻读：系统管理员A将数据库中所有学生的成绩从具体分数改为ABCDE等级，但是系统管理员B就在这个时候插入了一条具体分数的记录，当系统管理员A改结束后发现还有一条记录没有改过来，就好像发生了幻觉一样，这就叫幻读。

小结：不可重复读的和幻读很容易混淆，不可重复读侧重于修改，幻读侧重于新增或删除。解决不可重复读的问题只需锁住满足条件的行，解决幻读需要锁表

## MySQL事务隔离级别

| 事务隔离级别 | 脏读 | 不可重复读 | 幻读 |
|--------|--------|--------|--------|
|读未提交read-uncommitted| 是 | 是 | 是 |
|不可重复读read-committed| 否 | 是 | 是 |
|可重复读repeatable-read | 否 | 否 | 是 |
|串行化serializable      | 否 | 否 | 否 |

## 示例

### read-uncommitted

事务A

```
# 隔离级别
MariaDB [test]> set session transaction isolation level read uncommitted;
Query OK, 0 rows affected (0.00 sec)

# 没有被其他事务改动
MariaDB [test]> select * from aa;
+------+------+-----+
| id   | name | num |
+------+------+-----+
|    1 | cccc |   1 |
|    2 | bbbb |   2 |
+------+------+-----+
2 rows in set (0.00 sec)

# B在未提交事务里改动了一条记录，被查询出来
MariaDB [test]> select * from aa;
+------+------+-----+
| id   | name | num |
+------+------+-----+
|    1 | cccc |   1 |
|    2 | aaa  |   2 |
+------+------+-----+
2 rows in set (0.00 sec)

# B事务回滚了
MariaDB [test]> select * from aa;
+------+------+-----+
| id   | name | num |
+------+------+-----+
|    1 | cccc |   1 |
|    2 | bbbb |   2 |
+------+------+-----+
2 rows in set (0.00 sec)
```

B事务

```
# 事务显式开始
MariaDB [test]> begin;
Query OK, 0 rows affected (0.00 sec)

MariaDB [test]> select * from aa;
+------+------+-----+
| id   | name | num |
+------+------+-----+
|    1 | cccc |   1 |
|    2 | bbbb |   2 |
+------+------+-----+
2 rows in set (0.00 sec)

# 更新了一条记录，会被A事务读取到脏记录
MariaDB [test]> update aa set name='aaa' where num=2;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0

# 回滚
MariaDB [test]> rollback;
Query OK, 0 rows affected (0.07 sec)

MariaDB [test]> select * from aa;
+------+------+-----+
| id   | name | num |
+------+------+-----+
|    1 | cccc |   1 |
|    2 | bbbb |   2 |
+------+------+-----+
2 rows in set (0.00 sec)

```

### read-committed

A事务
```
# 设置事务级别
MariaDB [(none)]> set session transaction isolation level read committed;
Query OK, 0 rows affected (0.00 sec)
MariaDB [test]> begin;
Query OK, 0 rows affected (0.01 sec)
# 没有任何其他事务时
MariaDB [test]> select * from aa where num=1;
+------+------+-----+
| id   | name | num |
+------+------+-----+
|    1 | cccc |   1 |
+------+------+-----+
1 row in set (0.00 sec)

# B事务发生了修改但未提交时
MariaDB [test]> select * from aa where num=1;
+------+------+-----+
| id   | name | num |
+------+------+-----+
|    1 | cccc |   1 |
+------+------+-----+
1 row in set (0.00 sec)
# B事务发生了修改并提交后
MariaDB [test]> select * from aa where num=1;
+------+------+-----+
| id   | name | num |
+------+------+-----+
|    1 | xxxx |   1 |
+------+------+-----+
1 row in set (0.00 sec)
# A事务结束
MariaDB [test]> commit;
Query OK, 0 rows affected (0.00 sec)
MariaDB [test]> select * from aa where num=1;
+------+------+-----+
| id   | name | num |
+------+------+-----+
|    1 | xxxx |   1 |
+------+------+-----+
1 row in set (0.00 sec)
```

B事务
```
MariaDB [test]> begin;
Query OK, 0 rows affected (0.00 sec)

MariaDB [test]> update aa set name='xxxx' where num=1;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
# 在修改但未提交前影响了A事务
MariaDB [test]> commit;
Query OK, 0 rows affected (0.02 sec)
```

### repeatable-read

A事务
```
# 设置事务级别
MariaDB [test]> set session transaction isolation level repeatable read;
Query OK, 0 rows affected (0.00 sec)

# 事务开启
MariaDB [test]> begin;
Query OK, 0 rows affected (0.00 sec)
# 没有其他事务时
MariaDB [test]> select * from aa where num=2;
+------+------+-----+
| id   | name | num |
+------+------+-----+
|    2 | bbbb |   2 |
+------+------+-----+
1 row in set (0.00 sec)
# B事务修改了未提交
MariaDB [test]> select * from aa where num=2;
+------+------+-----+
| id   | name | num |
+------+------+-----+
|    2 | bbbb |   2 |
+------+------+-----+
1 row in set (0.00 sec)
# B事务修改了并已提交，还是不应向A事务
MariaDB [test]> select * from aa where num=2;
+------+------+-----+
| id   | name | num |
+------+------+-----+
|    2 | bbbb |   2 |
+------+------+-----+
1 row in set (0.00 sec)

MariaDB [test]> commit;
Query OK, 0 rows affected (0.00 sec)
# A事务结束后可以看到B事务的修改
MariaDB [test]> select * from aa where num=2;
+------+------+-----+
| id   | name | num |
+------+------+-----+
|    2 | dddd |   2 |
+------+------+-----+
1 row in set (0.00 sec)
```

B事务
```
MariaDB [test]> begin;
Query OK, 0 rows affected (0.00 sec)

MariaDB [test]> update aa set name='dddd' where num=2;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0

MariaDB [test]> commit;
Query OK, 0 rows affected (0.01 sec)
````

### 幻读

### 串行化serializable

A事务
```
# 设置隔离级别
MariaDB [(none)]> set session transaction isolation level serializable;
Query OK, 0 rows affected (0.00 sec)

MariaDB [test]> select * from aa;
+------+------+-----+
| id   | name | num |
+------+------+-----+
|    1 | xxxx |   1 |
|    2 | dddd |   2 |
+------+------+-----+
2 rows in set (0.00 sec)

# A先开启事务，锁定aa表
MariaDB [test]> begin;
Query OK, 0 rows affected (0.00 sec)

MariaDB [test]> update aa set name='bbbb' where num=1;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0

# rollback前导致B事务查询卡主
MariaDB [test]> rollback;
Query OK, 0 rows affected (0.04 sec)

MariaDB [test]> begin;
Query OK, 0 rows affected (0.00 sec)
# B事务后执行，此时被阻塞超时
MariaDB [test]> update aa set name='bbbb' where num=1;
ERROR 1213 (40001): Deadlock found when trying to get lock; try restarting transaction
MariaDB [test]>
```

B事务
```
# 设置隔离级别
MariaDB [test]>  set session transaction isolation level serializable;
Query OK, 0 rows affected (0.00 sec)

MariaDB [test]>
MariaDB [test]> begin;
Query OK, 0 rows affected (0.00 sec)
# 查询被A第一次阻塞，直到rollback后继续执行
MariaDB [test]> select * from aa;
+------+------+-----+
| id   | name | num |
+------+------+-----+
|    1 | xxxx |   1 |
|    2 | dddd |   2 |
+------+------+-----+
2 rows in set (18.17 sec)

# 此时获得了锁，导致A事务第二次执行超时
MariaDB [test]> update aa set name='aaaa' where num=1;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
```