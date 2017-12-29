
## 上下文管理器

上下文管理器manager是可以在with语句中使用，拥有__enter__和__exit__方法的对象。
```
with manager as var:
    do_something(var)

# 相当于以下情况的简化

var = manager.__enter__()
try:
    do_something(var)
finally:
    manager.__exit__()

with open('a.txt') as f:
```

换言之，[PEP 343](http://www.python.org/dev/peps/pep-0343)中定义的上下文管理器协议允许将无聊的try...except...finally结构抽象到一个单独的类中，仅仅留下关注的do_something部分。

1.__enter__方法首先被调用。它可以返回赋给var的值。as部分是可选的：如果它不出现，enter的返回值简单地被忽略。
2.with语句下的代码被执行。就像try子句，它们或者成功执行到底，或者break，continue或return，或者可以抛出异常。无论哪种情况，该块结束后，__exit__方法被调用。如果抛出异常，异常信息被传递给__exit__，这将在下一段讨论。通常情况下，异常可被忽略，就像在finally子句中一样，并且将在__exit__结束后重新抛出。

try...finally常见的用法是释放资源。各种不同的情况实现相似：在__enter__阶段资源被获得，在__exit__阶段释放，如果抛出异常也被传递。正如文件操作，往往这是对象使用后的自然操作，内置支持使之很方便。每一个版本，Python都在更多的地方提供支持。

当前已有的内置支持
    所有类似文件的对象：

        file   自动关闭
        fileinput,tempfile(py >= 3.2)
        bz2.BZ2File，gzip.GzipFile,
        tarfile.TarFile,zipfile.ZipFile
        ftplib, nntplib  关闭连接(py >= 3.2)
    锁

        multiprocessing.RLock  锁定和解锁
        multiprocessing.Semaphore
        memoryview   自动释放(py >= 3.2 或 3.3)
    decimal.localcontext  暂时更改计算精度
    _winreg.PyHKEY   打开和关闭Hive Key
    warnings.catch_warnings   暂时杀死(kill)警告
    contextlib.closing   如上例，调用close
    并行编程

        concurrent.futures.ThreadPoolExecutor         并行调用然后杀掉线程池(py >= 3.2)
        concurrent.futures.ProcessPoolExecutor        并行调用并杀死进程池(py >= 3.2)
        nogil   暂时解决GIL问题(仅仅cyphon ：（)


### 捕获异常
当一个异常在with块中抛出时，它作为参数传递给__exit__。和sys.exc_info()返回的相同有三个参数被使用：类型、值和回溯(traceback)。当没有异常抛出时，三个参数都是None。上下文管理器可以通过从__exit__返回一个真(True)值来“吞下”异常，否则异常还要向上层抛出。

可以参考unittest.case._AssertRaisesContext实现
```
class _AssertRaisesContext(object):
    """A context manager used to implement TestCase.assertRaises* methods."""

    def __init__(self, expected, test_case, expected_regexp=None):
        self.expected = expected
        self.failureException = test_case.failureException
        self.expected_regexp = expected_regexp

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            try:
                exc_name = self.expected.__name__
            except AttributeError:
                exc_name = str(self.expected)
            raise self.failureException(
                "{0} not raised".format(exc_name))
        if not issubclass(exc_type, self.expected):
            # let unexpected exceptions pass through
            return False
        self.exception = exc_value # store for later retrieval
        if self.expected_regexp is None:
            return True

        expected_regexp = self.expected_regexp
        if not expected_regexp.search(str(exc_value)):
            raise self.failureException('"%s" does not match "%s"' %
                     (expected_regexp.pattern, str(exc_value)))
        return True
```

### 使用生成器定义上下文管理器
```
@contextlib.contextmanager
def some_generator(<arguments>):
    <setup>
    try:
        yield <value>
    finally:
        <cleanup>
```