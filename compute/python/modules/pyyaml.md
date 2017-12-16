# Python YAML

## 官方文档

http://pyyaml.org/wiki/PyYAMLDocumentation

## YAML

YAML（发音 /?j?m?l/ ）是YAML Ain’t Markup Language(YAML非标记语言)的缩写，类似GNU的递归命名，是适用于所有编程语言的数据序列化标准。

所谓非标记语言是区别于XML等标记语言的。YAML提供了一种更简洁的方式来表达数据。可通过下面的例子来展示XML和YAML在表达数据上的区别。

```
# XML
<languages>
<language>Ruby</language>
<language>Perl</language>
<language>Python</language>
</languages>
<websites>
<website language="YAML">yaml.org</website>
<website language="Ruby">ruby-lang.org </website>
<website language="Python">python.org</website>
</websites>
```

```
# YAML
languages:
  - Ruby
  - Perl
  - Python 
websites:
  YAML: yaml.org 
  Ruby: ruby-lang.org 
  Python: python.org 
  Perl: use.perl.org
```
 
### YAML的优点及设计目的

- 简洁，简洁，简洁，不需要额外的标记，更关注数据
- 可读性好
- 和脚本语言的交互性好，易解析
- 使用实现语言的数据类型。
- 有一个一致的信息模型
- 易于实现
- 可以基于流来处理
- 表达能力强，扩展性好。

### YAML使用

#### 语法规则

- 大小写敏感
- 使用缩进来表示层次关系
- 缩进时不允许使用Tab，只允许使用空格
- 缩进的空格数目没有严格限制，相同层级左对齐即可
- 使用#表示注释一行

#### 文档(Documents)

YAML流由0或多个称为文档的结构组成。文档之间通过---分割，文档还可以由...表示结束。

```
# 一个标准的文档，当只有一个时可以忽略开头和结束
---
- Afterstep
- CTWM
- Oroborus
...
```

#### 块序列(Block sequences)

在一块内容中使用"- "来表示数组内容，或直接使用[]
```
# YAML
- The Dagger 'Narthanc'
- The Dagger 'Nimthanc'
- The Dagger 'Dethanc'
# Python
["The Dagger 'Narthanc'", "The Dagger 'Nimthanc'", "The Dagger 'Dethanc'"]

# 多层嵌套的例子
# YAML
- 1.1
- - 2.1
  - 2.2     #可以不必从新行开始 连续两个dash
- - - 3.1   #注意这里和文档---的区别
    - 3.2
    - 3.3
# Python
[1.1, [2.1, 2.2], [[3.1, 3.2, 3.3]]]
```

#### 块映射(Block)

使用": "来表示一个键值对，或直接使用{}

```
# YAML
base armor class: 0
base damage: [4,4]
plus to-hit: 12
plus to-dam: 16
plus to-ac: 0
# Python
{'plus to-hit': 12, 'base damage': [4, 4], 'base armor class': 0, 'plus to-ac': 0, 'plus to-dam': 16}

# YAML
hero:
  hp: 34
  sp: 8
  level: 4
orc:
  hp: 12
  sp: 0
  level: 2
# Python
{'hero': {'hp': 34, 'sp': 8, 'level': 4}, 'orc': {'hp': 12, 'sp': 0, 'level': 2}}
```

数据结构的组合例子
```
# 字典的value是数组
languages:
 - Ruby
 - Perl
 - Python
# Python
{languages:[Ruby, Perl, Python]}
# 字典的value是字典 
websites:
 YAML: yaml.org 
 Ruby: ruby-lang.org 
 Python: python.org 
 Perl: use.perl.org
# Python
{websites: {YAML: yaml.org, Ruby: ruby-lang.org, Python: python.org,Perl: use.perl.org}}
```

#### 流集合(Flow collections)

YAML中流集合的语法近似于Python中的list和dictionary的使用

```
# YAML
{ str: [15, 17], con: [16, 16], dex: [17, 18], wis: [16, 16], int: [10, 13], chr: [5, 8] }
```

#### 标量Scalars

YAML中有5种类型的标量:普通文本（plain）, 单引号标注（single-quoted）, 双引号标注（double-quoted）, 斜体（literal）, 以及闭合标注（folded）:

一个plain标量不使用标识符来描述起始位置，所以是最严格的样式。属性和参数名字是它的典型应用。

single-quoted 的标量, 可以表示不包含特殊字符的任意值。重复的单引号''被代替为一个单引号'，除此之外没有别的特殊替换

Double-quoted 是功能最强的样式，也是唯一能表示所有标量值的样式。

另两种块标量样式：literal 和 folded. literal 最适合大块的文本比如源代码。后者folded是将连续的非空行通过空格字符连接成一整行。
```
# YAML
plain: Scroll of Remove Curse
single-quoted: 'EASY_KNOW'
double-quoted: "?"
literal: |    # Borrowed from http://www.kersbergen.com/flump/religion.html
  by hjw              ___
     __              /.-.\
    /  )_____________\\  Y
   /_ /=== == === === =\ _\_
  ( /)=== == === === == Y   \
   `-------------------(  o  )
                        \___/
folded: >
  It removes all ordinary curses from all equipped items.
  Heavy or permanent curses are unaffected.

# Python
{'plain': 'Scroll of Remove Curse',
'literal':
    'by hjw              ___\n'
    '   __              /.-.\\\n'
    '  /  )_____________\\\\  Y\n'
    ' /_ /=== == === === =\\ _\\_\n'
    '( /)=== == === === == Y   \\\n'
    ' `-------------------(  o  )\n'
    '                      \\___/\n',
'single-quoted': 'EASY_KNOW',
'double-quoted': '?',
'folded': 'It removes all ordinary curses from all equipped items. Heavy or permanent curses are unaffected.\n'}
```

```
# 更多例子
# 字符串，默认不使用引号
str: onestr
str: one''str 单引号需使用两个引号转义

# 字符串可以写成多行，从第二行开始，必须有一个单空格缩进。换行符会被转为空格。
str: onestr
 twostr

# 多行字符串可以使用|保留换行符，也可以使用>折叠换行。
# +表示保留文字块末尾的换行，-表示删除字符串末尾的换行。
str: |
 onestr
 twostr
str1: >
 onestr
 twostr
# 等于
{‘str1’: ‘onestr twostr\n’, ‘str’: ‘onestr \ntwostr\n’} 
```

#### 别名(Aliases)

引用由锚点&和别名*来表示。类似于变量定义，用于减少重复配置。注意PyYAML目前不支持递归对象?

```
defaults: &defaults
  adapter:  postgres
  host:     localhost
development:
  database: myapp_development
  <<: *defaults
test:
  database: myapp_test
  <<: *defaults
# 类似于
development:
  database: myapp_development
  adapter:  postgres
  host:     localhost
```

#### 标签Tags

标签用于表示YAML节点的类型。参考标准的[YAML标签定义](http://yaml.org/type/index.html.)

没有显式标签定义的Plain 标量会得到隐式标签resolve的处理。标量的值被一系列正则表达式检测。如果发现匹配，则相应的标签被赋予该标量。PyYAML允许应用添加自定义的标签resolvers。

```
# 数值
number: 12
number: 12.1数字将分别会做整形或浮点型处理。

# 布尔型，用true和false
isTrue: false

# None
用~表示

# 日期
time: 2017-05-25将被解析为{'time': datetime.date(2017, 5, 25)}

# 类型强制转换
number: !!str 12中12将被解析为字符串，同{'number': '12'}
number: !!int '12'中’12’将被解析为int，{'number': 12}
number: !!float "3.14"                 {'number': 3.14}
```
#### YAML 标签 和 Python 类型

| YAML tag | Python type |
|--------|--------|
|标准YAML标签|
|!!null  |   None |
|!!bool  |   bool |
|!!int   |  int or long (int in Python 3)|
|!!float |  float |
|!!binary|  str(bytes in Python 3)|
|!!timestamp|  datetime.datetime|
|!!omap, !!pairs| list of pairs|
|!!set   |  set   |
|!!str   |  str or unicode (str in Python 3)|
|!!seq   |  list  |
|!!map   |  dict|
|Python-specific tags|
|!!python/none|  |
|!!python/bool|  |
|!!python/bytes|(bytes in Python 3)|
|!!python/str|	str (str in Python 3)|
|!!python/unicode|	unicode (str in Python 3)|
|!!python/int|	int|
|!!python/long|	long (int in Python 3)|
|!!python/float| float|
|!!python/complex|	complex|
|!!python/list| list|
|!!python/tuple|tuple|
|!!python/dict| dict|
|Complex Python tags|
|!!python/name:module.name|module.name|
|!!python/module:package.module|package.module|
|!!python/object:module.cls|module.cls instance|
|!!python/object/new:module.cls|module.cls instance|
|!!python/object/apply:module.f|value of f(...)|

## PyYAML

PyYAML是用于加载和持久化YAML文件的第三方python库。

### 基本使用

PyYAML主要提供两个接口load和dump，其中load用于从文件流中或字符串中加载YAML为Python对象，dump则是反向将python对象写入文件

#### load

通过load方法可以将字符串或字节流转换为python对象

```
>>> yaml.load("""
... - Hesperiidae
... - Papilionidae
... - Apatelodidae
... - Epiplemidae
... """)

['Hesperiidae', 'Papilionidae', 'Apatelodidae', 'Epiplemidae']
```

注意：直接通过load转换非可靠的内容是不安全的。应该使用safe_load方法替代。

可以通过load_all一次加载多个文档对象
```
>>> documents = """
... ---
... name: The Set of Gauntlets 'Pauraegen'
... description: >
...     A set of handgear with sparks that crackle
...     across its knuckleguards.
... ---
... name: The Set of Gauntlets 'Paurnen'
... description: >
...   A set of gauntlets that gives off a foul,
...   acrid odour yet remains untarnished.
... ---
... name: The Set of Gauntlets 'Paurnimmen'
... description: >
...   A set of handgear, freezing with unnatural cold.
... """

>>> for data in yaml.load_all(documents):
...     print data

{'description': 'A set of handgear with sparks that crackle across its knuckleguards.\n',
'name': "The Set of Gauntlets 'Pauraegen'"}
{'description': 'A set of gauntlets that gives off a foul, acrid odour yet remains untarnished.\n',
'name': "The Set of Gauntlets 'Paurnen'"}
{'description': 'A set of handgear, freezing with unnatural cold.\n',
'name': "The Set of Gauntlets 'Paurnimmen'"}
```

#### dump

dump函数接收python对象，并产生一个YAML文档
```
>>> print yaml.dump({'name': 'Silenthand Olleander', 'race': 'Human',
... 'traits': ['ONE_HAND', 'ONE_EYE']})

name: Silenthand Olleander
race: Human
traits: [ONE_HAND, ONE_EYE]
```

yaml.dump函数第二个参数支持文本或二进制文件，可以将内容输出到文件中


### 高级主题

#### Python2与Python3

#### Python对象转换

#### 自定义Tag

#### 性能

使用LibYAML(C库)绑定, 要比纯的python库速度快。需要下载并安装 LibYAML. 之后通过下列命令安装：

$ python setup.py --with-libyaml install 

为了使用 LibYAML 的 parser and emitter, 需要使用classes CParser and CEmitter. 例如,

```
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# ...

data = load(stream, Loader=Loader)

# ...

output = dump(data, Dumper=Dumper)
```
