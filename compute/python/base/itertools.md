# itertools — 创建高效迭代器的函数

## 无限迭代器

生成的迭代器可以无限循环，用户需要控制结束条件。注意返回的是迭代器，需要按照迭代器的使用方法使用才能获取实际值。

|方法定义|使用说明|
|--------|--------|
|itertools.count(start=0, step=1)| 从start开始，以step作为步进无限循环。参数可以使用浮点数 |
|itertools.cycle(iterable)| 无限循环可迭代的元素 |
|itertools.repeat(object[, times])| 循环返回对象，如果指定次数限制times则会终止 |

示例
- count
```
>>> aa = itertools.count(3,4)
>>> type(aa)
<type 'itertools.count'>
>>> next(aa)
3
>>> next(aa)
7
>>> next(aa)
11
>>> aa = itertools.count(2.0, 1.1)
>>> next(aa)
2.0
>>> next(aa)
3.1
>>> next(aa)
4.2
```

- cycle
```
>>> for i, v in enumerate(itertools.cycle('abc')):
...     if i > 7:
...         break
...     else:
...         print v
... 
a
b
c
a
b
c
a
```

- repeat
```
# 常用来生成入参
>>> list(imap(pow, xrange(10), repeat(2)))
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

## 有限迭代器

|方法定义|使用说明|
|--------|--------|
|itertools.chain(*iterables)| 生成一个迭代器，用于将连续的多个序列作为一个单独的序列。 |
|itertools.compress(data, selectors)| 按条件表selectors过滤迭代器元素。 |
|itertools.dropwhile(predicate, iterable)| 从头部开始符合条件的drop掉，一旦遇到不符合则返回其及后续所有的。 |
|itertools.takewhile(predicate, iterable)| 从头部开始符合条件的保留，一旦遇到不符合的则中断执行 |
|itertools.groupby(iterable[, key])| 将连续出现的相同元素进行分组，或按key转换为新的可迭代组。 |
|itertools.ifilter(predicate, iterable)| 按条件真值过滤，如果predicate是none，相当于true |
|itertools.ifilterfalse(predicate, iterable)| 按条件假值过滤，如果p是none，相当于false。 |
|itertools.imap(function, *iterables)| 与map相似，但在迭代元素参数不一样长时更有用 |
|itertools.starmap(function, iterable)| 与imap的区别相当于fun(a,b)和fun(*c) |
|itertools.islice(iterable, stop)| 按切片的方式迭代 |
|itertools.islice(iterable, start, stop[, step])|  |
|itertools.tee(iterable[, n=2])| 复制迭代器，一旦被分裂原可迭代容器不可再用 |
|itertools.izip(*iterables)| 与zip相似，但在迭代元素参数不一样长时更有用 |
|itertools.izip_longest(*iterables[, fillvalue])| 与zip相似，提供了补缺值 |


示例
- chain
```
>>> it = chain(xrange(3), "abc")
>>> list(it)
[0, 1, 2, 'a', 'b', 'c']
```

- compress
```
# 注意是按最短的参数进行处理的
>>> list(itertools.compress(xrange(5), [1,0,0,1]))
[0, 3]
>>> list(itertools.compress(xrange(5), [1,0,0,1,1]))
[0, 3, 4]
>>> list(itertools.compress(xrange(5), [1,0,0,1,1,1]))
[0, 3, 4]
>>> 
```

- dropwhile,takewhile
```
>>> list(itertools.dropwhile(lambda x:x>4, [1,2,3,4,5,6,7]))
[1, 2, 3, 4, 5, 6, 7]
>>> list(itertools.dropwhile(lambda x:x<4, [1,2,3,4,5,6,7]))
[4, 5, 6, 7]
>>> list(itertools.dropwhile(lambda x:x<=4, [1,2,3,4,5,6,7]))
[5, 6, 7]
>>>
>>> list(itertools.takewhile(lambda x:x>4, [1,2,3,4,5,6,7]))
[]
>>> list(itertools.takewhile(lambda x:x<4, [1,2,3,4,5,6,7]))
[1, 2, 3]
>>> list(itertools.takewhile(lambda x:x<=4, [1,2,3,4,5,6,7]))
[1, 2, 3, 4]
>>> 
```

- groupby
```
# 一种典型应用，按某种分组方法将原迭代划分为3个新的迭代
>>> def height_class(h):
...     if h>180:
...         return 'tall'
...     elif h<160:
...         return 'short'
...     else:
...         return 'middle'
... 
>>> friends = [191, 158, 159, 165, 170, 177, 181, 182, 190]
# 注意此处排序，一般使用了key就需要先排序，保证元素顺序。如果没有key，则将元素自身作为key
>>> friends = sorted(friends,key = height_class)
>>> friends
[165, 170, 177, 158, 159, 191, 181, 182, 190]
>>>
>>> for m,n in itertools.groupby(friends,key = height_class):
...     print m
...     print list(n)
... 
middle
[165, 170, 177]
short
[158, 159]
tall
[191, 181, 182, 190]
>>> 
>>> # 不带key参数的示例
>>> for m,n in itertools.groupby('AAABBCBB'):
...     print m
...     print n
... 
A
['A', 'A', 'A']
B
['B', 'B']
C
['C']
B
['B', 'B']
```

- ifilter,imap
```
>>> it = ifilter(lambda x: x % 2, xrange(10))
>>> list(it)
[1, 3, 5, 7, 9]
>>> it = ifilterfalse(lambda x: x % 2, xrange(10))
>>> list(it)
[0, 2, 4, 6, 8]
>>> 
# 注意map和imap的差别
>>> list(map(pow, [1,2,3,4],[2,2,3,3]))
[1, 4, 27, 64]
>>> list(map(pow, [1,2,3,4,5],[2,2,3,3]))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for ** or pow(): 'int' and 'NoneType'
>>> 
>>> list(itertools.imap(pow, [1,2,3,4,5],[2,2,3,3]))
[1, 4, 27, 64]
```

- islice
```
>>> list(itertools.islice('ABCDEDF',2))
['A', 'B']
>>> list(itertools.islice('ABCDEDF',1,5,2))
['B', 'D']
>>> list(itertools.islice('ABCDEDF',2,6))
['C', 'D', 'E', 'D']
>>> 
```

- izip
```
>>> it = izip("abc", [1, 2])
>>> list(it)
[('a', 1), ('b', 2)]
>>> it = izip_longest("abc", [1, 2], fillvalue = 0)
>>> list(it)
[('a', 1), ('b', 2), ('c', 0)]
```

- tee
```
# 返回的是元组，对应复制了原来的迭代器
>>> c,d,e = itertools.tee('abcde',3)
>>> type(c)
<type 'itertools.tee'>
>>> for i in c:
...     print i,
... 
a b c d e
>>> for i in c:
...     print i,
... 
>>>
# 可以对复制出的迭代分别进行不同的操作
>>> for i in e:
...     print ord(i),
... 
97 98 99 100 101
# 注意不可对原迭代器再进行迭代操作
```

## 组合生成器

|方法定义|使用说明|
|--------|--------|
|itertools.product(*iterables[, repeat])| 笛卡尔积，如果有repeat表示自身的乘积次数 |
|itertools.permutations(iterable[, r])| 排列，迭代中每个元素和迭代中除自己的元素组合成一个长度为r的tuple，如r未指定则是全部元素|
|itertools.combinations(iterable, r)| 组合,迭代中每个元素和其后面的元素合成一个长度为r的tuple |
|itertools.combinations_with_replacement(iterable, r)| 同上，但包含自身 |

示例

- product
```
>>> list(itertools.product('ab','xy'))
[('a', 'x'), ('a', 'y'), ('b', 'x'), ('b', 'y')]
>>> list(itertools.product('abc','xy'))
[('a', 'x'), ('a', 'y'), ('b', 'x'), ('b', 'y'), ('c', 'x'), ('c', 'y')]
>>> 
>>> list(itertools.product(range(2),repeat=3))
[(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
>>> list(itertools.product([0,1],[0,1],[0,1]))
[(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
```

- permutations
```
>>> list(itertools.permutations('ABCD',1))
[('A',), ('B',), ('C',), ('D',)]
>>> list(itertools.permutations('ABCD',2))
[('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'A'), ('B', 'C'), ('B', 'D'), ('C', 'A'), ('C', 'B'), ('C', 'D'), ('D', 'A'), ('D', 'B'), ('D', 'C')]
>>> 
>>> list(itertools.permutations('ABCD',3))
[('A', 'B', 'C'), ('A', 'B', 'D'), ('A', 'C', 'B'), ('A', 'C', 'D'), ('A', 'D', 'B'), ('A', 'D', 'C'), ('B', 'A', 'C'), ('B', 'A', 'D'), ('B', 'C', 'A'), ('B', 'C', 'D'), ('B', 'D', 'A'), ('B', 'D', 'C'), ('C', 'A', 'B'), ('C', 'A', 'D'), ('C', 'B', 'A'), ('C', 'B', 'D'), ('C', 'D', 'A'), ('C', 'D', 'B'), ('D', 'A', 'B'), ('D', 'A', 'C'), ('D', 'B', 'A'), ('D', 'B', 'C'), ('D', 'C', 'A'), ('D', 'C', 'B')]
>>> list(itertools.permutations('ABB',2))
[('A', 'B'), ('A', 'B'), ('B', 'A'), ('B', 'B'), ('B', 'A'), ('B', 'B')]
```

- combinations
```
>>> list(itertools.combinations('abcd',2))
[('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('b', 'd'), ('c', 'd')]
>>> 
>>> list(itertools.combinations('ABB',2))
[('A', 'B'), ('A', 'B'), ('B', 'B')]
>>> 
>>> list(itertools.combinations_with_replacement('ABB',2))
[('A', 'A'), ('A', 'B'), ('A', 'B'), ('B', 'B'), ('B', 'B'), ('B', 'B')]
>>>
```