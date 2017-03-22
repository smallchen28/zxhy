# mock

## 简介

Mock这个词在英语中有模拟的这个意思，因此我们可以猜测出这个库的主要功能是模拟一些东西。准确的说，Mock是Python中一个用于支持单元测试的库，它的主要功能是使用mock对象替代掉指定的Python对象，以达到模拟对象的行为。

python2.7及之前版本，需要单独安装mock来使用，python3.3之后版本将mock集成进了unittest，使用unittest.mock即可。

### 使用Mock的理由

当测试代码运行时，需要被测试代码以一定的规则进行运行，并对运行的结果(也有可能是中间或初始状态等)进行检查。而被测试代码运行时
还依赖于一些测试资源(如更底层的调用/某些特定模块类对象等)的运行。测试时关注的是被测试对象，这些测试资源的实现并不关心。

某些情况下测试资源可能不可用，代价高等原因并不适合被调用。mock向测试对象提供一套和测试资源相同的方法接口并且更容易创建和管理。它能向测试对象提供和真实的测试资源相同的方法接口。它能提供确定的结果，并可以自定义以适用于特定的测试。能够容易的更新，以反映实际资源的变化。

### 使用原则

Mock对象的一般用法是这样的：

1.找到你要替换的对象，这个对象可以是一个类，或者是一个函数，或者是一个类实例。

2.然后实例化Mock类得到一个mock对象，并且设置这个mock对象的行为，比如被调用的时候返回什么值，被访问成员的时候返回什么值等。

3.使用这个mock对象替换掉我们想替换的对象，也就是步骤1中确定的对象。

4.之后就可以开始写测试代码，这个时候我们可以保证我们替换掉的对象在测试用例执行的过程中行为和我们预设的一样。

太多的mock会使测试过于复杂，让你跟踪错误变得更困难。最好的实践是每个测试用例限制使用一到两个mock，或者为每个mock/对象对使用独立的测试用例。
	
### Mocks对Stubs对Fakes

认识stub:stub为测试对象提供了一套方法接口，和真实的测试资源提供给测试对象的接口是相同的。当测试对象调用stub方法时，stub响应预定的结果。也可以产生一个预定的错误或者异常。stub可以跟踪和测试对象的交互，但是它不处理输入的数据。

fake也提供了一套方法接口并且也可以跟踪和测试对象的交互。但是和stub不同，fake真正的处理了从测试对象输入的数据产生的结果是基于这些数据的。简而言之，fake是功能性的，它是真实测试资源的非生产版。

### 个人理解



## 使用Mock

### Mock类

class unittest.mock.Mock(spec=None, side_effect=None, return_value=DEFAULT, wraps=None, name=None, spec_set=None, unsafe=False, **kwargs)

mock类有常用的四组方法，下面依次说明

#### 初始化

|参数|说明|其他|
|--------|---------|--------|
|spec|字符串列表或模拟类|如果传入类则mock模拟该对象的属性或方法，不会多出其他属性|
|spec_set|||
|side_effect|调用模拟时调用的函数||
|return_value|调用模拟是返回的值||
|wraps|||
|name|用于模拟对象的repr表达||
|unsafe|允许属性以assert开头|为了防止为断言方法冲突？|

#### 断言方法

断言方法将帮助跟踪测试对象对mock方法的调用。他们能和unittest模块的断言一起工作。

|方法|说明|其他|
|--------|---------|--------|
|assert_called_with(*args, **kwargs)|检查mock方法是否获得了正确的参数调用|参数类型，顺序，数量有差别都将失败|
|assert_called_once_with(*args, **kwargs)|断言该模拟被调用了一次，并使用指定的参数。||
|assert_any_call(*args, **kwargs)|断言模拟是否被调用过(不定次)|参数比较，上面两个只比较最近一次|
|assert_has_calls(calls, any_order=False)|断言调用多次并且调用顺序固定|参见示例|
|assert_not_called()|断言从未被调用过||

#### 工具方法

这部分方法允许你控制和管理mock对象。

|方法|说明|其他|
|--------|---------|--------|
|reset_mock()|重置一个mock对象上的所有调用属性|不会清除mock对象的return_value和side_effect属性和它的方法属性|
|attach_mock(mock, attribute)|通过属性名替换为一个属性/方法为新的模拟|参见下面示例|
|configure_mock(**kwargs)|批量的更改mock对象|参数是一个键值对序列，每个键就是你想要修改的属性|
|mock_add_spec(spec, spec_set=False)|添加属性spec||

还可以直接对方法属性进行修改，设置对应returnvalue和sideeffect

```
mockFoo.callFoo.return_value = "narf"
mockFoo.callFoo.side_effect = TypeError
mockFoo.callFoo.side_effect = None
```

#### 统计方法

这部分方法对mock的使用进行了统计

|方法|说明|其他|
|--------|---------|--------|
|called|模拟对象是否被调用过|boolean值|
|call_count|模拟对象是被调用次数|int值|
|return_value|设置或返回对象调用返回值||
|side_effect|设置或返回对象调用的sideeff|注意这里除了最下面两个都是对象调用，不是对象的方法调用？|
|call_args|模拟调用的参数|是一个元组形式|
|call_args_list|模拟调用的参数按调用顺序列表|[(),()]的形式|
|method_calls|对方法和属性的调用||
|mock_calls|记录所有对模拟对象以及属性方法的调用||

```
>>> mok = Mock()
>>> mok.return_value = 'fish'
>>> mok()
'fish'

>>> mok = mock.Mock()
>>> mok()
<Mock name='mock()' id='140674781282576'>
>>> mok.method_calls
[]
>>> mok.method()
<Mock name='mock.method()' id='140674781284240'>
>>> mok.method_calls
[call.method()]
>>> mok.mock_calls
[call(), call.method()]
>>> 
```

### MagicMock



### Patcher补丁

这两个函数作为函数装饰器，类装饰器或上下文管理器使用。都会返回一个mock内部的类实例

```
unittest.mock.patch(target, new=DEFAULT, spec=None, create=False, spec_set=None, autospec=None, new_callable=None, **kwargs)

unittest.mock.patch.object(target, attribute, new=DEFAULT, spec=None, create=False, spec_set=None, autospec=None, new_callable=None, **kwargs)
```

使用patch或者patch.object的目的是为了控制mock的范围，意思就是在一个函数范围内，或者一个类的范围内，或者with语句的范围内mock掉一个对象。

```
class TestClient(unittest.TestCase):

    def test_success_request(self):
        status_code = '200'
        success_send = mock.Mock(return_value=status_code)
        with mock.patch('client.send_request', success_send):
            from client import visit_ustack
            self.assertEqual(visit_ustack(), status_code)

    def test_fail_request(self):
        status_code = '404'
        fail_send = mock.Mock(return_value=status_code)
        with mock.patch('client.send_request', fail_send):
            from client import visit_ustack
            self.assertEqual(visit_ustack(), status_code)

    # patch.object的表示方法，替换掉一个对象的属性/方法
    def test_fail_request(self):
        status_code = '404'
        fail_send = mock.Mock(return_value=status_code)
        with mock.patch.object(client, 'send_request', fail_send):
            from client import visit_ustack
            self.assertEqual(visit_ustack(), status_code)
```

patch.object以装饰器的方式替换某个类的方法

```
# Mock某一个类的方法：
import mock
import Module1 
@mock.patch.object(Module1.Class1, 'some_method') 
def test(mock_method): 
     mock_method.return_value = 3 
     mock_method.side_effect = some_side_effect 
     m = Module1.Class1() 
     m.some_method(*args, **kwargs) 
     assert m.some_method is mock_method 
     m.some_method.assert_called_with(*args, **kwargs)
```


## 示例

根据某个对象创建一个mock对象

```
from mock import Mock

# The class interfaces
class Foo(object):
    # instance properties
    _fooValue = 123
    
    def callFoo(self):
        print "Foo:callFoo_"
    
    def doFoo(self, argValue):
        print "Foo:doFoo:input = ", argValue    

# 传递字符串列表的写法
#fooSpec = ["_fooValue", "callFoo", "doFoo"]
#mockFoo = Mock(spec = fooSpec)

# 传递模拟对象的写法，产生了一个和Foo类具有同样属性的模拟对象。
# create the mock object
mockFoo = Mock(spec = Foo)

# accessing the mocked attributes
print mockFoo
# returns <Mock spec='Foo' id='507120'>
print mockFoo._fooValue
# returns <Mock name='mock._fooValue' id='2788112'>
print mockFoo.callFoo()
# returns: <Mock name='mock.callFoo()' id='2815376'>

# 注意具有相同的属性，但没有实际操作
mockFoo.callFoo()
# nothing happens, which is fine

# accessing the missing attributes
print mockFoo._fooBar
# raises: AttributeError: Mock object has no attribute '_fooBar'
mockFoo.callFoobar()
# raises: AttributeError: Mock object has no attribute 'callFoobar'
```

使用断言判断函数参数是否调用正确

```
# 使用上面的Foo类
# create the mock object
mockFoo = Mock(spec = Foo)
print mockFoo
# returns <Mock spec='Foo' id='507120'>

mockFoo.doFoo("narf")
mockFoo.doFoo.assert_called_with("narf")
# assertion passes

mockFoo.doFoo("zort")
mockFoo.doFoo.assert_called_with("narf")
# AssertionError: Expected call: doFoo('narf')
# Actual call: doFoo('zort')
```

使用断言判断函数调用此时及顺序是否正确

```
# create the mock object
mockFoo = Mock(spec = Foo)
print mockFoo
# returns <Mock spec='Foo' id='507120'>

mockFoo.callFoo()
mockFoo.doFoo("narf")
mockFoo.doFoo("zort")

fooCalls = [call.callFoo(), call.doFoo("narf"), call.doFoo("zort")]
mockFoo.assert_has_calls(fooCalls)
# assert passes

fooCalls = [call.callFoo(), call.doFoo("zort"), call.doFoo("narf")]
mockFoo.assert_has_calls(fooCalls)
# AssertionError: Calls not found.
# Expected: [call.callFoo(), call.doFoo('zort'), call.doFoo('narf')]
# Actual: [call.callFoo(), call.doFoo('narf'), call.doFoo('zort')]

fooCalls = [call.callFoo(), call.doFoo("zort"), call.doFoo("narf")]
mockFoo.assert_has_calls(fooCalls, any_order = True)
# assert passes
```

attach_mock示例

```
from mock import Mock

# The mock object
class Foo(object):
    # instance properties
    _fooValue = 123
    
    def callFoo(self):
        print "Foo:callFoo_"
    
    def doFoo(self, argValue):
        print "Foo:doFoo:input = ", argValue

class Bar(object):
    # instance properties
    _barValue = 456
    
    def callBar(self):
        pass
    
    def doBar(self, argValue):
        pass

# create the first mock object
mockFoo = Mock(spec = Foo)
print mockFoo
# returns <Mock spec='Foo' id='507120'>

# create the second mock object
mockBar = Mock(spec = Bar)
print mockBar
# returns: <Mock spec='Bar' id='2784400'>

# attach the second mock to the first
mockFoo.attach_mock(mockBar, 'fooBar')

# access the first mock's attributes
print mockFoo
# returns: <Mock spec='Foo' id='495312'>
print mockFoo._fooValue
# returns: <Mock name='mock._fooValue' id='428976'>
print mockFoo.callFoo()
# returns: <Mock name='mock.callFoo()' id='448144'>

# access the second mock and its attributes
print mockFoo.fooBar
# returns: <Mock name='mock.fooBar' spec='Bar' id='2788592'>
print mockFoo.fooBar._barValue
# returns: <Mock name='mock.fooBar._barValue' id='2788016'>
print mockFoo.fooBar.callBar()
# returns: <Mock name='mock.fooBar.callBar()' id='2819344'>
print mockFoo.fooBar.doBar("narf")
# returns: <Mock name='mock.fooBar.doBar()' id='4544528'>
```

configuremock示例

```
mockFoo.configure_mock(return_value = 999)
print mockFoo()
# returns: 999

fooSpec = {'callFoo.return_value':"narf", 'doFoo.return_value':"zort", 'doFoo.side_effect':StandardError}
mockFoo.configure_mock(**fooSpec)

print mockFoo.callFoo()
# returns: narf
print mockFoo.doFoo("narf")
# raises: StandardError

fooSpec = {'doFoo.side_effect':None}
mockFoo.configure_mock(**fooSpec)
print mockFoo.doFoo("narf")
# returns: zort
```

callarglist示例

```
>>> mock = Mock(return_value=None)
>>> mock()
>>> mock(3, 4)
>>> mock(key='fish', next='w00t!')
>>> mock.call_args_list
[call(), call(3, 4), call(key='fish', next='w00t!')]
>>> expected = [(), ((3, 4),), ({'key': 'fish', 'next': 'w00t!'},)]
>>> mock.call_args_list == expected
True
```

patch示例

```
>>> class MyTest(testtools.TestCase):
...     # 使用自定义方法来替换原有方法
...     @patch.object(SomeClass， 'attribute'， sentinel.attribute)
...     # 使用自动的 Mock 对象来替换原有对象，Mock 对象会被作为参数自动传给
...     # 测试函数，注意顺序与修饰时顺序相反。
...     @patch('package.module.ClassName1')
...     @patch('package.module.ClassName2')
...     def test_something(self， MockClass2， MockClass1):
...         self.assertEqual(SomeClass.attribute， sentinel.attribute)
...         self.assertTrue(package.module.ClassName1 is MockClass1)
...         self.assertTrue(package.module.ClassName2 is MockClass2)
...
>>> original = SomeClass.attribute
>>> MyTest('test_something').test_something()
# 在 patch 所修饰的函数之外，替换没有作用，patch 有其作用域
>>> assert SomeClass.attribute == original
>>> class ProductionClass(object):
...     def method(self):
...         pass
...
>>> with patch.object(ProductionClass， 'method') as mock_method:
...     mock_method.return_value = None
...     real = ProductionClass()
...     real.method(1， 2， 3)
```