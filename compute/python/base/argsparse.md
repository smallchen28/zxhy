# argparse -命令行选项，参数和子命令的解析器

用来创建用户友好的命令行交互界面，用来定义命令行需要的参数并对参数进行解析，同时也支持自动生成帮助和其他有用信息。

## ArgumentParser 命令解析器对象

### 定义
```
class argparse.ArgumentParser(prog=None,
                              usage=None,
                              description=None,
                              epilog=None,
                              parents=[],
                              formatter_class=argparse.HelpFormatter,
                              prefix_chars='-',
                              fromfile_prefix_chars=None,
                              argument_default=None,
                              conflict_handler='error',
                              add_help=True)
```
							  
| 参数 |说明|
|--------|--------|
|prog | 在帮助信息中显示的程序的名称，默认是sys.argv[0]。一般不需要传递。|
|usage | 命令使用帮助，默认自动生成，一般不需要输入 |
|description | 参数帮助信息之前的文本，一般需要输入。显示在usage和实际帮助信息之间 |
|epilog | 参数帮助信息之后的文本，例如在help最后增加一个邮件或网站地址信息 |
|parents | 父对象列表，支持命令的结构化扩展，一般不需要。|
|formatter_class | 用来定制帮助输出的类，一般不需要 |
|prefix_chars | 选项前缀的字符串集合，默认为'-'，一般不需要。当需要多种前缀时，例如通过-f/+f表示某种相反选项时，则传入'+-' |
|fromfile_prefix_chars | 额外的参数应读取的文件的前缀字符集 |
|argument_default | 参数的全局默认值，一般不需要 |
|conflict_handler | 选项冲突解决策略，默认是error，另一个值是'resolve'。通常在父子结构扩展中，当用子命令参数覆盖父命令参数时解决冲突 |
|add_help | 是否增加帮助选项，默认是。在结构扩展中有用，屏蔽父类的帮助 |

### 使用

- prog
```
# 代码部分
[root@spark216 ~]# cat ptest.py 
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--foo', help='foo help')
args = parser.parse_args()

# 不传递参数，一般使用模块文件名
[root@spark216 ~]# python ptest.py --help
usage: ptest.py [-h] [--foo FOO]

optional arguments:
  -h, --help  show this help message and exit
  --foo FOO   foo help
  
# 传递参数的构造
parser = argparse.ArgumentParser(prog='ptester')
[root@spark216 ~]# python ptest.py --help
usage: ptester [-h] [--foo FOO]    
```

- usage
```
parser = argparse.ArgumentParser(prog='ptester',usage='how it works')
# 参数内容显示在usage后面
[root@spark216 ~]# python ptest.py --help
usage: how it works

optional arguments:
  -h, --help  show this help message and exit
  --foo FOO   foo help
```

- description
```
# 增加了前段说明
parser = argparse.ArgumentParser(description='ptester command is something')

[root@spark216 ~]# python ptest.py --help
usage: ptest.py [-h] [--foo FOO]

ptester command is something

optional arguments:
  -h, --help  show this help message and exit
  --foo FOO   foo help
```

- epilog
```
# 增加了后段说明
parser = argparse.ArgumentParser(epilog="report bug to liu1xin@outlook.com")

[root@spark216 ~]# python ptest.py --help
usage: ptest.py [-h] [--foo FOO]

optional arguments:
  -h, --help  show this help message and exit
  --foo FOO   foo help

report bug to liu1xin@outlook.com
```

- formatter_class

*当前(2.7)中有三种帮助格式化类*

RawDescriptionHelpFormatter 对desc和epilog中的内容保留原始格式，换行和缩进

RawTextHelpFormatter 将保留所有帮助文本的空白，包括参数的描述。

ArgumentDefaultsHelpFormatter 会在帮助中显示参数的默认值

- prefix_chars
```
parser = argparse.ArgumentParser(prefix_chars='-+')
parser.add_argument('+g', help='add g')

[root@spark216 ~]# python ptest.py --help
usage: ptest.py [-h] [--foo FOO] [+g G]

optional arguments:
  -h, --help  show this help message and exit
  --foo FOO   foo help
  +g G        add g
```

## add_argument() 方法

### 定义

这个方法定义了一个参数应该被怎样解析
```
ArgumentParser.add_argument(name or flags...[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest])
```

| 参数 |说明|
|--------|--------|
|name or flags |参数名称，可以有一个或多个表达形式，如-f,--foo(可选参数),foo(位置参数)|
|action | 解析某个参数时将对应的一个动作，默认的动作就是将值保存。| 
|nargs | 应该读取的命令行参数数目。类似正则表达式的将多个参数匹配一个action |
|const | 常量值，和前面的action配合使用 |
|default | 默认值 |
|type | 类型检查和类型转换。支持内建类型和方法，还支持用户自定义 |
|choices | 对参数值的范围进行限制，注意是类型转换后的 |
|required | 表示参数为必须输入的，一般用来限制可选参数必须输入 |
|help | 对参数的帮助描述。如果是help=argparse.SUPPRESS则不在帮助信息中显示此选项|
|metavar | 用来在帮助中显示的参数名称，默认是和dest一致 |
|dest | 参数对应保存的属性名称 |



### 使用

- name and flags参数名
```
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('-f', '--foo') # 可选参数
>>> parser.add_argument('bar') # 位置参数
>>> parser.parse_args(['BAR'])
Namespace(bar='BAR', foo=None)
>>> parser.parse_args(['BAR', '--foo', 'FOO'])
Namespace(bar='BAR', foo='FOO')
>>> parser.parse_args(['--foo', 'FOO'])
usage: PROG [-h] [-f FOO] bar
PROG: error: too few arguments
```
这里说明一下可选参数和位置参数

可选参数表示参数是可选的，不是必须输入的

位置参照表示参数是必须输入的，并且和顺序有关

- action动作
```
# 可用的action如下
# store:将值保存，这是默认动作
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo')
>>> parser.parse_args('--foo 1'.split())
Namespace(foo='1'
>>>
# store_const:将某个常量值保存到参数中，配合const
>>> parser.add_argument('--foo', action='store_const', const=42)
>>> parser.parse_args('--foo'.split())
Namespace(foo=42)
>>>
# store_true/store_false：将true/false保存到参数中。是store_const的一种特例
>>> parser.add_argument('--foo', action='store_true')
>>> parser.add_argument('--bar', action='store_false')
>>> parser.add_argument('--baz', action='store_false')
>>> parser.parse_args('--foo --bar'.split())
Namespace(bar=False, baz=True, foo=True)
>>>
# append:将值保存到列表参数中
>>> parser.add_argument('--foo', action='append')
>>> parser.parse_args('--foo 1 --foo 2'.split())
Namespace(foo=['1', '2'])
>>>
# append_const:将常量值保存到列表中，通常将相关的一组固定选择保存到list中
>>> parser.add_argument('--str', dest='types', action='append_const', const=str)
>>> parser.add_argument('--int', dest='types', action='append_const', const=int)
>>> parser.parse_args('--str --int'.split())
Namespace(types=[<type 'str'>, <type 'int'>])
>>>
# count：参数出现次数的计数，通常用来对-v,-vv,-vvv这样的参数进行匹配
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--verbose', '-v', action='count')
>>> parser.parse_args('-vvv'.split())
Namespace(verbose=3)
>>>
# help：显示帮助信息
# version：显示版本信息
>>> import argparse
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('--version', action='version', version='%(prog)s 2.0')
>>> parser.parse_args(['--version'])
PROG 2.0
# 还能够自定义action子类，一般可以扩展argparse.Action，覆盖`__call__`方法
```

- nargs参数与动作的匹配次数
```
# nargs=N。命令行中的N个参数将被一起收集在一个列表中。
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', nargs=2)
>>> parser.add_argument('bar', nargs=1)
>>> parser.parse_args('c --foo a b'.split())
Namespace(bar=['c'], foo=['a', 'b'])
>>>
# nargs='?'。如果有的话就从命令行读取一个参数并生成一个元素。如果没有对应的命令行参数，则产生一个来自default的值。
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', nargs='?', const='c', default='d')
>>> parser.add_argument('bar', nargs='?', default='d')
>>> parser.parse_args('XX --foo YY'.split())
Namespace(bar='XX', foo='YY')
>>> parser.parse_args('XX --foo'.split())
Namespace(bar='XX', foo='c')
>>> parser.parse_args(''.split())
Namespace(bar='d', foo='d')
>>>
# nargs='*'。出现的所有命令行参数都被收集到一个列表中。
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', nargs='*')
>>> parser.add_argument('--bar', nargs='*')
>>> parser.add_argument('baz', nargs='*')
>>> parser.parse_args('a b --foo x y --bar 1 2'.split())
Namespace(bar=['1', '2'], baz=['a', 'b'], foo=['x', 'y'])
>>>
# nargs='+'。和'*'一样，出现的所有命令行参数都被收集到一个列表中。
# 除此之外，如果没有至少出现一个命令行参数将会产生一个错误信息。
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('foo', nargs='+')
>>> parser.parse_args('a b'.split())
Namespace(foo=['a', 'b'])
>>> parser.parse_args(''.split())
usage: PROG [-h] foo [foo ...]
PROG: error: too few arguments
>>>
# nargs=argparse.REMAINDER.所有剩余的命令行参数都被收集到一个列表中。
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('--foo')
>>> parser.add_argument('command')
>>> parser.add_argument('args', nargs=argparse.REMAINDER)
>>> print parser.parse_args('--foo B cmd --arg1 XX ZZ'.split())
Namespace(args=['--arg1', 'XX', 'ZZ'], command='cmd', foo='B')
```

- default默认值
```
# 设置默认值，在用户没有传递命令行参数时使用该默认值
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', default=42)
>>> parser.parse_args('--foo 2'.split())
Namespace(foo='2')
>>> parser.parse_args(''.split())
Namespace(foo=42)
>>>
# 如果default的值是一个字符串，解析器将像命令行参数一样解析这个值。
>>> parser.add_argument('--length', default='10', type=int)
>>> parser.add_argument('--width', default=10.5, type=int)
>>> parser.parse_args()
Namespace(length=10, width=10.5)
# default=argparse.SUPPRESS将导致如果没有命令行参数时不会添加属性：
>>> parser.add_argument('--foo', default=argparse.SUPPRESS)
>>> parser.parse_args([])
Namespace()
>>> parser.parse_args(['--foo', '1'])
Namespace(foo='1')
```

- type类型
```
# 默认以字符串处理，可以通过type转换为特定类型
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('foo', type=int)
>>> parser.add_argument('bar', type=file)
>>> parser.parse_args('2 temp.txt'.split())
Namespace(bar=<open file 'temp.txt', mode 'r' at 0x...>, foo=2)
# 对文件类型，提供了更丰富的方法type=argparse.FileType('w')
# type参数或者是任何可调用的方法，只要该方法接受字符串参数并返回转换后的某个类型对象
```

- choices选择
```
# choices可以用来控制传入参数是否在适当范围内，类型转换后再判断
>>> parser = argparse.ArgumentParser(prog='doors.py')
>>> parser.add_argument('door', type=int, choices=range(1, 4))
>>> print(parser.parse_args(['3']))
Namespace(door=3)
>>> parser.parse_args(['4'])
usage: doors.py [-h] {1,2,3}
doors.py: error: argument door: invalid choice: 4 (choose from 1, 2, 3)
# 支持in操作符的任何对象都可以传递给choices作为它的值，所以dict对象、set对象以及自定义的容器等等都支持。
```

- required
```
# 期望可选参数是必须输入时使用
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', required=True)
>>> parser.parse_args(['--foo', 'BAR'])
Namespace(foo='BAR')
>>> parser.parse_args([])
usage: argparse.py [-h] [--foo FOO]
argparse.py: error: option --foo is required
```

- help
```
# 用来显示参数的帮助信息
>>> argp = argparse.ArgumentParser()
>>> argp.add_argument('--foo', help='help info add foo')
>>> argp.parse_args('-h'.split())
usage: [-h] [--foo FOO]

optional arguments:
  -h, --help  show this help message and exit
  --foo FOO   help info add foo
>>>
# help字符串可以包含各种格式指示符以避免如程序名字和参数default的重复。
# 可用的指示符包括程序的名称%(prog)s以及大部分add_argument()的关键字参数，例如%(default)s、%(type)s等：
>>> parser.add_argument('bar', nargs='?', type=int, default=42,
...         help='the bar to %(prog)s (default: %(default)s)')
```

- dest
```
# 对于位置参数的动作，dest 通常使用第一个参数
# 对可选参数是将第一个长的选项字符串前面的--字符串去掉
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('-f', '--foo-bar', '--foo')
>>> parser.add_argument('-x', '-y')
>>> parser.parse_args('-f 1 -x 2'.split())
Namespace(foo_bar='1', x='2')
>>> parser.parse_args('--foo 1 -y 2'.split())
Namespace(foo_bar='1', x='2')
>>>
# 可以使用自定义的dest名称
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', dest='bar')
>>> parser.parse_args('--foo XXX'.split())
Namespace(bar='XXX')
```

- 一个更全面的例子，综合了name,type,choices,nargs,help,desc,const,default,metavar
```
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument(
...     'integers', metavar='int', type=int, choices=xrange(10),
...  nargs='+', help='an integer in the range 0..9')
>>> parser.add_argument(
...     '--sum', dest='accumulate', action='store_const', const=sum,
...   default=max, help='sum the integers (default: find the max)')
>>> parser.parse_args(['1', '2', '3', '4'])
Namespace(accumulate=<built-in function max>, integers=[1, 2, 3, 4])
>>> parser.parse_args('1 2 3 4 --sum'.split())
Namespace(accumulate=<built-in function sum>, integers=[1, 2, 3, 4])
```

## parse_args()方法

### 定义
将参数字符串转换成对象并设置成命名空间的属性。返回构成的命名空间。
```
ArgumentParser.parse_args(args=None, namespace=None)
```

### 示例

- args
```
# 选项有多种写法:
# 最常见写法，参数名和参数值空格分隔
>>> parser.parse_args('-x X'.split())
Namespace(foo=None, x='X')
>>> parser.parse_args('--foo FOO'.split())
Namespace(foo='FOO', x=None)
>>>
# 长选项
>>> parser.parse_args('--foo=FOO'.split())
Namespace(foo='FOO', x=None)
>>>
# 短选项
>>> parser.parse_args('-xX'.split())
Namespace(foo=None, x='X')
>>> parser.add_argument('-x', action='store_true')
>>> parser.add_argument('-y', action='store_true')
>>> parser.add_argument('-z')
>>> parser.parse_args('-xyzZ'.split())
Namespace(x=True, y=True, z='Z')
```

- namespace
用于创建一个保存属性的对象并返回该对象。
```
# 将这个对象转换出字典
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo')
>>> args = parser.parse_args(['--foo', 'BAR'])
>>> vars(args)
{'foo': 'BAR'}
>>>
# 分配属性到一个已经存在的对象而不是一个新的Namespace对象。
>>> class C(object):
...     pass
...
>>> c = C()
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo')
>>> parser.parse_args(args=['--foo', 'BAR'], namespace=c)
>>> c.foo
'BAR'
```

## 其他特性

### add_subparsers子命令

### FileType文件类型对象

`class argparse.FileType(mode='r', bufsize=None)`

FileType创建可以传递给ArgumentParser.add_argument()的type参数的对象。
以FileType对象为类型的参数将用要求的模式和缓冲区大小来打开命令行参数作为文件：
```
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--output', type=argparse.FileType('wb', 0))
>>> parser.parse_args(['--output', 'out'])
Namespace(output=<open file 'out', mode 'wb' at 0x...>)
```

### add_argument_group 参数分组

`ArgumentParser.add_argument_group(title=None, description=None)`

不分组时参数是区分为可选和位置参数两部分。但一组相关的参数可以划分到一个组中。未加入组的仍按原来的形式显示
```
>>> parser = argparse.ArgumentParser(prog='PROG', add_help=False)
>>> group1 = parser.add_argument_group('group1', 'group1 description')
>>> group1.add_argument('foo', help='foo help')
>>> group2 = parser.add_argument_group('group2', 'group2 description')
>>> group2.add_argument('--bar', help='bar help')
>>> parser.print_help()
usage: PROG [--bar BAR] foo

group1:
  group1 description

  foo    foo help

group2:
  group2 description

  --bar BAR  bar help
```

### add_mutually_exclusive_group排它参数组

`ArgumentParser.add_mutually_exclusive_group(required=False)`

表示这一组中的参数是互斥的不能同时使用，如果使用了required表示至少需要传递一个参数
```
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> group = parser.add_mutually_exclusive_group()
>>> group.add_argument('--foo', action='store_true')
>>> group.add_argument('--bar', action='store_false')
>>> parser.parse_args(['--foo'])
Namespace(bar=True, foo=True)
>>> parser.parse_args(['--bar'])
Namespace(bar=False, foo=False)
>>> parser.parse_args(['--foo', '--bar'])
usage: PROG [-h] [--foo | --bar]
PROG: error: argument --bar: not allowed with argument --foo
```

### 解析器默认值

`ArgumentParser.set_defaults(**kwargs)`

大部分时候，parse_args()返回的对象的属性完全由命令行参数和参数的动作决定。set_defaults()允许添加一些额外的属性而不用命令行的解析决定：
```
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('foo', type=int)
>>> parser.set_defaults(bar=42, baz='badger')
>>> parser.parse_args(['736'])
Namespace(bar=42, baz='badger', foo=736)
```

### 打印帮助

在交互式环境下有些方法方便直接将帮助信息输出，例如ArgumentParser.print_help(),print_usage()

### parse_known_args部分解析

`ArgumentParser.parse_known_args(args=None, namespace=None)`

用来解析当前匹配的参数，并将剩余的参数再返回。正常情况下参数和解析完全匹配会异常，部分解析可以规避。

```
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', action='store_true')
>>> parser.add_argument('bar')
>>> parser.parse_args(['--foo', '12', 'test', '--ppt', '11'])
usage: [-h] [--foo] bar
: error: unrecognized arguments: test --ppt 11
>>> parser.parse_known_args(['--foo', '12', 'test', '--ppt', '11'])
(Namespace(bar='12', foo=True), ['test', '--ppt', '11'])
```

### 退出和异常信息

`ArgumentParser.exit(status=0, message=None)`

该方法将终止程序，以指定的status退出，如果给出message，则会在此之前打印出它。

`ArgumentParser.error(message)`

该方法打印一个用法信息包括message参数到标准错误输出并以状态码2终止程序。
