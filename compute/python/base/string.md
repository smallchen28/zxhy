# string模块

## 基本概念
string模块包含大量的常量和类，提供了对字符串操作的一些功能。

## 字符串常量

|常量|说明|
|--------|--------|
|string.ascii_letters| 大写加小写 |
|string.ascii_lowercase | 小写字母'abcdefghijklmnopqrstuvwxyz' |
|string.ascii_uppercase| 大写的字母'ABCDEFGHIJKLMNOPQRSTUVWXYZ' |
|string.digits| 字符串'0123456789' |
|string.hexdigits| 字符串'0123456789abcdefABCDEF' |
|string.letters| lowercase+uppercase |
|string.lowercase| 一个字符串，包含所有被认为是小写字母的字符。 |
|string.octdigits| 字符串'01234567' |
|string.punctuation| 在C语言中的标点字符的 ASCII 字符的字符串 |
|string.printable|可打印的字符的字符串。|
|string.uppercase|一个字符串，包含所有被认为是大写字母的字符。|
|string.whitespace|包含的所有字符都被视为空格的字符串。|

## 字符串函数

模块提供的方法和str对象，unicode对象本身支持的方法大多类似。
对象方法参照builtintypes文档

## 字符串格式化

字符串和Unicode对象有一个独特的内置操作：%（取模）操作符。这也被称为字符串格式化或插值操作符。
给出format % values（其中format是字符串或Unicode对象），转换规范format中的%转换说明被替换为values的零个或多个元素。

如果format需要一个单一的参数，values可以是一个单个的非元组对象。否则，values必须是一个元组且其元素个数与格式字符串指定的完全相同，或者是一个单一的映射对象（例如，一个字典）。

转换说明符包含两个或多个字符并具有以下组件，必须按以下顺序发生：

- '%'字符，它标记指示符的起点。
- 映射的键（可选），由圆括号括起来的字符序列组成（例如，(somename)）。
- 转换的标志（可选），它们影响某些转换类型的结果。
- 字段最小的宽度（可选）。如果用'*'（星号）表示，则真正的宽度从元组values中下一个元素读取，字段最小宽度值后面的是将要转换的对象和可选的精度。
- 精度（可选），用'.'（点号）后面跟上精度给出。如果用'*'（星号）表示，真正的宽度从元组values中的下一个元素读取，精度后面的是将要转换的值。
- 长度调整器（可选）。
- 转换的类型。

当右侧参数是一个字典（或其它映射类型）时，那么字符串中的formats必须包含一个圆括号括起来的键，其来自于%字符后立即插入的那个字典，见示例如下。
```
>>> print '%(language)s has %(number)03d quote types.' % \
...       {"language": "Python", "number": 2}
Python has 002 quote types.
```

### 类型转换
|转换|含义|备注|
|--------|--------|--------|
|d| 有符号的十进制整数 ||
|i| 有符号的十进制整数 ||
|o| 有符号的八进制值 ||
|u| 废弃的类型 – 与'd'完全一致 ||
|x| 有符号的十六进制数（小写） ||
|X| 有符号的十六进制（大写） ||
|e| 浮点数的指数形式（小写） ||
|E| 浮点数的指数形式（大写） ||
|f| 浮点数的十进制形式 ||
|F| 浮点数的十进制形式 ||
|g| 浮点数形式 ||
|G| 浮点数形式 ||
|c| 单个字符 ||
|r| 字符串（使用repr()转换任何Python对象） ||
|s| 字符串（使用str()转换任意Python对象） ||
|%| 不转换任何参数，结果中出现的是'%'字符。 ||

## 格式字符串语法

内置的 str 和 unicode 类通过在 PEP 3101 中描述的 str.format()方法提供了复杂的变量替换和格式化值的能力。

格式字符串为花括号{}包围的替换字段。所有括号外的内容均被视作文本，不做改变复制到输出。 如果需要在文本中包括花括号字符，它可以通过双花括号字符来进行转义： {{和}}

替换字段的语法如下所示：
```
replacement_field ::=  "{" [field_name] ["!" conversion] [":" format_spec] "}" 替换内容包含在括号中，可以指定字段名，转换领域，转换格式3部分
field_name        ::=  arg_name ("." attribute_name | "[" element_index "]")*  fieldname由参数名，后面可追加属性或序列下标组成
arg_name          ::=  [identifier | integer]                                  argname由标示符或整形序号表示
attribute_name    ::=  identifier                                              attrname由标示符表示
element_index     ::=  integer | index_string                                   
index_string      ::=  <any source character except "]"> +
conversion        ::=  "r" | "s"                                               转换格式由r或s表示
format_spec       ::=  <described in the next section>                         转换格式定义语法，见稍后描述 
```

一些示例
```
"First, thou shalt count to {0}" 指定了fieldname为0
"Bring me a {}"                  未指定任何，默认为0
"From {} to {}"                  未指定任何，则先后使用0,1
"My quest is {name}"             指定了对象名name
"Weight in tons {0.weight}"      使用0对象的weight属性
"Units destroyed: {players[0]}"  使用players对象的第0个item
```

一般情况下值进行格式化是由值本身的__format__()方法完成的。转换方式支持r(repr)和s(str)两种方式。

### 格式说明符

Format_spec字段包含格式如何表现的说明，包括这些细节作为字段宽度、对齐、 填充、 小数精度等方面的规范。
```
format_spec ::=  [[fill]align][sign][#][0][width][,][.precision][type]
fill        ::=  <any character>
align       ::=  "<" | ">" | "=" | "^"
sign        ::=  "+" | "-" | " "
width       ::=  integer
precision   ::=  integer
type        ::=  "b" | "c" | "d" | "e" | "E" | "f" | "F" | "g" | "G" | "n" | "o" | "s" | "x" | "X" | "%"
```

### 示例

访问参数按位置
```
>>> '{0}, {1}, {2}'.format('a', 'b', 'c')
'a, b, c'
>>> '{}, {}, {}'.format('a', 'b', 'c')  # 2.7+ only
'a, b, c'
>>> '{2}, {1}, {0}'.format('a', 'b', 'c')
'c, b, a'
>>> '{2}, {1}, {0}'.format(*'abc')      # unpacking argument sequence
'c, b, a'
>>> '{0}{1}{0}'.format('abra', 'cad')   # arguments' indices can be repeated
'abracadabra'
```

按名称访问参数
```
>>> 'Coordinates: {latitude}, {longitude}'.format(latitude='37.24N', longitude='-115.81W')
'Coordinates: 37.24N, -115.81W'
>>> coord = {'latitude': '37.24N', 'longitude': '-115.81W'}
>>> 'Coordinates: {latitude}, {longitude}'.format(**coord)
'Coordinates: 37.24N, -115.81W'
```

访问对象的参数或序列
```
>>> class Point(object):
...     def __init__(self, x, y):
...         self.x, self.y = x, y
...     def __str__(self):
...         return 'Point({self.x}, {self.y})'.format(self=self)
...
>>> str(Point(4, 2))
'Point(4, 2)'
>>> coord = (3, 5)
>>> 'X: {0[0]};  Y: {0[1]}'.format(coord)
'X: 3;  Y: 5'
```

r和s
```
>>> "repr() shows quotes: {!r}; str() doesn't: {!s}".format('test1', 'test2')
"repr() shows quotes: 'test1'; str() doesn't: test2"
```

## Formatter类

string模块中的Formatter类允许您创建和自定义自己的字符串格式类以替换内置format()方法。

|类方法|说明|
|--------|--------|
|format(format_string, *args, **kwargs)||
|vformat(format_string, args, kwargs)||
|parse(format_string)||
|get_field(field_name, args, kwargs)||
|get_value(key, args, kwargs)||
|check_unused_args(used_args, args, kwargs)||
|format_field(value, format_spec)||
|convert_field(value, conversion)||

## Template类

string模块中还提供了更简单的字符串替换方法，称为模板类。模板通过$进行替换

模板类中的两个替换方法
substitute(mapping[, **kws])
safe_substitute(mapping[, **kws])

示例
```
>>> from string import Template
>>> s = Template('$who likes $what')
>>> s.substitute(who='tim', what='kung pao')
'tim likes kung pao'
>>> d = dict(who='tim')
>>> Template('Give $who $100').substitute(d)
Traceback (most recent call last):
...
ValueError: Invalid placeholder in string: line 1, col 11
>>> Template('$who likes $what').substitute(d)
Traceback (most recent call last):
...
KeyError: 'what'
>>> Template('$who likes $what').safe_substitute(d)
'tim likes $what'
```



