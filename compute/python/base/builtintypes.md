# Built-in Types

1.最主要的内置类型包括数值型numerics，序列sequences，映射mappings，文件files，类classes，实例instances，异常exceptions

2.特点：所有标准对象可以用于布尔测试、同类型之间可以比较大小和转换为string（使用内建函数repr(obj)或str(obj)）。

## 1.真值测试

任何对象都可以测试真值，用于if或while的条件或下面布尔运算的操作数。下面的值被视为假：
    None
    False
    任何数值类型的零，例如，0,0L,0.0,0j
    任何空的序列，例如， '',(),[]
    任何空的映射，例如，{}
    用户定义的类的实例，如果该类定义一个`__nonzero__()`或`__len__()`的方法，在该方法返回整数零或布尔值False时。
    所有其他值都被视为真 — 所以许多类型的对象永远为真。

## 2.布尔运算 and,or,not

|操作|说明|备注|
|--------|--------|--------|
|x or y| 如果x是False返回y，否则返回x | 只有当x为False时y才会被执行|
|x and y| 如果x是False返回x，否则返回y | 只有当x为True时y才会被执行|
|not x | 如果x是False则返回True，否则返回False | not操作符的优先级比较低|

```
# 特别注意如下一段代码，布尔操作符or和and返回的是一个操作数，不是true或false
>>> x=3
>>> y=[]
>>> b = x or y
>>> print b
3
>>> b = x and y
>>> print b
[] 
```

## 3.比较运算

所有对象都支持比较运算。它们都具有相同的优先级（高于布尔运算）。
比较可以任意链接；例如，x < y < = z相当于x < y and y < = z，只是y只计算一次（但这两种情况在x < y为假时都不会计算z）。

|操作|说明|备注|
|--------|--------|--------|
| < | 严格地小于 |不支持复数 |
| <=| 小于或等于 | |
| > | 严格地大于 | |
| >=| 大于或等于 | |
| ==| 等于 | |
| !=| 不等于 | 另一种写法<>不建议使用|
| is | 是某个对象(id) | |
| is not | 不是某个对象 | |
| in | 在序列中 | 支持seq，map两种类型|
| not in| 不在序列中 | |

更多说明：

类的非同一个实例比较时通常不相等，除非该类定义`__eq__()或__cmp__()`方法。

一个类的实例通常不能与同一个类的其它实例或者其他类型的对象排序，除非该类定义足够丰富的比较方法`__ge__()、__le__()、__gt__()、__lt__()`或`__cmp__()`方法。

CPython 的实现细节：除数值以外不同类型的对象按它们的类型名称进行排序；不支持合适比较的相同类型的对象按它们的地址进行排序

## 4.数值类型

有四种不同的数值类型：int普通整数、long长整数、float浮点数和complex复数。此外，布尔值是普通整数的一个子类型。

int使用C中的long实现，其精度至少为32位（当前平台最大的普通整数值是sys.maxint，最小值是-sys.maxint)。

long具有无限的精度。

float通常使用C中的double实现；有关你的程序所运行的机器上的浮点数精度及其内部表示形式的信息在sys.float_info中可以获得。

复数有实部和虚部，各是一个浮点数。若要从复数z中提取这些部分，请使用z.real和z.imag。

### 4.1.数值运算

内置数值类型支持如下操作

|操作或方法|说明|备注|
|--------|--------|--------|
| x + y   |加法运算||
| x - y   |减法运算||
| x * y   |乘法运算||
| x / y   |除法运算|对于（普通或长）整数除法，结果是一个整数。结果总是向负无穷舍入：1/2是0，(-1)/2是-1，1/(-2)是-1，（-1)/(-2)是0|
| x // y  |x与y的（整除）商||
| x % y  |模值运算||
| -x       |负x||
| +x     |x保持不变||
| abs(x) |x的绝对值或大小|参见内建方法|
| int(x)  |x转换成整数|使用int()或long()函数转换浮点数会向零截断，类似相关的函数math.trunc()函数。|
| long(x) |x转换成长整数||
| float(x)  |x转换成浮点数|浮点数还接受可带有可选前缀 "+"或"-"的字符串"nan"和"inf"来表示非数字（NaN)）和正/负无穷|
| complex(re,im)  |实部为re，虚部为im的一个复数。im默认为零。||
| c.conjugate()  |复数c的共轭。（用实数表示）||
| divmod(x, y)  |元组(x // y, x % y)||
| pow(x, y)  |x的y次方|pow(0,0)和0 ** 0为1|
| x**y | x的y次方||

### 4.2.整数类型的位操作

按位运算只有对整数才有意义。

二元位运算的优先级都低于数值操作，但高于比较操作；一元操作~具有和其它的一元数值操作（+和-）相同的优先级。

下表按优先级升序排列列出位运算

|操作|说明|备注|
|--------|--------|--------|
|`x | y` |x和y的按位或||
| x ^ y |x和y的按位异或||
| x & y |x和y的按位与||
| x << n |x左移n位|n不能为负数|
| x >> n |x右移n位||
| ~x |反转x的各个位||

### 4.3.数值类型上的一些方法

数值类型更多是numbers模块中抽象类实现，参考number模块

- int.bit_length()long.bit_length()返回以二进制表示一个整数必须的位数，不包括符号和前导零：
```
>>> n = -37
>>> bin(n)
'-0b100101'
>>> n.bit_length()
6
```

- float.as_integer_ratio()返回一对整数，它们的比例准确地等于浮点数的原始值，且分母为正数
```
>>> a=3.33333
>>> a.as_integer_ratio()
(938248984118931, 281474976710656)
>>> 938248984118931/281474976710656.0
3.33333
```

- float.is_integer()判断浮点数是否一个整数？

- float.hex()浮点数转换为十六进制字符串。这个是实例方法

- float.fromhex(s)十六进制字符串转换为浮点数。这个是类方法

## 5.迭代器类型

迭代容器对象**iterable**支持迭代：

 `container.__iter__()`返回迭代器对象。该对象必须支持如下所述的迭代器协议。

迭代对象**iterator**本身需要支持以下两种方法，它们组合在一起形成迭代器协议：

 `iterator.__iter__()`返回迭代器对象本身
 
 `iterator.next()`从容器中返回下一个元素。如果没有元素，引发StopIteration异常。

### 生成器类型

Python的生成器提供一种方便的方法来实现迭代器协议。
如果容器对象的`__iter__()`方法实现为一个生成器，它将自动返回一个提供`__iter__()`和`next()`方法的迭代器对象（从技术上讲，是生成器对象）。生成器的更多信息可以在yield表达式的文档中找到。

## 6.序列类型

有七个序列类型： 字符串str、 Unicode字符串unicode、 列表list、 元组tuple、 字节数组bytearray、 缓冲区buffer和xrange对象xrange。
其中list和bytearray是可变序列类型，表明序列里的值可以被修改。其他都是不可变序列类型

序列类型有多种创建方式，最常用的是通过内置方法。

### 6.1.通用序列类型操作

|操作|说明|备注|
|--------|--------|--------|
| x in s | s序列中某个元素等于x则返回True | 字符串时支持x是任意长度的字符串|
| x not in s| s序列中不存在等于x的元素 | |
| s + t | 两个序列的连接操作 | 连接的实现和优化取决于所用版本，因此要注意|
| s * n, n * s| 序列 | n如果是0返回同类型的空序列，注意此处是浅拷贝|
| s[i]| 获取s序列中第i个元素 | 序列是从0开始的|
| s[i:j]| 分片操作 | |
| s[i:j:k] | 以步长k进行分片操作 | |
| len(s) | 返回序列长度 | 内置函数 |
| min(s) | 返回序列中最小元素 | 内置函数 |
| max(s)| 返回序列中最大元素 | 内置函数 |
|s.index(x)| 返回s序列中第一个等于x元素的元素下标||
|s.count(x)| 返回s序列中等于x元素的元素个数||

### 6.2.字符串方法

字符串类型作为序列除了上面的通用方法，还支持自身的一系列特定方法。

|方法|说明|
|--------|--------|
|str.capitalize()|返回字符串的副本，该副本第一个字符大写，其余字符小写。|
|str.center(width[, fillchar])|返回长度为width的字符串，并使得自身居中。使用指定的fillchar（默认为一个空格）做填充。|
|str.count(sub[, start[, end]])|返回在[start, end]范围内的子串sub非重叠出现的次数。|
|str.decode([encoding[, errors]])|使用 encoding 中注册的编解码器，对字符串进行解码。|
|str.encode([encoding[, errors]])|返回该字符串编码后的版本。|
|str.endswith(suffix[, start[, end]])|如果字符串以指定的suffix结尾则返回True，否则返回False。suffix也可以是一个元组。|
|str.expandtabs([tabsize])||
|str.find(sub[, start[, end]])|返回在字符串中找到的子字符串sub的最低索引|
|str.format(*args, **kwargs)|执行字符串格式化操作。|
|str.index(sub[, start[, end]])|类似find()，但未找到子字符串时引发ValueError |
|str.isalnum()|如果字符串中的所有字符都是数字或者字母，并且至少有一个字符，则返回true，否则返回false。|
|str.isalpha()|字符串至少有一个字符并且都是字母，则返回true，否则返回false。|
|str.isdigit()|如果在字符串中的所有字符都是数字并且至少一个字符，则返回 true。否则返回false。|
|str.islower()|如果在字符串中的所有字符都小写并且至少一个字符，则返回true|
|str.isspace()|如果有只有空白字符在字符串中返回true|
|str.istitle()|如果字符串是标题类型的字符串且至少包含一个字符，则返回 true|
|str.isupper()|字符串中都大写且至少包含一个字符，则返回 true|
|str.join(iterable)|返回一个字符串，为iterable可迭代对象中字符串的连接。|
|str.ljust(width[, fillchar])|返回字符串的长度宽度中左对齐一个字符串。做了填充使用指定的fillchar （默认为一个空格）。|
|str.lower()|返回转换为小写字符串|
|str.lstrip([chars])|返回删除前导字符的字符串的副本。Chars参数是一个字符串，指定要移除的字符集。|
|str.partition(sep)||
|str.replace(old, new[, count])|返回字符串的一个拷贝，其中所有的子串old通过new替换。如果指定了count，则只有前面的count个出现被替换。|
|str.rfind(sub[, start[, end]])|返回被搜索子串最后一次出现在字符串的索引位置,|
|str.rindex(sub[, start[, end]])|类似rfind() ，但未找到子字符串子时引发ValueError|
|str.rjust(width[, fillchar])|返回字符串的长度宽度中右对齐的字符串。|
|str.rpartition(sep)|参考partition|
|str.rsplit([sep[, maxsplit]])|参考split|
|str.rstrip([chars])|参考lstrip|
|str.split([sep[, maxsplit]])|返回字符串中的单词列表，使用sep作为分隔符字符串。如果给出maxsplit，则至多拆分maxsplit次|
|str.splitlines([keepends])|返回字符串中行组成的列表，在行的边界截断。|
|str.startswith(prefix[, start[, end]])|参考endswith|
|str.strip([chars])|参考lstrip，同时删除两边|
|str.swapcase()|返回字符串的一个拷贝，其中大写字符转换为小写，小写字符转换为大写。|
|str.title()|返回字符串首字母大写的一个版本，所有单词以大写字母开始，剩下的字母都是小写。|
|str.translate(table[, deletechars])|出现在参数deletechars中的所有字符被删除，其余的字符通过给定的转换表映射，转换表必须是长度为256的一个字符串。|
|str.upper()|返回字符串的一个拷贝，所有字符转换为大写|
|str.zfill(width)|在数值字符串的左边填充零至长度为width。符号前缀将正确处理。|
|unicode.isnumeric()|如果S中只有数值字符则返回True，否则返回False。|
|unicode.isdecimal()|如果S中只有十进制字符，则返回True，否则返回False。|

```
>>> 'abcd'.capitalize()
'Abcd'
>>> 'abcD'.capitalize()
'Abcd'
>>> 
>>> 'abcdefg'.center(3)
'abcdefg'
>>> 'abcdefg'.center(12)
'  abcdefg   '
>>> 'abcdefg'.center(12,'-')
'--abcdefg---'
>>> 
>>> 'abcdefg'.endswith('fg')
True
>>> 'abcdefg'.endswith('cfg')
False
>>> filename.endswith(('gz','bz'))
True
>>>
>>> 'www.aaa.com'.lstrip('a.w')
'com'
>>> 
# translate更详细用法参考string
>>> 'abcdefgfedcba'.translate(None,'eg')
'abcdffdcba'
>>> 
>>> '-737733'.zfill(10)
'-000737733'
>>> 'b37733'.zfill(10)
'0000b37733'
```

### 6.3.字符串的格式化

参考string模块

### 6.4.xrange类型
xrange类型是不可变的序列，通常用于循环。xrange类型的好处是xrange对象始终占用相同数量的内存，无论它表示的范围的大小。但它没有始终一致的性能优势。xRange对象的行为很少：它们仅支持索引、迭代和len()函数。不支持切片、 连接或重复，在它们上使用in，not in、 min()或max()效率较低。
```
>>> aa = xrange(5)
>>> 
>>> 3 in aa
True
>>> len(aa)
10
>>> for a in aa:
...     print a
... 
0
1
2
3
4
>>> aa[3]
3
```

### 6.5.可变序列类型

列表和bytearray对象支持允许就地修改该对象的额外操作。其它可变的序列类型（在添加到该语言中时）也应支持这些操作。
字符串和元组是不可变的序列类型：这类对象一旦创建不能修改。

可变序列类型支持的操作如下：

|操作|说明|备注|
|--------|--------|--------|
|s[i] = x|替换i位置元素为x||
|s[i:j] = t|分片选择i到j，根据迭代器的内容替换这部分||
|del s[i:j]|删除分片中内容||
|s[i:j:k] = t|分片选择，根据迭代器的内容替换这部分|t的长度需要等于切片长度|
|del s[i:j:k]|删除分片中内容||
|s.append(x)|在最后增加一个元素x||
|s.extend(x)|在最后将迭代器内容追加||
|s.count(x)|返回x元素的个数||
|s.index(x[, i[, j]])|返回第一个等于x的位置||
|s.insert(i, x)|在i位置插入元素x|支持i为负值，i会加上列表的长度。如果仍为负值，则将其截取为零|
|s.pop([i])|删除第i过元素并返回该元素|i默认参数是-1，表示是最后一个元素||
|s.remove(x)|删除第一个x元素||
|s.reverse()|将序列反序|为了节省空间sort()和reverse()方法将原地修改该列表。|
|s.sort([cmp[, key[, reverse]]])|将序列重新排序|反序和排序时如果记录被修改会异常|

## 7.集合类型:set,frozenset

集合对象是一个不同且可哈希对象组成的无序集合。常见的使用包括成员测试、从序列中删除重复项和计算数学运算（如交、并、差和对称差）。
作为一个无序的集合，集合不记录元素位置和插入顺序。因此，集合不支持索引、 切片、 或其它类似于序列的行为。

目前有两个内置的集合类型，set和frozenset。
set类型是可变的 可以使用add()和remove()方法来更改内容。因为它是可变的，所以它没有哈希值且不能用作字典的键或另一个集合的元素。
frozenset类型是不可变且可哈希的 — 它创建后不能更改其内容；因此可以用作字典的键或另一个集合元素。

可以通过set/forzenset内置函数构建，还可以通过放置一个逗号分隔的的元素序列于花括号内来创建非空集合（frozensets不可以），例如：{'jack', 'sjoerd'}。

### 7.1.集合类型常用方法



## 8.映射类型:dict

一个映射对象将可映射的的值映射到任意对象。映射是可变对象。目前只有一种标准映射类型，dict。

用于键的数值类型遵守数值比较的正常规则：如果两个数字的比较结果相等（如1和1.0），那么它们可以用于互相索引相同的词典条目。但实际不推荐浮点数作为键值

### 8.1.字典类型常用方法

|操作或方法|说明|备注|
|--------|--------|--------|
|len(d)|返回字典d中元素的个数。||
|d[key]|返回字典d中键为key的元素。如果key不在映射中，则引发一个KeyError。|建议用get方法|
|d[key] = value|设置d[key]的值为value。||
|del d[key]|从d中删除d[key] 。如果key不在映射中，则抛出KeyError。||
|key in d|如果d有一个键key，则返回True，否则返回False||
|key not in d|||
|iter(d)|返回字典的键上的一个迭代器。||
|clear()|从字典中移除所有项。||
|copy()|返回字典的一个浅拷贝。||
|fromkeys(seq[, value])|与键从seq和值将设置为值创建一个新的字典。||
|get(key[, default])|如果key在字典中，则返回key对应的值，否则返回default。|如果没有预置default的值，则它默认为None，所以此方法永远不会引发KeyError|
|has_key(key)|测试key是否在字典中存在。||
|items()|返回该dictionary的(key, value)对的列表。||
|iteritems()|返回字典的(key, value)对上的一个迭代器。||
|iterkeys()|返回字典的键上的一个迭代器。||
|itervalues()|返回字典的(key, value)对上的一个迭代器。|同iter|
|keys()|返回的字典的键列表的副本。|||
|pop(key[, default])|如果key在字典中，删除它并返回其值，否则返回default。||
|popitem()|从字典中移除并返回任意一个(key, value)对|如果字典为空，调用popitem()将引发一个KeyError|
|setdefault(key[, default])|如果key在字典中，返回其值。如果不在，则插入值为default的key并返回default。||
|update([other])|依据other更新词典的键/值对，覆盖现有的键。返回None。||
|values()|返回字典的值的列表的副本。||
|viewitems()|返回字典项(key, value)对的一个新视图。|参见下面的字典视图对象|
|viewkeys()|返回字典的键的新的视图。||
|viewvalues()|返回字典的值的新的视图。||

### 8.2.字典视图对象

由dict.viewkeys()、dict.viewvalues()和dict.viewitems()返回的对象是视图对象。
它们提供字典条目上的一个动态视图，这意味着当字典更改时，视图会反映出这些变化。

|操作或方法|说明|备注|
|--------|--------|--------|
|len(d)|返回字典中的条目数||
|iter(dictview)|返回字典中键、值或项（表示为(key, value)元组）上的一个迭代器。||
|x in dictview|如果x在底层字典的键、值或项中返回True||
|dictview & other|返回dictview和其它对象的交集作为一个新的集合||
|dictview | other|返回dictview和其它对象的并集作为一个新的集合||
|dictview - other|返回dictview和其它对象的差集作为一个新的集合|所有在dictview中但不在other中的元素|
|dictview ^ other|返回dictview和另一个对象的对称差|在dictview或other中，但不是在两个中都存在的所有元素|

## 9.文件类型:file

|方法或属性|说明|备注|
|--------|--------|--------|
|file.close()| 关闭该文件。关闭的文件无法再读取或写入。 | 使用with语句，可以避免显式调用此方法|
|file.flush()| 刷新内部缓冲区 | 不一定写入文件的数据到磁盘。在flush()后紧接着使用os.fsync()来确保这种行为。 |
|file.fileno()| 返回"文件描述符"整数 | |
|file.isatty()| 返回True如果文件连接到一个（类）tty的设备，否则返回False。 | |
|file.next()| 文件对象是其自身的迭代器，例如iter(f)返回f （除非f被关闭）。 | |
|file.read([size])| 最多从文件读取size字节 （如果在读到字节之前就遇到了EOF，则就比size字节少）。如果size参数为负或被省略，读取所有数据，直到达到了 EOF。 | |
|file.readline([size])| 从文件中读取一整行。结尾的换行符包含在字符串中 （当文件为非一整行结束时就可能不在）。 | |
|file.readlines([sizehint])| 使用readline ()读取直到EOF，并返回一个包含所读取行的列表。| |
|file.seek(offset[, whence])| 设置文件的当前位置。| whence可用参数os.SEEK_SET/CUR/END|
|file.tell()| 返回文件的当前位置 | |
|file.truncate([size])| 截断文件的大小。如果存在可选大小参数，则该文件将被截断到 （最多） 那种尺寸。 | |
|file.write(str)| 向文件中写入字符串。 | |
|file.writelines(sequence)| 向文件中写入一个字符串序列。 | 不会自动添加换行 |
|file.closed| 返回布尔类型指示的文件对象的当前状态。 | |
|file.encoding| 此文件使用的编码。 | |
|file.mode| 该文件 I/O 模式。 | |
|file.name| 文件名称 | |
|file.newlines| | |

## 10.内存视图类型:memoryview

memoryview对象允许Python代码访问对象的内部数据而不用复制，只要该对象支持缓冲区协议。内存通常被视为简单的字节。
支持缓冲区协议的内置对象包括str和bytearray（但没有unicode）。memoryview具有元素的概念，它是由原始对象obj处理的原子内存单元。对于许多的简单类型，例如str和bytearray，元素是一个单字节，但是其他第三方的类型可能会使用较大的元素。

|方法或属性|说明|备注|
|--------|--------|--------|
|class memoryview(obj)| 创建一个对象的memoryview| |
|tobytes()| 以一个字节字符串返回缓冲区的数据| |
|tolist()| 以一个整数列表返回该缓冲区中的数据。| |
|format| | |
|itemsize| 每个元素以字节为单位的大小。 | |
|shape| | |
|ndim| 一个整数，指示该内存表示的多维数组有多少维度。| |
|strides| | |
|readonly| 一个布尔值，指示内存是否只读。| |

## 11.Context Manager Types

上下文管理器是可以在with语句中使用，拥有`__enter__`和`__exit__`方法的对象。

参考高级特性文档

## 12.其它的内建类型

