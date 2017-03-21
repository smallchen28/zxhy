# [testtools](http://testtools.readthedocs.io/en/latest/)

## 简介

testtools是个unittest的扩展框架，主要是在unittest的基础上提供了更好的assert功能，使得写单元测试更加方便。

### 为什么要使用testtools

- 更好的断言方法，标准库中的断言并不足够并且友好。这里提供了更多更好的实现

- 通过Matchers提供比断言更优雅的方法，可以针对特定业务实现特定的比较规则

- 更多的调试信息，方便代码的修改和跟踪

- 兼容性的扩展了unitest

- 跨版本的支持

## 使用

### 基本用例

一个基本的测试用例和标准库的testcase很像，只是基类不同。

```
from testtools import TestCase
from myproject import silly

class TestSillySquare(TestCase):
    """Tests for silly square function."""

    def test_square(self):
        # 'square' takes a number and multiplies it by itself.
        result = silly.square(7)
        self.assertEqual(result, 49)

    def test_square_bad_input(self):
        # 'square' raises a TypeError if it's given bad input, say a
        # string.
        self.assertRaises(TypeError, silly.square, "orange")
```

运行方法也和标准库类似

```
$ python -m testtools.run exampletest
Tests running...
Ran 2 tests in 0.000s

OK

# 不会包含遍历，需要加discover库才支持?
$ python -m testtools.run discover packagecontainingtests

# 执行帮助
python -m testtools.run --help
```

通过distutils管理运行

```
# 通过distutils管理包时构建扩展的setup.py。
$ python setup.py test -m exampletest
Tests running...
Ran 2 tests in 0.000s

OK
```

### 断言

自动化测试的核心是对事物的方式进行断言，当事情不是所期望的时候可以得到一个好的、有用的、有信息性的错误信息。

testtools提供的断言涵盖了所有unittest的断言，并进行了的改进/扩展和补充。

- assertRaises

捕获异常并对异常中信息判断

```
def test_square_bad_input(self):
    # 'square' raises a TypeError if it's given bad input, say a string, should be int
    e = self.assertRaises(TypeError, silly.square, "orange")
    self.assertEqual("orange", e.bad_value)
    self.assertEqual("Cannot square 'orange', not a number.", str(e))
```

- ExpectedException

支持上下文管理器的一种写法，比上面的更精炼。

```
def test_square_root_bad_input_2(self):
    # 'square' raises a TypeError if it's given bad input.
    with ExpectedException(TypeError, "Cannot square.*"):
        silly.square('orange')
```

- expectFailure

将某种特例的失败作为正常

```
def test_expect_failure_example(self):
    self.expectFailure(
        "cats should be dogs", self.assertEqual, 'cats', 'dogs')
```

- assertIn, assertNotIn

判断一个对象是否在序列中

```
def test_assert_in_example(self):
    self.assertIn('a', 'cat')
    self.assertNotIn('o', 'cat')
    self.assertIn(5, list_of_primes_under_ten)
    self.assertNotIn(12, list_of_primes_under_ten)
```
	
- assertIs, assertIsNot
	
判断是否同一个对象

```
def test_assert_is_example(self):
    foo = [None]
    foo_alias = foo
    bar = [None]
    self.assertIs(foo, foo_alias)
    self.assertIsNot(foo, bar)
    self.assertEqual(foo, bar) # They are equal, but not identical
```

- assertIsInstance

判断是否某类型的实例，注意没有assertIsNotInstance

```
def test_assert_is_instance_example(self):
    now = datetime.now()
    self.assertIsInstance(now, datetime)
```

### Matchers匹配器

内置的断言非常有用，但总有满足不了特殊场景的时候。当此时matchers提供了有力的表达工具

#### assertThat

示例：

```
import testtools
from testtools.matchers import Equals

class TestSquare(TestCase):
    def test_square(self):
       result = square(7)
	   # 和普通的语法表达更贴近
       self.assertThat(result, Equals(49))
```

assertthat一旦失败会中断执行，因此另外提供了一个expectThat，单个断言失败不会导致立刻返回失败。

#### 内建的matchers

|方法|说明|示例|
|------|-------|--------|
|数值或对象匹配|||
|Equals|两个实例是否相等|self.assertThat([42], Equals([42]))|
|NotEquals|不等于|注意差异Not(Equals(x)). NotEquals(x)|
|KeysEqual|字典关键字相同||
|Is|两个实例是否相同|self.assertThat(foo, Is(foo))|
|IsInstance|是否是某个实例|self.assertThat(MyClass(), IsInstance(MyClass))|
|DocTestMatches|||
|GreaterThan|大于|self.assertThat(3, GreaterThan(2))|
|LessThan|小于|self.assertThat(2, LessThan(3))|
|StartsWith|以字符串开始|self.assertThat('underground', StartsWith('und'))|
|EndsWith|以字符串结束|self.assertThat('underground', EndsWith('und'))|
|Contains|包含|self.assertThat('abc', Contains('b'))|
|HasLength|序列或集合长度|self.assertThat([1, 2, 3], HasLength(3))|
|MatchesRegex|字符串与正则表达式|self.assertThat('foo', MatchesRegex('fo+'))|
|文件匹配|||
|PathExists|路径是否存在|self.assertThat('/', PathExists())|
|DirExists|目录是否存在|self.assertThat('/home/jml/some-file.txt', DirExists())|
|FileExists|文件是否存在|self.assertThat('/bin/true', FileExists())|
|DirContains|目录包含的文件|self.assertThat('foo', DirContains(['a', 'b', 'c']))|
|FileContains|文件包含的内容|self.assertThat('greetings.txt', FileContains("Hello World!"))|
|HasPermissions|文件权限|self.assertThat('/tmp', HasPermissions('1777'))|
|SamePath|是否同一目录|self.assertThat('somefile', SamePath('childdir/../somefile'))|
|TarballContains|打包文件包含||
|组合匹配|||
|Always|总是匹配|self.assertThat(x, Always())|
|Never|永不匹配|self.assertThat(x, Never())|
|Not|非|self.assertThat([42], Not(Equals("potato")))|
|Annotate|||
|MatchesAll|多条件匹配|self.assertThat("underground", MatchesAll(StartsWith("und"), EndsWith("und")))|
|MatchesAny|任意调节匹配|self.assertThat(42, MatchesAny(Equals(5), Not(Equals(6))))|
|AllMatch|所有项都匹配|self.assertThat([2, 3, 5, 7], AllMatch(LessThan(10)))|
|MatchesListwise|||
|MatchesSetwise|||
|MatchesStructure|结构中特定属性匹配||
|MatchesPredicate|||
|MatchesPredicateWithParams||
|异常处理相关|||
|MatchesException|异常类型|更多使用raises|
|raises|是否抛出异常|self.assertThat(lambda: 1/0, raises(ZeroDivisionError))|
|Raises|抛出异常匹配|self.assertThat(lambda: 1/0, Raises(MatchesException(ZeroDivisionError)))|
|IsDeprecated|不建议的|是对下面两个方法的组合|
|Warnings|||
|WarningMessage|||


#### 自定义matchers


### Details细节输出

前面提到过自动化测试是为了更快，更方便的定位和解决问题。仅仅提供函数名和断言信息等是不够的，必要时还需要记录测试用例执行时的详细信息，例如日志记录，部分模块状态，当时的动作等等。

unittest通过基于MIME的内容对象保存细节信息，因此允许你将运行测试过程中任意内容输出。基本的content对象testtools.content.Content由ContentType和实际可迭代的字节块构成。

一个示例，在测例失败时将服务端的日志信息也同步记录下来
```
from testtools import TestCase
from testtools.content import attach_file, Content
from testtools.content_type import UTF8_TEXT

from myproject import SomeServer

class SomeTestCase(TestCase):

    def setUp(self):
        super(SomeTestCase, self).setUp()
        self.server = SomeServer()
        self.server.start_up()
        self.addCleanup(self.server.shut_down)
        self.addCleanup(attach_file, self.server.logfile, self)

    def attach_log_file(self):
        self.addDetail(
            'log-file',
            Content(UTF8_TEXT,
                    lambda: open(self.server.logfile, 'r').readlines()))

    def test_a_thing(self):
        self.assertEqual("cool", self.server.temperature)
```

### 控制测试的执行

addCleanup，提供了一种统一清除fixtures的办法

fixtures，如果一个场景是否复杂的，建议实现为fixtures.Fixture对象。

skippingtests，通过方法TestCase.skipTest可以暂不运行本测例并返回必要的信息。

addOnException

### 一些便利方法

TestCase.patch替换某些对象

```
将标准输出替换为某个IO
def test_foo(self):
    my_stream = StringIO()
    self.patch(sys, 'stderr', my_stream)
    run_some_code_that_prints_to_stderr()
    self.assertEqual('', my_stream.getvalue())
```

Creation methods，提供了通用办法产生一些字符串或整数，这样不用写死。

testtools.TestCase.getUniqueString/getUniqueInteger

Test attributes

Conditional imports条件导入

```
# testtools提供了方便的按条件导入方法
try:
    from twisted.internet import defer
except ImportError:
    defer = None
# 可以写成	
defer = try_import('twisted.internet.defer')	

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
	
# 可以写成
StringIO = try_imports(['StringIO.StringIO', 'io.StringIO'])	
```

Nullary callables

## 扩展testtools框架

