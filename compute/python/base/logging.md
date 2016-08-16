# Logging

## 基本概念
一段日志内容是通过logRecord对象最终产生，这个对象包含了loggers,handlers,filters,formatters四个部分
1. Loggers expose the interface that application code directly uses.
向应用提供了调用接口
2. Handlers send the log records (created by loggers) to the appropriate destination.
将日志内容实际输出
3. Filters provide a finer grained facility for determining which log records to output.
过滤器过滤输出结果
4. Formatters specify the layout of log records in the final output.
对输出内容进行格式化

### logging级别
数值越大说明越严重，默认只输出warning级别以上日志。

|级别|数值|
|--------|--------|
|CRITICAL| 50 |
|ERROR | 40 |
|WARNING| 30 |
|INFO| 20 |
|DEBUG |10 |
|NOTSET | 0 |


### 模块级方法
| 方法 |说明|参数或示例|
|--------|--------|--------|
|logging.getLogger() |      获取logger对象  | logging.getLogger('a.b')|
|logging.basicConfig()|创建一个默认formater的streamhandler，并加入到rootlogger。如果rootlogger的handler被设置过则没有用。如果没有指定格式则默认输出为`severity:logger name:message`。必须在主线程初始化阶段使用|参数包括level,format,strem,filename,filemode,dateformat|
|logging.setLoggerClass()|设置当前的Logger类，每次初始化新logger时都是创建一个此类对象|setLoggerClass(myLogger)|
|logging.getLoggerClass()|获取当前的logger类||
|logging.shutdown()|在系统退出或不再使用日志系统时使用，可以将所有日志刷新输出并关闭handlers||
|logging.info()|直接进行info级别的日志输出|logging.info('this is info')|
|logging.debug()|debug级别||
|logging.error() |||
|logging.log()|直接进行某级别的日志输出|log(level=logging.info, 'this is info')|

### Logger对象
logger对象应该通过logging.getLogger方法创建，具有相同名称的对象只会被创建一次。logger对象依照名称具有类似python的层级。建议使用`logging.getLogger(__name__)`获取当前模块的logger对象。
通过logging.getLogger()或者logging.getLogger("")得到root logger实例。

| 方法或属性 |说明|参数或示例|
|--------|--------|--------|
|Logger.propagate|传递属性，向父logger进行传递||
|Logger.setLevel()|设置logger日志输出级别||
|Logger.getChild()|获取子logger| logging.getLogger('abc').getChild('def.ghi')|
|Logger.debug()|以debug级别记录日志||
|Logger.info()|以info级别记录日志||
|Logger.warning()|以warning级别记录日志||
|Logger.error()|以error级别记录日志||
|Logger.critical()|以critical级别记录日志||
|Logger.exception()|以error级别记录日志||
|Logger.addFilter()|增加过滤器||
|Logger.removeFilter()|移除过滤器||
|Logger.addHandler()|增加处理器||
|Logger.removeHandler()|移除处理器||
|Logger.findCaller()|返回当前调用的文件名,行号,方法名元组||


### Handler对象
这是一个父类，不能直接创建对象，必须使用Handler子类。handler对象定义了基本的方法和属性

| 方法或属性 |说明|参数或示例|
|--------|--------|--------|
|Handler.setLevel()|设置handler输出级别||
|Handler.setFormatter()|设置handler关联的formatter||
|Handler.addFilter()|增加handler关联的filter||
|Handler.removeFilter()|移除handler关联的filter||
|Handler.flush()|刷新日志内容||
|Handler.close()|关闭日志输出||

系统在模块`logging.handlers`提供了一些默认的实现
#### handlers实现
| 类 |说明|参数或示例|
|--------|--------|--------|
|StreamHandler|流处理器,支持stdout,stderr,file类对象|参数为file对象，默认为standerr|
|FileHandler|文件处理器,继承自streamhandle|参数包括filename,mode,encoding,delay|
|NullHandler|空处理器,不进行任何输出|上面三个handler归属在模块logging下，其他的在logging.handlers|
|WatchedFileHandler|||
|RotatingFileHandler|支持回转的文件处理器,支持回转覆盖|参数还包括maxbytes,backupcount|
|TimedRotatingFileHandler|支持根据时间回转的文件处理器,支持按时间回转覆盖|参数还包括when,interval,backupcount|
|SocketHandler|支持socket处理器，TCP/IP|参数为host,port|
|DatagramHandler|数据报UDP处理器，继承自sockethandler|参数为host,port|
|SysLogHandler|系统日志处理器,支持输出到本地或远程的unix syslog||
|NTEventLogHandler|win系统日志处理器,支持win系统日志||
|SMTPHandler|支持通过smtp服务发送邮件日志||
|MemoryHandler|内存日志处理器，将日志缓存到内存中||
|HTTPHandler|支持通过getpost发送日志到web服务器||


### formatter对象
指定了日志输出时的格式，不进行设置时默认的日志格式就只有message部分，就是'%(message)s' 。
可以在创建format对象时指定格式，也可以创建自己的子类定义格式。一般包括datefmt+msgfmt两部分定义

| 方法或属性 |说明|参数或示例|
|--------|--------|--------|
|logging.Formatter()|创建一个format对象|参数包括fmt,datefmt。实际对应了下面两个方法|
|fmt.format()|对msg部分的格式定义|系统提供了默认和用户自定义的条目，具体参见下面的logrecord属性表格|
|fmt.formatTime()|对date部分的格式定义|时间格式参照time模块部分|


### filter对象
可以为handler和logger提供除级别外更精确的过滤操作。
可以创建一个指定的fliter对象，也可以创建子类进行示例化。


### logrecord对象
当每次logger对象进行一次日志记录，都会产生一个对应的logrecord对象。
这个对象包含了一条日志所关联的相关其他附属属性，有些属性可以在format中使用

| 属性 |格式|说明|
|--------|--------|--------|
|asctime|%(asctime)s|日志产生时间|
|created|%(created)f|日志产生时间|
|filename|%(filename)s|产生日志的模块对应的文件路径名|
|funcName|%(funcName)s|产生日志的对应方法名|
|levelname|%(levelname)s|日志级别|
|levelno|%(levelno)s|日志级别编号|
|lineno|%(lineno)d|日志产生所在的行号|
|module|%(module)s|日志产生所在的模块|
|msecs|%(msecs)d|日志产生时间 毫秒|
|message|%(message)s|日志体|
|name|%(name)s|产生日志的logger对象的名称|
|pathname|%(pathname)s|全路径|
|process|%(process)d|进程号|
|processName|%(processName)s|进程名|
|thread|%(thread)d|线程号|
|threadName|%(threadName)s|线程名|
|relativeCreated|%(relativeCreated)d|相对日志模块加载的时间，单位毫秒|
|args|||
|exc_info|||
|msg|||


## config，基于配置的日志定义

对日志的配置，logging提供了三种模式
1. Creating loggers, handlers, and formatters explicitly using Python code that calls the configuration methods listed above.
2. Creating a logging config file and reading it using the fileConfig() function.
3. Creating a dictionary of configuration information and passing it to the dictConfig() function.


## 示例

- 直接输出日志

```
import logging

logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')
```

- 使用baseconfig

```
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')
```

- 设置handler

```
import logging
from logging.handlers import RotatingFileHandler

#定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
rthandler = RotatingFileHandler('myapp.log', maxBytes=10*1024*1024,backupCount=5)
rthandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
rthandler.setFormatter(formatter)
logging.getLogger(__name__).addHandler(rthandler)
```

- 设置复杂的format

```
FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)
d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
logger = logging.getLogger('tcpserver')
logger.warning('Protocol problem: %s', 'connection reset', extra=d)
# 输出结果如下
2006-02-08 22:20:02,165 192.168.0.1 fbloggs  Protocol problem: connection reset
```

- 定义库的日志输出

```
# 将代码作为第三方库发布时应该仔细的进行log设置说明，通常的建议是将库中的日志功能屏蔽。因为怎样进行日志输出的设置是开发者的特权，如果库也有日志输出很容易和应用的日志输出混淆起来。
import logging
logging.getLogger('foo').addHandler(logging.NullHandler())
```
