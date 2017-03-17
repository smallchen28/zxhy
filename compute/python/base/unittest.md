# unittest

## 基本概念

### 重要概念

- testcase：测试用例或测试单元，是一个最小的独立运行的测试流程。实现了对某个过程/方法/对象的测试。

- testsuite：多个测试用例集合在一起，构成了一个测试集。测试集可以和其他测试用例/集构成一个更大的测试集。

- testloader：构建一个testsuite的过程，一般是将case加入到suite中返回一个suite实例

- testrunner：测试执行器，用来组织执行suite或case并向用户返回结果。

- testfixture：执行某个测试时对测试用例环境的搭建和销毁，是一个fixture。

### 执行步骤

首先是要写好TestCase，然后由TestLoader加载TestCase到TestSuite，然后由TextTestRunner来运行TestSuite，运行的结果保存在TextTestResult中，整个过程集成在unittest.main模块中。

```
suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
unittest.TextTestRunner(verbosity=2).run(suite)
```

从上面的代码步骤中可以看出实际的执行机制。根据此机制，可以定制化实现更精细的控制。

### 测试代码发现机制

为了匹配自动发现机制，所有测试代码文件必须是可以从项目根目录(topleveldirectory)导入的包或模块。默认的发现由TestLoader.discover()实现。

指定发现目录和发现规则的参数参见下面简单帮助中的discover部分选项。

startdirectory默认是命令执行的当前目录
topleveldirectory默认是startdirectory

使用包名(例如myproject.subpackage.test)做为参数传入时，将导入此包，并以包所在目录作为启动目录(startdirectory)导入所有其下的测试模块。

测试模块或包可以通过load_tests protocol指定测试发现和加载机制。

## 编写用例

### 简单示例

一个测试用例文件大概的布局如下

```
# 导入被测模块和单元测试模块
Import  xxxx
Import  unittest

# 以test开头，继承TestCase对象。通常对应测试一个模块或对象
class test_xxx(unittest.TestCase):

    # 执行初始化
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # 以test开头，加上一定的命名规则说明被测试的方法或对象
    def test_function1(self):
        self.assertXXX()	

    # 注意每个测例都会单独执行一遍up/down
    def test_function2(self):
        self.assertXXX()

if __name__ == '__main__':
    unittest.main()		
```

### 组织代码


### 可选择的执行条件

执行测试时并不是都需要执行或者安装某个条件执行

```
class MyTestCase(unittest.TestCase):

    # 通过skip装饰器忽略执行
    @unittest.skip("demonstrating skipping")
    def test_nothing(self):
        self.fail("shouldn't happen")

    # 按条件的忽略
    @unittest.skipIf(mylib.__version__ < (1, 3),
                     "not supported in this library version")
    def test_format(self):
        # Tests that work for only a certain version of the library.
        pass

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_windows_support(self):
        # windows specific testing code
        pass

    # 需要返回失败
    @unittest.expectedFailure
    def test_fail(self):
        self.assertEqual(1, 0, "broken")		
```

### 模块和类级别的fixtures

模块和类级别的fixtures是在TestSuite中实现的，当suite组织所有case时，如果加载到一个新类则执行类上的setUpClass()/tearDownClass()。同样的是加载到一个新模块时则执行setUpModule/tearDownModule。

#### setUpClass and tearDownClass

类级别的是以类方法实现

```
import unittest

class Test(unittest.TestCase):
    # 如果up抛出异常，则本类的测试用例都不会执行。如果抛出的是SkipTest则最终包括可以显示被忽略
    @classmethod
    def setUpClass(cls):
        cls._connection = createExpensiveConnectionObject()

    @classmethod
    def tearDownClass(cls):
        cls._connection.destroy()
```

#### setUpModule and tearDownModule

模块级别的是以模块方法实现

```
# 如果up抛出异常，则本模块的测试用例都不会执行。如果抛出的是SkipTest则最终包括可以显示被忽略
def setUpModule():
    createConnection()

def tearDownModule():
    closeConnection()
```

## 执行测试

### 执行单元测试的命令

```
# 以官方文档中的basic example为例通过unittest.main执行
(pydev) [root@db1 code]# python utest.py 
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s
(pydev) [root@db1 code]# ./utest.py 
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s
# 更精确的控制执行某一部分用例
(pydev) [root@db1 code]# python -m unittest utest
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s
(pydev) [root@db1 code]# python -m unittest utest.TestStringMethods
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s
(pydev) [root@db1 code]# python -m unittest utest.TestStringMethods.test_isupper
.
----------------------------------------------------------------------
Ran 1 test in 0.000s
(pydev) [root@db1 code]# python -m unittest -v utest
test_isupper (utest.TestStringMethods) ... ok
test_split (utest.TestStringMethods) ... ok
test_upper (utest.TestStringMethods) ... ok
----------------------------------------------------------------------
Ran 3 tests in 0.000s
```

### 简单帮助

```
(pydev) [root@db1 code]# python -m unittest -h
Usage: python -m unittest [options] [tests]

Options:
  -h, --help       Show this message
  -v, --verbose    Verbose output
  -q, --quiet      Minimal output
  -f, --failfast   Stop on first failure
  -c, --catch      Catch control-C and display results
  -b, --buffer     Buffer stdout and stderr during test runs

Examples:
  python -m unittest test_module               - run tests from test_module
  python -m unittest module.TestClass          - run tests from module.TestClass
  python -m unittest module.Class.test_method  - run specified test method

[tests] can be a list of any number of test modules, classes and test
methods.

Alternative Usage: python -m unittest discover [options]

Options:
  -v, --verbose    Verbose output
  -f, --failfast   Stop on first failure
  -c, --catch      Catch control-C and display results
  -b, --buffer     Buffer stdout and stderr during test runs
  -s directory     Directory to start discovery ('.' default)
  -p pattern       Pattern to match test files ('test*.py' default)
  -t directory     Top level directory of project (default to
                   start directory)

For test discovery all test modules must be importable from the top
level directory of the project.
```

## 类和方法

### Test Cases

class unittest.TestCase(methodName='runTest') 

对测试用例testcase的抽象定义，提供了testcase的标准方法

|方法|说明|
|--------|--------|
|setUp()|执行某条测试前需要准备的工作，比如创建某个文件或目录、数据库生成测试数据等。每次调用case前，都会执行这个方法。|
|tearDown()|执行某条测试完后执行清理工作，例如删除临时文件，释放数据库连接等|
|run(result=None)|测试用例运行时执行的部分，可以不实现|
|defaultTestResult()|返回测试结果，是一个testresult对象|
|id()|返回测试用例的标识信息|
|shortDescription()|根据docstr返回该case的短描述|
|addCleanup(function, *args, **kwargs)|增加一个clean方法，在teardown后执行|

支持的各种断言方法

|方法|说明|
|--------|--------|
|assertEqual(a, b)|a == b|
|assertNotEqual(a, b)|a != b|
|assertTrue(x)|bool(x) is True|
|assertFalse(x)|bool(x) is False|   
|assertIs(a, b)|a is b|
|assertIsNot(a, b)|a is not b|
|assertIsNone(x)|x is None|
|assertIsNotNone(x)|x is not None|
|assertIn(a, b)|a in b|
|assertNotIn(a, b)|a not in b|
|assertIsInstance(a, b)|isinstance(a, b)|
|assertNotIsInstance(a, b)|not isinstance(a, b)|
|assertRaises(exc, fun, *args, **kwds)|fun(*args, **kwds) raises exc|
|assertRaisesRegexp(exc, r, fun, *args, **kwds)|fun(*args, **kwds) raises exc and the message matches regex r|
|assertAlmostEqual(a, b)|round(a-b, 7) == 0   |
|assertNotAlmostEqual(a, b)|round(a-b, 7) != 0  | 
|assertGreater(a, b)| a > b 2.7 |
|assertGreaterEqual(a, b)| a >= b 2.7 |
|assertLess(a, b)| a < b 2.7 |
|assertLessEqual(a, b)|a <= b 2.7 |
|assertRegexpMatches(s, r)|r.search(s)|
|assertNotRegexpMatches(s, r)|not r.search(s)|
|assertItemsEqual(a, b)| sorted(a) == sorted(b) and works with unhashable objs |
|assertMultiLineEqual(a, b)|strings| 
|assertSequenceEqual(a, b)|sequences|
|assertListEqual(a, b)|lists|
|assertTupleEqual(a, b)|tuples|
|assertSetEqual(a, b)|sets or frozensets |
|assertDictEqual(a, b)| dicts|

### Group Test

class unittest.TestSuite(tests=()) 

对测试组testsuite的抽象定义。

|方法|说明|
|--------|--------|
|addTest(test)|将case或suite加入suite|
|addTests(tests)|遍历加入|
|run(result) |被TestRun调用|
|countTestCases()||

### Loading and running tests

class unittest.TestLoader 

从类和模块中加载case产生suite，unittest模块提供了默认的实现defaultTestLoader。

class unittest.TestResult

汇总测试结果信息，unittest模块提供了默认的实现TextTestResult

class unittest.TextTestRunner

一个基本的运行器实现

unittest.main([module[, defaultTest[, argv[, testRunner[, testLoader[, exit[, verbosity[, failfast[, catchbreak[, buffer]]]]]]]]]]) 

命令行程序可以调用的入口
```
if __name__ == '__main__':
    unittest.main(verbosity=2)
```