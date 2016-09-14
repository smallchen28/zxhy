# Built-in Functions 内置方法

## 内置类型

### 字符与字符串
- basestring()
抽象类型，是str和unicode的父类。不能实例化，只能用来判断一个对象是否是这个类型
```
>>> isinstance(u'中文', basestring)
True
>>> isinstance(u'中文', (unicode))
True
>>> isinstance(u'中文', (str))
False
>>> isinstance(u'中文', (str,unicode))
True
```

- chr(i)
返回只有一个字符(ASCII表中的字符)的字符串。参数必须在0-255之间，否则抛出ValueError。另外参见ord(),unichr()
```
>>> chr(97)
'a'
>>> chr(2)
'\x02'
```

- class str(object='') 
将一个对象转换为str类型，注意与repr(obj)的区别
```
>>> a=[1,2,3,4]
>>> b=str(a)
>>> print b
[1, 2, 3, 4] # str对象b
>>> len(b)
12
```

- unichr(i) 
将一个整型值转换为unicode单字符串，另外参见chr,ord

- unicode(object='') unicode(object[, encoding[, errors]]) 
返回一个unicode字符串

### 数值类型
- class bool([x]) 
判断一个对象并返回bool值对象，只有True和False两种
```
>>> bool([])
False
>>> bool([1])
True
>>> bool([0,0])
True
>>> bool(None)
False
```

- class int(x=0) class int(x, base=10)
从一个数值或字符转换为整型值。可以指定进制
```
>>> int(11)
11
>>> int('123')
123
>>> int('10F', 16)
271
>>> int('101100', 2)
44
```

- class long(x=0) class long(x, base=10)
构建一个长整型对象

- class float([x]) 
从数值或字符串返回浮点数

- class complex([real[, imag]])
创建一个复数对象

### 序列，集合，字典
- class dict(**kwarg) class dict(mapping, **kwarg) class dict(iterable, **kwarg)
构造一个字典对象
```
>>> da = dict(a=1,b=2,c=3)
>>> db = dict(da, d=4)
>>> print db
{'a': 1, 'c': 3, 'b': 2, 'd': 4}
```

- class bytearray([source[, encoding[, errors]]]) 
返回一个新的字节数组

- class list([iterable]) 
将一个可迭代对象转换为列表

- tuple([iterable]) 
将迭代对象转换为元组并保持原来的顺序

- class set([iterable]) 
根据迭代对象生成一个集合，另外参见frozenset

- frozenset([iterable])
返回一个新的frozenset对象，如果可选参数iterable存在，frozenset的元素来自于iterable。

- memoryview(obj)
构建一个内存视图对象

- class slice(stop) class slice(start, stop[, step]) 
返回一个slice对象，表示由索引range(start, stop, step)指出的集合。

## 数值相关

### 数值计算
- abs()
返回数值的绝对值，参数可以是整型，浮点型，复数
```
>>> abs(11.2)
11.2
>>>
>>> abs(-11.2)
11.2
>>> abs(-11)
11
>>> abs(12343433332.2323)
12343433332.2323
>>>
```

- divmod(a, b)
对整型变量来说相当于返回(a // b, a % b). 

- pow(x, y[, z]) 
进行指数运算，如果只有xy，则等同于`x**y`。如果有z则相当于`(x**y)%z`

- round(number[, ndigits]) 
对小数部分进行四舍五入操作，返回一个浮点数

- cmp(x, y)
比较两个对象并根据结果返回一个整型，如果x<y返回负数，相等返回0，x>y返回正数
```
>>> cmp(11,2)
1
>>> cmp(11,11)
0
```

- hash(object) 
返回对象的hash值(如果有的话).hash值是一个整型，通常用来在字典中快速定位。
两个数值型即使类型不一样如果compare结果一样，则hash值也是一样的。例如1和1.00
```
>>> hash(10)
10
>>> hash(10.000)
10
>>> hash(10.001)
2905810505
>>> 
```

### 数值和字符串转换
- bin(x)
将整型数值转换为二进制字符串，如果一个对象不是整型但通过实现`__index__()`方法返回整型，则使用此方法的返回值转换。
```
>>> bin(123)
'0b1111011'
>>> bin(-123)
'-0b1111011'
>>> bin(9123)
'0b10001110100011'
```

- hex(x) 
将一个整型数值转换为小写的十六进制字符串显示。另外参见int(),float.hex()
```
>>> hex(255)
'0xff'
>>> hex(15)
'0xf'
```

- oct(x)
将整型数值转换为8进制显示的字符串

- ord(c) 
将只有一个字符串转换为数值，另外参见chr,unichr

## 输入输出

### 格式化
- format(value[, format_spec]) 
将值进行格式化

- print(*objects, sep=' ', end='\n', file=sys.stdout) 
将对象输出到文件流中

- input([prompt])
等同于eval(raw_input(prompt)).建议使用raw_input

- raw_input([prompt])
根据提示进行输入，将输入值保存在字符串对象中

### 文件
- open(name[, mode[, buffering]])
打开文件并返回一个文件类型的对象

- file(name[, mode[, buffering]]) 
file类型的构造方法，和open类似。但推荐使用open，而file用来对对象类型进行判断

## 迭代相关

### 真值测试
- all(iterable)
迭代对象全部为真或空则返回True。另外参见any方法
```
>>> all([1,2,3,4,6])
True
>>> all([1,2,3,4,0])
False
>>> all([])
True
# 非常方便的判断一个迭代中的对象是否都符合某个条件
all(word in dicts for word in words)
```

- any(iterable)
迭代对象有任意一个为真则返回True。另外参见all方法
```
>>> any([])
False
>>> any([1,0])
True
>>> any([0,0])
False
```

### 循环遍历的方法
- enumerate(sequence, start=0) 
将一个序列或可迭代对象进行枚举。返回值包含一个序列值和序列中迭代出的对象
```
>>> for idx,val in enumerate(['a','b','c']):
...     print idx, val
...
0 a
1 b
2 c
>>> for idx,val in enumerate(['a','b','c'], 4):
...     print idx, val
...
4 a
5 b
6 c
```

- zip([iterable, ...]) 
将多个迭代对象合并产生一个元组列表。还支持反向解压操作
```
>>> x = [1, 2, 3]
>>> y = [4, 5, 6]
>>> zipped = zip(x, y)
>>> zipped
[(1, 4), (2, 5), (3, 6)]
>>> x2, y2 = zip(*zipped)
>>> x == list(x2) and y == list(y2)
True
```

- filter(function, iterable) 
构造一个列表，列表的元素来自于iterable，对于这些元素function返回真。
iterable可以是个序列，支持迭代的容器，或者一个迭代器。如果iterable是个字符串或者元组，则结果也是字符串或者元组；否则结果总是列表。
如果function是None，使用特性函数，即为假的iterable被移除。

- map(function, iterable, ...) 
将function应用于iterable的每一个元素，返回结果的列表。如果有多个参数并行的传递给func。另外参见filter,reduce方法

- reduce(function, iterable[, initializer])
对迭代对象按递归方式套用方法，另外参见filter,map
它是这样一个过程：每次迭代，将上一次的迭代结果（第一次时为init的元素，如没有init则为seq的第一个元素）与下一个元素一同执行一个二元的func函数。
```
>>> ft=lambda x:x.isdigit()
>>> aa
['12', 'ab', '', '12c', '009']
>>> filter(None, aa)
['12', 'ab', '12c', '009']
>>> filter(ft, aa)
['12', '009']
>>> 
>>> aa
['12', 'ab', '', '12c', '009']
>>> mp=lambda x:len(x)
>>> map(mp, aa)
[2, 2, 0, 3, 3]
>>> bb
['34', 'cc', 'aa', '777', '']
>>> mp=lambda x,y: x+y
>>> map(mp, aa, bb)
['1234', 'abcc', 'aa', '12c777', '009']
>>> map(None, aa, bb)
[('12', '34'), ('ab', 'cc'), ('', 'aa'), ('12c', '777'), ('009', '')]
>>>
>>> dec = lambda x,y: x*10+y
>>> reduce(dec, [3,4,7,7])
3477
```

### 迭代对象产生
- iter(o[, sentinel])
返回一个迭代器对象

- next(iterator[, default])
获取迭代对象的下一个，如果有default对象当遍历不到时返回，否则抛出StopIteration异常

- range(stop) range(start, stop[, step])
返回一个数值序列列表
```
>>> range(4)
[0, 1, 2, 3]
>>> range(-4)
[]
>>> range(0,-4)
[]
>>> range(0,-4,-1)
[0, -1, -2, -3]
>>> range(-4,0)
[-4, -3, -2, -1]
>>> range(0,20,4)
[0, 4, 8, 12, 16]
```

- xrange(stop) xrange(start, stop[, step]) 
功能和range类似，但是返回的是一个迭代对象

### 迭代对象的一些常用操作
- len(s) 
返回对象的长度。参数可以是序列(such as a string, bytes, tuple, list, or range)或集合(such as a dictionary, set, or frozen set).

- reversed(seq)
将一个序列反转并返回一个迭代对象

- sorted(iterable[, cmp[, key[, reverse]]]) 
根据迭代对象产生一个新的排序的列表

- max(iterable[, key]) max(arg1, arg2, *args[, key])
返回迭代对象中最大值

- min(iterable[, key]) min(arg1, arg2, *args[, key])
返回迭代对象中最小值，或一组参数中的最小值，key可以用来指定比较方法

- sum(iterable[, start]) 
将一个迭代对象里的内容合计，如果有传入start则从此位置开始。迭代对象的内容必须是数值型

## 对象自省

### 自执行
- callable(object)
判断一个对象参数是否可调用，如果是可调用返回True。注意可调用并不表示一定会调用成功，但不可调用肯定调用失败。
一个类是可调用的，一个类实例如果实现了`__call__()`方法也是可调用的

- compile(source, filename, mode[, flags[, dont_inherit]])
将一段源码转换为代码或ast对象(抽象语法树,参见ast模块)。
参数model：指定编译代码的种类。可以指定为 ‘exec’,’eval’,’single’。另外参见exec,eval
```
>>> code = "for i in range(0, 5): print i"
>>> cmpcode = compile(code, '', 'exec')
>>> exec cmpcode
0
1
2
3
4
```

- eval(expression[, globals[, locals]])
参数是Unicode或者Latin-1编码的字符串，全局变量和局部变量可选。
如果有全局变量，globals必须是个字典。如果有局部变量，locals可以是任何映射类型对象。
```
>>> x = 1
>>> print eval('x+1')
2
```

- execfile(filename[, globals[, locals]])
该函数类似于exec语句，它解析一个文件而不是字符串。

- repr(object)
返回某个对象可打印形式的字符串。repr()和``做的是完全一样的事情，它们返回的是一个对象的“官方”字符串表示，
也就是说绝大多数情况下可以通过求值运算（使用内建函数eval()）重新得到该对象。
注意并不是所有repr()返回的字符串都能够用eval()内建函数得到原来的对象。也就是说 repr() 输出对 Python比较友好，而str()的输出对用户比较友好。
```
>>> dt = datetime.datetime.now()
>>> dt
datetime.datetime(2016, 9, 13, 17, 24, 54, 444747)
>>> repr(dt)
'datetime.datetime(2016, 9, 13, 17, 24, 54, 444747)'
>>> str(dt)
'2016-09-13 17:24:54.444747'
>>> # 用来进行对象的序列化？
>>> strdt = repr(dt)
>>> dt2 = eval(strdt)
>>> print dt2
2016-09-13 17:24:54.444747
>>> type(dt2)
<type 'datetime.datetime'>
>>> 
```

### 对象属性
- setattr(object, name, value) 
给对象设置属性和属性值

- delattr(object, name)
参数为一个对象和字符串。作用是根据名称删除对象的属性。另外参见setattr

- getattr(object, name[, default]) 
根据名称返回对象属性，如果对应名称存在则返回属性值。否则返回defalut，如果都没有则抛出AttributeError

- hasattr(object, name)
判断对象是否有某个属性，实际内部调用了getattr

### 变量相关
- globals()
将当前全局符号表按字典形式返回。是对当前模块的一个字典性的描述
```
>>> globals()
{'val': 'c', 'idx': 6, '__builtins__': <module '__builtin__' (built-in)>, 'db': {'a': 1, 'c': 3, 'b': 2, 'd': 4}, 'da': {'a': 1, 'c': 3, 'b': 2}, '__name__': '__main__', '__package__': None, '__doc__': None}
```
- locals()
更新并返回表示当前局部符号表的字典。当locals在函数块中而不是类块中被调用时，locals()返回自由变量。
```
>>> locals()
{'val': 'c', 'idx': 6, '__builtins__': <module '__builtin__' (built-in)>, 'db': {'a': 1, 'c': 3, 'b': 2, 'd': 4}, 'da': {'a': 1, 'c': 3, 'b': 2}, '__name__': '__main__', '__package__': None, '__doc__': None}
```

- vars([object]) 
如果不带参数，则vars()的行为类似locals()
返回模块、类、实例或其它任何具有__dict__属性的对象的__dict__属性。


### 模块相关
- dir([object])
如果没有参数，返回当前本地作用域内的名字列表。如果有参数，尝试返回参数所指明对象的合法属性的列表。

- help([object])

- reload(module)
重新加载前面加载过的模块，适用于在程序运行过程中修改模块代码再重新导入。

- `__import__(name[, globals[, locals[, fromlist[, level]]]]) `

### 装饰器
- classmethod(function)
将一个方法封装成类方法。另外参见装饰器

- staticmethod(function)
静态方法装饰器，静态方法不接受隐式的第一个参数（也就是实例名称self）。

- class property([fget[, fset[, fdel[, doc]]]])
设置新型类的属性，也可以做为装饰器使用
```
class C(object):
    def __init__(self):
        self._x = None
        self._voltage = 100000

    # 类方法即可以通过类来调用C.getA(2)，也可以通过实例来调用c1.getA(2)
    @classmethod
    def getA(cls, value):
        return value + 1

    # 静态方法即可以通过类来调用C.getB(2)，也可以通过实例来调用c1.getB(2)
    @staticmethod
    def getB(value):
        return value + 2

    # 通过property内置函数提供封装的get/set/del方法
    # c.x will invoke the getter, c.x = value will invoke the setter and del c.x the deleter
    def getx(self):
        return self._x
    def setx(self, value):
        self._x = value
    def delx(self):
        del self._x
    x = property(getx, setx, delx, "I'm the 'x' property.")

    # Property 性质的属性具有getter、setter和deleter 方法
	# 适用场景即可以对入参进行检查，同时又提供了直接属性操作的方便。
    # 将voltage() 方法转换为一个名称相同的只读属性。
    @property
    def voltage(self):
        return self._voltage

    # p.voltage = 1
    @voltage.setter/getter/deleter属性装饰器，提供了更多的方法
    def voltage(self. v)
        self._voltage = v
```

### 类，子类，父类，类型
- object()
返回一个新的无特征的对象。object是所有新式类的基类。它有对所有新式类的实例通用的方法。

- isinstance(object, classinfo)
判断一个对象是否某个类(父类)的实例。classinfo可以是类classobject,类型typeobject,或是递归包含的元组

- issubclass(class, classinfo)
判断一个类是否某个类的子类，一个类被认为是它自己的子类。

- super(type[, object-or-type])
获取这个类的父类

- class type(object) class type(name, bases, dict)
返回一个对象的类型，更推荐使用isinstance

- id(object)
返回一个对象的唯一标识，这个值在对象生命周期中是唯一且不变的。暂时可以理解为对象的地址。
```
# 前面global中的对象
>>> id(val)
139976213650168
>>> id(db)
11704400
```



