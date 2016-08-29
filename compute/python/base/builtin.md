# Built-in Functions内置方法

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

- bin(x)
将整型数值转换为二进制字符串，如果一个对象不是整型但通过实现__index__()方法返回整型，则使用此方法的返回值转换。
```
>>> bin(123)
'0b1111011'
>>> bin(-123)
'-0b1111011'
>>> bin(9123)
'0b10001110100011'
```

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

- class bytearray([source[, encoding[, errors]]]) 
返回一个新的字节数组

- callable(object) 
判断一个对象参数是否可调用，如果是可调用返回True。注意可调用并不代码一定会调用成功，但不可调用肯定调用失败。
一个类是可调用的，一个类实例如果实现了__call__()方法也是可调用的

- chr(i)
返回只有一个字符(ASCII表中的字符)的字符串。参数必须在0-255之间，否则抛出ValueError。另外参见ord(),unichr()
```
>>> chr(97)
'a'
>>> chr(2)
'\x02'
```

- classmethod(function) 
将一个方法封装成类方法。另外参见装饰器,staticmethod()

- cmp(x, y)
比较两个对象并根据结果返回一个整型，如果x<y返回负数，相等返回0，x>y返回正数
```
>>> cmp(11,2)
1
>>> cmp(11,11)
0
```

- compile(source, filename, mode[, flags[, dont_inherit]])
将一段源码转换为代码或ast对象(抽象语法树,参见ast模块)。另外参见exec,eval

- class complex([real[, imag]])
创建一个复数对象

- delattr(object, name)
参数为一个对象和字符串。作用是根据名称删除对象的属性。另外参见setattr

- class dict(**kwarg) class dict(mapping, **kwarg) class dict(iterable, **kwarg)
构造一个字典对象
```
>>> da = dict(a=1,b=2,c=3)
>>> db = dict(da, d=4)
>>> print db
{'a': 1, 'c': 3, 'b': 2, 'd': 4}
```

- dir([object])

- divmod(a, b)
对整型变量来说相当于返回(a // b, a % b). 

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

- eval(expression[, globals[, locals]])

- execfile(filename[, globals[, locals]])

- file(name[, mode[, buffering]]) 
file类型的构造方法，和open类似。但推荐使用open，而file用来对对象类型进行判断

- filter(function, iterable) 
过滤器,参见map,reduce方法

- class float([x]) 
从数值或字符串返回浮点数

- format(value[, format_spec]) 
将值进行格式化

- class frozenset([iterable]) 

- getattr(object, name[, default]) 
根据名称返回对象属性，如果对应名称存在则返回属性值。否则返回defalut，如果都没有则抛出AttributeError

- globals() 
将当前全局符号表按字典形式返回。是对当前模块的一个字典性的描述
```
>>> globals()
{'val': 'c', 'idx': 6, '__builtins__': <module '__builtin__' (built-in)>, 'db': {'a': 1, 'c': 3, 'b': 2, 'd': 4}, 'da': {'a': 1, 'c': 3, 'b': 2}, '__name__': '__main__', '__package__': None, '__doc__': None}
```

- hasattr(object, name)
判断对象是否有某个属性，实际内部调用了getattr

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

- help([object]) 

- hex(x) 
将一个整型数值转换为小写的十六进制字符串显示。另外参见int(),float.hex()
```
>>> hex(255)
'0xff'
>>> hex(15)
'0xf'
```

- id(object) 
返回一个对象的唯一标识，这个值在对象生命周期中是唯一且不变的。暂时可以理解为对象的地址。
```
# 前面global中的对象
>>> id(val)
139976213650168
>>> id(db)
11704400
```

- input([prompt]) 
等同于eval(raw_input(prompt)).建议使用raw_input

- class int(x=0) class int(x, base=10)
从一个数值或字符转换为整型值。可以指定进制
```
>>> int(11)
11
>>> int('123')
123
>>> int('10f', 16)
271
>>> int('101100', 2)
44
```

- isinstance(object, classinfo) 
判断一个对象是否某个类(父类)的实例。classinfo可以是类classobject,类型typeobject,或是递归包含的元组

- issubclass(class, classinfo) 
判断一个类是否某个类的子类

- iter(o[, sentinel]) 
返回一个迭代器对象

- len(s) 
返回对象的长度。参数可以是序列(such as a string, bytes, tuple, list, or range)或集合(such as a dictionary, set, or frozen set).

- class list([iterable]) 
将一个可迭代对象转换为列表

locals() 
将当前本地符号表以字典形式返回
```
>>> locals() 
{'val': 'c', 'idx': 6, '__builtins__': <module '__builtin__' (built-in)>, 'db': {'a': 1, 'c': 3, 'b': 2, 'd': 4}, 'da': {'a': 1, 'c': 3, 'b': 2}, '__name__': '__main__', '__package__': None, '__doc__': None}
>>> 
```

- class long(x=0) class long(x, base=10)
构建一个长整型对象

- map(function, iterable, ...) 
映射方法，另外参见filter,reduce方法

- max(iterable[, key]) max(arg1, arg2, *args[, key])

- memoryview(obj)

- min(iterable[, key]) min(arg1, arg2, *args[, key])
返回迭代对象中最小值，或一组参数中的最小值，key可以用来指定比较方法

- next(iterator[, default])
获取迭代对象的下一个，如果有default对象当遍历不到时返回，否则抛出StopIteration异常

- oct(x)
将整型数值转换为8进制显示的字符串

- open(name[, mode[, buffering]])
打开文件并返回一个文件类型的对象

- ord(c) 
将只有一个字符串转换为数值，另外参见chr,unichr

- pow(x, y[, z]) 
进行指数运算，如果只有xy，则等同于x**y。如果有z则相当于(x**y)%z

- print(*objects, sep=' ', end='\n', file=sys.stdout) 
将对象输出到文件流中

- class property([fget[, fset[, fdel[, doc]]]])
设置新型类的属性，也可以做为装饰器使用
```
class C(object):
    def __init__(self):
        self._x = None
    def getx(self):
        return self._x
    def setx(self, value):
        self._x = value
    def delx(self):
        del self._x
    x = property(getx, setx, delx, "I'm the 'x' property.")

#c.x will invoke the getter, c.x = value will invoke the setter and del c.x the deleter
```

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

- raw_input([prompt]) 
根据提示进行输入，将输入值保存在字符串对象中

- reduce(function, iterable[, initializer]) 
对迭代对象按递减方式套用方法，另外参见filter,map

- reload(module) 
重新加载前面加载过的模块，适用于在程序运行过程中修改模块代码再重新导入。

- repr(object) 


- reversed(seq)
将一个序列反转并返回一个迭代对象

- round(number[, ndigits]) 
对小数部分进行四舍五入操作，返回一个浮点数

- class set([iterable]) 
根据迭代对象生成一个集合，另外参见frozenset

- setattr(object, name, value) 
给对象设置属性和属性值

- class slice(stop) class slice(start, stop[, step]) 


- sorted(iterable[, cmp[, key[, reverse]]]) 
根据迭代对象产生一个新的排序的列表

- staticmethod(function) 
静态方法装饰器

- class str(object='') 
将一个对象转换为str类型，注意与repr(obj)的区别

- sum(iterable[, start]) 
将一个迭代对象里的内容合计，如果有传入start则从此位置开始。迭代对象的内容必须是数值型

- super(type[, object-or-type]) 

- tuple([iterable]) 
将迭代对象转换为元组并保持原来的顺序

- class type(object) class type(name, bases, dict)
返回一个对象的类型，更推荐使用isinstance

-unichr(i) 
将一个整型值转换为unicode字符串

- unicode(object='') unicode(object[, encoding[, errors]]) 
返回一个unicode字符串

- vars([object]) 

- xrange(stop) xrange(start, stop[, step]) 
功能和range类似，但是返回的是一个迭代对象

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

- __import__(name[, globals[, locals[, fromlist[, level]]]]) 

