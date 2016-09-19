# 迭代器和生成器

## 基本概念

循环（loop），指的是在满足条件的情况下，重复执行同一段代码。比如，while语句。

迭代（iterate），指的是按照某种顺序逐个访问列表中的每一项。比如，for语句。

递归（recursion），指的是一个函数不断调用自身的行为。比如，以编程方式输出著名的斐波纳契数列。

遍历（traversal），指的是按照一定的规则访问树形结构中的每个节点，而且每个节点都只访问一次。

### 中英文对照

**iterable**

An object capable of returning its members one at a time. Examples of iterables include all sequence types (such as list, str, and tuple) and some non-sequence types like dict and file and objects of any classes you define with an `__iter__()` or `__getitem__() `method. Iterables can be used in a for loop and in many other places where a sequence is needed (zip(), map(), ...). When an iterable object is passed as an argument to the built-in function iter(), it returns an iterator for the object. This iterator is good for one pass over the set of values. When using iterables, it is usually not necessary to call iter() or deal with iterator objects yourself. The for statement does that automatically for you, creating a temporary unnamed variable to hold the iterator for the duration of the loop. See also iterator, sequence, and generator.

**可迭代对象**

每次迭代能返回一个内部成员的对象(迭代容器)。迭代容器对象包括所有的序列类型(如list,str,tuple)和一些非序列类型(如dic)和file类型，或者任何实现了`__iter__`或`__getitem__()`方法的自定义类。迭代容器可以在for循环或者一些序列类型支持的操作(`zip()`,`map()`...)中使用。当一个迭代容器作为参数被传递给内建函数`iter()`会返回一个迭代器。当使用迭代容器时，一般不需要调用iter()来单独处理返回的迭代器，在for语句中实际分配了一个未命名变量对应此返回的迭代器。另外参见iterator,sequence,gererator

**iterator**

An object representing a stream of data. Repeated calls to the iterator’s next() method return successive items in the stream. When no more data are available a StopIteration exception is raised instead. At this point, the iterator object is exhausted and any further calls to its next() method just raise StopIteration again. Iterators are required to have an `__iter__()` method that returns the iterator object itself so every iterator is also iterable and may be used in most places where other iterables are accepted. One notable exception is code which attempts multiple iteration passes. A container object (such as a list) produces a fresh new iterator each time you pass it to the iter() function or use it in a for loop. Attempting this with an iterator will just return the same exhausted iterator object used in the previous iteration pass, making it appear like an empty container.

**迭代器**

将一系列数据以流的方式呈现的对象。重复调用迭代器对象的next()方法会返回流中当前对象的下一个数据，当流结束没有数据时会抛出StopIteration异常。而迭代器的`__iter__()`方法将返回迭代器自身，所以迭代器也是一个迭代容器，并且可以用到迭代容器被接受处理的地方。一种常见的代码编写错误是多次迭代，一个迭代容器每次通过iter()或loop循环都会产生新的迭代器，如果没有新迭代器，每次迭代完成后再进行迭代操作会导致异常。

**generator**

A function which returns an iterator. It looks like a normal function except that it contains yield statements for producing a series of values usable in a for-loop or that can be retrieved one at a time with the next() function. Each yield temporarily suspends processing, remembering the location execution state (including local variables and pending try-statements). When the generator resumes, it picks-up where it left-off (in contrast to functions which start fresh on every invocation).

**生成器**

一个能返回迭代器的函数，看上去就像一个普通函数只是里面包含了yield语句。yield返回的一系列值能够被for循环或next()获取使用。每次yield将临时的挂起当前函数处理流程(保留了当前函数里的位置，变量和try语句信息等)，直到外部处理完成又进入迭代从刚才的位置继续往下处理。普通的函数每次重新进入都是从入口到结束。


*迭代类型和生成器类型，参见 builtintypes 文档*

### 综述

1.通过实现迭代器协议对应的`__iter__()`和`next()`方法，可以自定义迭代器类型。对于可迭代对象，for语句可以通过iter()方法获取迭代器，并且通过next()方法获得容器的下一个元素。

2.像列表这种序列类型的对象，可迭代对象和迭代器对象是相互独立存在的，在迭代的过程中各个迭代器相互独立；但是，有的可迭代对象本身又是迭代器对象，那么迭代器就没法独立使用(多次迭代)。

3.itertools模块提供了一系列迭代器，能够帮助用户轻松地使用排列、组合、笛卡尔积或其他组合结构。

4.生成器是一种特殊的迭代器，内部支持了生成器协议，不需要明确定义`__iter__()`和`next()`方法。

5.生成器通过生成器函数产生，生成器函数可以通过常规的def语句来定义，但是不用return返回，而是用yield一次返回一个结果。

## 示例

 - 自定义迭代器和迭代容器
```
class DataIter(object):
    def __init__(self, data):
        self._index = 0
        self._data = data._data

    def __iter__(self):
        return self

    def next(self):
        if self._index >= len(self._data):
            raise StopIteration()

        d = self._data[self._index]
        self._index += 1
        return d

class Data(object):
    def __init__(self, *args):
        self._data = list(args)

    def __iter__(self):
        return DataIter(self)

```

 - 迭代器的使用
```
>>> import iterA
>>> d = iterA.Data(1,2,3,4)
>>> type(d)
<class 'iterA.Data'>
# 通过for循环迭代
>>> for i in d:
...     print i
... 
1
2
3
4
# 通过iter,next进行迭代
>>> it = iter(d)
>>> print it
<iterA.DataIter object at 0x7f68e656cf50>
>>> print it.__iter__()
<iterA.DataIter object at 0x7f68e656cf50>
>>> it
<iterA.DataIter object at 0x7f68e656cf50>
>>> next(it)
1
>>> b = next(it)
>>> print b
2
>>> print type(b)
<type 'int'>
>>> next(it)
3
>>> next(it)
4
>>> next(it)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "iterA.py", line 22, in next
    raise StopIteration()
StopIteration
```

 - 生成器定义
```
class Data(object):
    def __init__(self, *args):
        self._data = list(args)

    # 返回迭代器的接口用yield产生
    def __iter__(self):
        for x in self._data:
		   yield x
```

 - 生成器的执行顺序
```
>>> def foo():
...     print "begin"
...     for i in range(3):
...         print "before yield", i
...         yield i
...         print "after yield", i
...     print "end"
...
>>> f = foo()
>>> f.next()
begin
before yield 0
0
>>> f.next()
after yield 0
before yield 1
1
>>> f.next()
after yield 1
before yield 2
2
>>> f.next()
after yield 2
end
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
>>>
```

 - file类型支持迭代
```
abc.txt
aaaa
bbbb
cccc
dddd
>>> f = open("abc.txt")
>>> for line in f:
...     print line,
... 
>>> aaaa
>>> bbbb
>>> cccc
>>> dddd
>>> f = open('abc.txt')
>>> [line for line in f]
['aaaa\n', 'bbbb\n', 'cccc\n', 'dddd\n']
#更简洁的写法，list支持传递参数iterable
>>> list(open('abc.txt'))
['aaaa\n', 'bbbb\n', 'cccc\n', 'dddd\n']
```


## 更多的生成器

### 生成器表达式

生成器表达式是在python2.4中引入的，当序列过长，而每次只需要获取一个元素时，应当考虑使用生成器表达式而不是列表推导式。
生成器表达式的语法和列表推导式一样，只不过生成器表达式是被()括起来的，而不是[]
```
>>> gen = (i for i in range(50) if i%2)
>>> type(gen)
<type 'generator'>
>>> [i for i in gen]
[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49]
>>> gen
<generator object <genexpr> at 0x7f331abc3af0>
# 使用一次后的再次迭代
>>> [i for i in gen]
[]
```

### 生成器的send()和close()方法
- send(value):

Python 2.5中，yield语句变成了yield表达式，也就是说yield可以有一个值，而这个值就是send()方法的参数。
所以send(None)和next()是等效的。同样，next()和send()的返回值都是yield语句处的参数（yielded value）

关于send()方法需要注意的是：调用send传入非None值前，生成器必须处于挂起状态，否则将抛出异常。
也就是说，第一次调用时，要使用next()语句或send(None)，因为没有yield语句来接收这个值。

- close():

这个方法用于关闭生成器，对关闭的生成器后再次调用next或send将抛出StopIteration异常。

示例
```
>>> def consumer():
... while True:
... d = yield
... if not d: break
... print "consumer:", d
>>> c = consumer() # 创建消费者
>>> c.send(None)  # 启动消费者
>>> c.send(1)  # 生产数据，并提交给消费者。
consumer: 1
>>> c.send(2)
consumer: 2
>>>c.send(3)
consumer: 3
>>> c.send(None) # 生产结束，通知消费者结束。
StopIteration
```