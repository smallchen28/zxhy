# blinker

参考 [Blinker Documentation](http://pythonhosted.org/blinker/)

Blinker 是一个基于Python的强大的信号库，它既支持简单的对象到对象通信，也支持针对多个对象进行组播。Flask的信号机制就是基于它建立的。

Blinker的内核虽然小巧，但是功能却非常强大，它支持以下特性：

- 支持注册全局命名信号
- 支持匿名信号
- 支持自定义命名信号
- 支持与接收者之间的持久连接与短暂连接
- 通过弱引用实现与接收者之间的自动断开连接
- 支持发送任意大小的数据
- 支持收集信号接收者的返回值
- 线程安全

## 使用方法

### 通过命名信号解耦

信号通过signal()方法进行创建：
```
>>> import blinker
>>> ab = blinker.signal('inited')
>>> cd = blinker.signal('inited')
>>> id(ab)
140683392710544
>>> id(cd)
140683392710544
>>> ef = blinker.signal('quited')
>>> id(ef)
140683392710608
```

每次调用signal('name')都会返回同一个信号对象。因此这里signal()方法使用了单例模式。

### 订阅信号

使用Signal.connect()方法注册一个函数，每当触发信号的时候，就会调用该函数。该函数以触发信号的对象作为参数，这个函数其实就是信号订阅者。
```
>>> def subscriber(sender):
...     print("Got a signal sent by %r" % sender)
...
>>> ready = signal('ready')
>>> ready.connect(subscriber)
<function subscriber at 0x...>
```

### 发射信号

使用Signal.send()方法通知信号订阅者。

下面定义类Processor，在它的go()方法中触发前面声明的ready信号，send()方法以self为参数，也就是说Processor的实例是信号的发送者。
```
>>> class Processor:
...    def __init__(self, name):
...        self.name = name
...
...    def go(self):
...        ready = signal('ready')
...        ready.send(self)
...        print("Processing.")
...        complete = signal('complete')
...        complete.send(self)
...
...    def __repr__(self):
...        return '<Processor %s>' % self.name
...
>>> processor_a = Processor('a')
>>> processor_a.go()
Got a signal sent by <Processor a>
Processing.
```

注意到go()方法中的complete信号没？并没有订阅者订阅该信号，但是依然可以触发该信号。如果没有任何订阅者的信号，结果是什么信号也不会发送，而且Blinker内部对这种情况进行了优化，以尽可能的减少内存开销。

### 订阅特定的发布者

默认情况下，任意发布者触发信号，都会通知订阅者。可以给Signal.connect()传递一个可选的参数，以便限制订阅者只能订阅特定发送者。
```
>>> def b_subscriber(sender):
...     print("Caught signal from processor_b.")
...     assert sender.name == 'b'
...
>>> processor_b = Processor('b')
>>> ready.connect(b_subscriber, sender=processor_b)
<function b_subscriber at 0x...>
```

现在订阅者只订阅了processor_b发布的ready信号:
```
>>> processor_a.go()
Got a signal sent by <Processor a>
Processing.
>>> processor_b.go()
Got a signal sent by <Processor b>
Caught signal from processor_b.
Processing.
```

### 通过信号收发数据

可以给send()方法传递额外的关键字参数，这些参数会传递给订阅者。
```
>>> send_data = signal('send-data')
>>> @send_data.connect
... def receive_data(sender, **kw):
...     print("Caught signal from %r, data %r" % (sender, kw))
...     return 'received!'
...
>>> result = send_data.send('anonymous', abc=123)
Caught signal from 'anonymous', data {'abc': 123}
```

send()方法的返回值收集每个订阅者的返回值，拼接成一个元组组成的列表。每个元组的组成为(receiver function, return value)。
```
>>> result
[(<function receive_data at 0x...>, 'received!')]
```

### 匿名信号

前面我们创建的信号都是命名信号，每次调用Signal构造器都会创建一个唯一的信号,，也就是说每次创建的信号是不一样的。下面对前面的Processor类进行改造，将signal作为它的类属性。
```
>>> from blinker import Signal
>>> class AltProcessor:
...    on_ready = Signal()
...    on_complete = Signal()
...
...    def __init__(self, name):
...        self.name = name
...
...    def go(self):
...        self.on_ready.send(self)
...        print("Alternate processing.")
...        self.on_complete.send(self)
...
...    def __repr__(self):
...        return '<AltProcessor %s>' % self.name
...
```

上面创建的就是匿名信号。on_ready与on_complete是两个不同的信号。

### 使用装饰器订阅信号

除了使用connect()方法订阅信号之外，使用@connect修饰器可以达到同样的效果。
```
>>> apc = AltProcessor('c')
>>> @apc.on_complete.connect
... def completed(sender):
...     print "AltProcessor %s completed!" % sender.name
...
>>> apc.go()
Alternate processing.
AltProcessor c completed!
```

尽管这样用起来很方便，但是这种形式不支持订阅指定的发送者。这时，可以使用connect_via()：
```
>>> dice_roll = signal('dice_roll')
>>> @dice_roll.connect_via(1)
... @dice_roll.connect_via(3)
... @dice_roll.connect_via(5)
... def odd_subscriber(sender):
...     print("Observed dice roll %r." % sender)
...
>>> result = dice_roll.send(3)
Observed dice roll 3.
```

### 优化信号发送

信号通常会进行优化，以便快速的发送。不管有没有订阅者，都可以发送信号。如果发送信号时需要传送的参数要计算很长时间，可以在发送之前使用receivers属性先检查一下是否有订阅者。
```
>>> bool(signal('ready').receivers)
True
>>> bool(signal('complete').receivers)
False
>>> bool(AltProcessor.on_complete.receivers)
True
```

还可以检查订阅者是否订阅了某个具体的信号发布者。
```
>>> signal('ready').has_receivers_for(processor_a)
True
```

### 文档化信号

命名和匿名信号可以在构造时传递一个doc参数作为信号的pydoc帮助文本信息。这段说明可以被大部分文档生成器读取

## API


## 代码解析



