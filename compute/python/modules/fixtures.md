# [fixtures](https://pypi.python.org/pypi/fixtures)

## 简介

测试用例一般都包含一个 setUp 方法来准备测试环境，主要是生成一些测试过程中会用到的变量与对象。有时候我们会需要在不同的测试用例间共享这些变量与对象，避免在每一个测试用例中重复定义。所以就有了 fixtures，它制定了一套规范，将测试代码与环境准备代码分离开来，使得测试代码亦可方便的组织和扩展。

依赖testtools和pbr包。任意支持TestCase.addCleanup的框架都可以使用。

## 使用

### 创建fixtrues

最基本的用法是创建一个Fixture子类，实现_setUp方法

```
import unittest
import fixtures

# 设置了一个属性并支持cleanup
class NoddyFixture(fixtures.Fixture):
    def _setUp(self):
        self.frobnozzle = 42
        self.addCleanup(delattr, self, 'frobnozzle')
```

fixture中支持content，这样不必在测试用例的setup中指定detail

```
from testtools.content import text_content
class WithLog(fixtures.Fixture):
     def _setUp(self):
        self.addDetail('message', text_content('foo bar baz'))
```

fixture支持继承关系，可以组合使用多个fixture

```
class ReusingFixture(fixtures.Fixture):
    def _setUp(self):
        self.noddy = self.useFixture(NoddyFixture())
```

通过functionfixture方法直接将对应setup/cleanup绑定到fixture

```
>>> def setup_function():
...     return tempfile.mkdtemp()
>>> def teardown_function(fixture):
...     shutil.rmtree(fixture)
>>> fixture = fixtures.FunctionFixture(setup_function, teardown_function)
# 更简练的写法，直接传递方法
>>> fixture = fixtures.FunctionFixture(tempfile.mkdtemp, shutil.rmtree)
>>> fixture.setUp()
# fn_result表示执行后的返回值
>>> print (os.path.isdir(fixture.fn_result))
True
>>> fixture.cleanUp()
```


### 使用fixture

在unittest或testtools中使用fixture

```
标准库使用fixture的setup和cleanup
class SomeUnitTest(unittest.TestCase):
    def setUp(self):
        super(SomeTest， self).setUp()
        self.fixture = NoddyFixture()
        self.fixture.setUp()
        self.addCleanup(self.fixture.cleanUp)

# testtools简化了fixture的使用
class SomeTesttoolsTest(testtools.TestCase):
    def setUp(self):
        super(SomeTest， self).setUp()
        self.useFixture(NoddyFixture())
```

### 更多固定方法

fixtures库提供了一系列固定方法用来创建特定的场景

|方法|说明|示例|
|------|-------|--------|
|ByteStream|字节流|fixture = fixtures.StringStream('my-content')|
|EnvironmentVariable|环境变量|fixture = fixtures.EnvironmentVariable('HOME')|
|FakeLogger|模拟日志|fixture = fixtures.FakeLogger()|
|FakePopen|模拟打开的文件|fixture = fixtures.FakePopen(lambda _:{'stdout': BytesIO('foobar')})|
|MockPatchObject|mock|fixture = fixtures.MockPatchObject(Fred, 'value', 2)|
|MockPatch||fixture = fixtures.MockPatch('subprocess.Popen.returncode', 3)|
|MockPatchMultiple||fixture = fixtures.StringStream('my-content')|
|MonkeyPatch||fixture = fixtures.StringStream('my-content')|
|NestedTempfile|为tempfile模块创建的的临时目录|fixture = fixtures.NestedTempfile()|
|PackagePathEntry|将路径加入到sys.package.__path__|fixture = fixtures.PackagePathEntry('package/name', '/foo/bar')|
|PythonPackage|创建包路径|fixture = fixtures.PythonPackage('foo.bar', [('quux.py', '')])|
|PythonPathEntry|将路径加入到sys.package|fixture = fixtures.PythonPathEntry('/foo/bar')|
|StringStream|字符串流|fixture = fixtures.StringStream('stdout')|
|TempDir|创建临时目录|fixture = fixtures.TempDir()|
|TempHomeDir|创建临时目录并加入到$HOME环境变量中|fixture = fixtures.TempHomeDir()|
|Timeout|超时控制||
