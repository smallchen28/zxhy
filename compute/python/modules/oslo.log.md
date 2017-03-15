# oslo.log


## 简介

oslo.log库为openstack项目提供了标准化的日志配置，支持标准日志中的格式，句柄，上下文相关等特性。

### 基本使用原则/步骤

标准库使用方法

```
import logging
LOG = logging.getLogger(__name__)

# Define a default handler at INFO logging level
logging.basicConfig(level=logging.INFO)

LOG.info("Python Standard Logging")
LOG.warning("Python Standard Logging")
LOG.error("Python Standard Logging")
```

oslo.log库的使用方法

```
from oslo_config import cfg  
from oslo_log import log as logging  
  
LOG = logging.getLogger(__name__)  
CONF = cfg.CONF  
DOMAIN = "demo"  
 
# 向config注册log模块的配置模式
logging.register_options(CONF)  

# 可选步骤，设置默认信息。各个模块的打印级别都不同
_DEFAULT_LOG_LEVELS = ['amqp=WARN', 'amqplib=WARN', 'boto=WARN',
                       'qpid=WARN', 'stevedore=WARN', 'oslo_log=INFO',
                       'iso8601=WARN', 'elasticsearch=WARN',
                       'requests.packages.urllib3.connectionpool=WARN',
                       'urllib3.connectionpool=WARN', 'websocket=WARN',
                       'keystonemiddleware=WARN', 'routes.middleware=WARN']
_DEFAULT_LOGGING_CONTEXT_FORMAT = ('%(asctime)s.%(msecs)03d %(process)d '
                                   '%(levelname)s %(name)s [%(request_id)s'
                                   ' %(user_identity)s] %(instance)s '
                                   '%(message)s')
logging.set_defaults(_DEFAULT_LOGGING_CONTEXT_FORMAT, _DEFAULT_LOG_LEVELS)
# 根据配置和域信息进行加载	
logging.setup(CONF, DOMAIN)  
  
# Oslo Logging uses INFO as default  
LOG.info("Oslo Logging")  
LOG.warning("Oslo Logging")  
LOG.error("Oslo Logging")
```

## 模块使用

### 配置项

这里日志的配置读取通过oslo.config完成。这些配置项对整个openstack项目的配置文件中日志部分都是统一的。

通过配置文件log_config_append可以更复杂的控制log中相关loggers,handlers,formatters。这部分配置参见pythonlog使用规范

|配置项|类型|说明|
|--------|--------|--------|
|debug|boolean|日志输出的默认级别为debug|
|verbose|boolean|true时日志输出的默认级别为info，已不建议使用|
|log_config_append|string|日志配置文件|
|log_date_format|string|日志输出的时间格式:%Y-%m-%d %H:%M:%S|
|log_file|string|日志输出的文件，没有则是stderr|
|log_dir|string|日志输出的路径|
|watch_log_file|boolean|当日志被移除时是否重新生成|
|use_syslog|boolean||
|syslog_log_facility|string||
|logging_context_format_string|string|日志中context的格式|
|logging_default_format_string|string|日志默认的格式|
|logging_debug_format_suffix|string|debug日志前缀格式|
|logging_exception_prefix|string|异常日志前缀格式|
|logging_user_identity_format|string|日志中用户标识的格式|
|default_log_levels|list|默认日志级别|
|publish_errors|boolean|异常日志前缀格式|
|instance_format|string|日志中虚机实例格式|
|instance_uuid_format|string|日志中uuid格式|
|rate_limit_interval|integer|控制日志的输出频率|
|rate_limit_burst|integer||
|rate_limit_except_level|string||
|fatal_deprecations|boolean||

### log模块

这个模块定义了基本的几个方法

|方法|说明|
|--------|--------|
|oslo_log.log.getLogger(name=None, project='unknown', version='unknown')|创建日志对象|
|oslo_log.log.get_default_log_levels()|获取默认的日志级别设置|
|oslo_log.log.set_defaults(logging_context_format_string=None, default_log_levels=None)|设置默认值|
|oslo_log.log.register_options(conf)|将log模块的配置项模式注册到opt中|
|oslo_log.log.setup(conf, product_name, version='unknown')|加载日志项|

## 示例

一个标准的openstack中示例
```
# Use default Python logging to display running output
import logging as py_logging
from oslo_config import cfg
from oslo_log import log as logging

LOG = py_logging.getLogger(__name__)
CONF = cfg.CONF
DOMAIN = "demo"

def prepare():
    """Prepare Oslo Logging (2 or 3 steps)

    Use of Oslo Logging involves the following:

    * logging.register_options
    * logging.set_defaults (optional)
    * logging.setup
    """

    LOG.debug("Prepare Oslo Logging")

    LOG.info("Size of configuration options before %d", len(CONF))

    # Required step to register common, logging and generic configuration
    # variables
    logging.register_options(CONF)

    LOG.info("Size of configuration options after %d", len(CONF))

    # Optional step to set new defaults if necessary for
    # * logging_context_format_string
    # * default_log_levels
    #
    # These variables default to respectively:
    #
    #  import oslo_log
    #  oslo_log._options.DEFAULT_LOG_LEVELS
    #  oslo_log._options.log_opts[0].default
    #

    custom_log_level_defaults = logging.get_default_log_levels() + [
        'dogpile=INFO',
        '__main__=DEBUG' #此处将本模块的打印调整为DEBUG级别
        ]

    logging.set_defaults(default_log_levels=custom_log_level_defaults)

    # NOTE: We cannot show the contents of the CONF object
    # after register_options() because accessing this caches
    # the default_log_levels subsequently modified with set_defaults()
    LOG.info("List of Oslo Logging configuration options and current values")
    LOG.info("=" * 80)
    for c in CONF:
        LOG.info("%s = %s" % (c, CONF[c]))
    LOG.info("=" * 80)

    # Required setup based on configuration and domain
    logging.setup(CONF, DOMAIN)

if __name__ == '__main__':
    py_logging.basicConfig(level=py_logging.DEBUG)

    prepare()
    # 查看实际的日志配置值
    LOG.warning(CONF.debug)
    # NOTE: These examples do not demonstration Oslo i18n messages
    LOG.info("Welcome to Oslo Logging")
    LOG.debug("A debugging message")
    LOG.warning("A warning occurred")
    LOG.error("An error occurred")
    try:
        raise Exception("This is exceptional")
    except Exception:
        LOG.exception("An Exception occurred")
```

显示结果
```
(pydev) [root@db1 code]# python usage_helper.py 
DEBUG:__main__:Prepare Oslo Logging
INFO:__main__:Size of configuration options before 0
INFO:__main__:Size of configuration options after 22
INFO:__main__:List of Oslo Logging configuration options and current values
INFO:__main__:================================================================================
INFO:__main__:default_log_levels = ['amqp=WARN', 'amqplib=WARN', 'boto=WARN', 'qpid=WARN', 'sqlalchemy=WARN', 'suds=INFO', 'oslo.messaging=INFO', 'iso8601=WARN', 'requests.packages.urllib3.connectionpool=WARN', 'urllib3.connectionpool=WARN', 'websocket=WARN', 'requests.packages.urllib3.util.retry=WARN', 'urllib3.util.retry=WARN', 'keystonemiddleware=WARN', 'routes.middleware=WARN', 'stevedore=WARN', 'taskflow=WARN', 'keystoneauth=WARN', 'oslo.cache=INFO', 'dogpile.core.dogpile=INFO', 'dogpile=INFO', '__main__=DEBUG']
INFO:__main__:verbose = True
INFO:__main__:watch_log_file = False
INFO:__main__:logging_default_format_string = %(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [-] %(instance)s%(message)s
INFO:__main__:use_stderr = False
INFO:__main__:log_date_format = %Y-%m-%d %H:%M:%S
INFO:__main__:rate_limit_burst = 0
INFO:__main__:logging_context_format_string = %(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [%(request_id)s %(user_identity)s] %(instance)s%(message)s
INFO:__main__:instance_format = [instance: %(uuid)s] 
INFO:__main__:use_syslog = False
INFO:__main__:log_dir = None
INFO:__main__:publish_errors = False
INFO:__main__:logging_debug_format_suffix = %(funcName)s %(pathname)s:%(lineno)d
INFO:__main__:logging_exception_prefix = %(asctime)s.%(msecs)03d %(process)d ERROR %(name)s %(instance)s
INFO:__main__:syslog_log_facility = LOG_USER
INFO:__main__:instance_uuid_format = [instance: %(uuid)s] 
INFO:__main__:log_config_append = None
INFO:__main__:rate_limit_except_level = CRITICAL
INFO:__main__:rate_limit_interval = 0
INFO:__main__:debug = False
INFO:__main__:log_file = None
INFO:__main__:logging_user_identity_format = %(user)s %(tenant)s %(domain)s %(user_domain)s %(project_domain)s
INFO:__main__:================================================================================
2017-03-15 16:27:27.413 23448 INFO __main__ [-] Welcome to Oslo Logging
2017-03-15 16:27:27.413 23448 DEBUG __main__ [-] A debugging message <module> usage_helper.py:97
2017-03-15 16:27:27.413 23448 WARNING __main__ [-] A warning occurred
2017-03-15 16:27:27.413 23448 ERROR __main__ [-] An error occurred
2017-03-15 16:27:27.413 23448 ERROR __main__ [-] An Exception occurred
2017-03-15 16:27:27.413 23448 ERROR __main__ Traceback (most recent call last):
2017-03-15 16:27:27.413 23448 ERROR __main__   File "usage_helper.py", line 101, in <module>
2017-03-15 16:27:27.413 23448 ERROR __main__     raise Exception("This is exceptional")
2017-03-15 16:27:27.413 23448 ERROR __main__ Exception: This is exceptional
2017-03-15 16:27:27.413 23448 ERROR __main__ 
```

从配置文件和命令行参数获取log配置
```
# 在setup前增加CONF的加载，这样会从命令行参数和项目默认路径加载配置项
CONF(sys.argv[1:],
     project=DOMAIN)
logging.setup(CONF, DOMAIN)    

# 命令执行，可以看到一个配置是命令传递，另一个是配置文件配置
(pydev) [root@db1 code]# python usage_helper.py --log-file=aa.log
(pydev) [root@db1 code]# cat /root/demo.conf 
[DEFAULT]

debug=True

# 日志输出到了aa.log中
(pydev) [root@db1 code]# cat aa.log 
2017-03-15 17:11:11.849 3485 WARNING __main__ [-] True #这项是debug的值
2017-03-15 17:11:11.850 3485 INFO __main__ [-] Welcome to Oslo Logging
2017-03-15 17:11:11.850 3485 DEBUG __main__ [-] A debugging message <module> usage_helper.py:101
2017-03-15 17:11:11.850 3485 WARNING __main__ [-] A warning occurred
2017-03-15 17:11:11.850 3485 ERROR __main__ [-] An error occurred
2017-03-15 17:11:11.850 3485 ERROR __main__ [-] An Exception occurred
2017-03-15 17:11:11.850 3485 ERROR __main__ Traceback (most recent call last):
2017-03-15 17:11:11.850 3485 ERROR __main__   File "usage_helper.py", line 105, in <module>
2017-03-15 17:11:11.850 3485 ERROR __main__     raise Exception("This is exceptional")
2017-03-15 17:11:11.850 3485 ERROR __main__ Exception: This is exceptional
2017-03-15 17:11:11.850 3485 ERROR __main__ 
(pydev) [root@db1 code]# 
```

日志的国际化
```
from oslo_config import cfg
from oslo_log import log as logging
from _i18n import _, _LI, _LW, _LE  # noqa

if __name__ == '__main__':
    prepare()
    # NOTE: These examples use Oslo i18n marker functions

    LOG.info(_LI("Welcome to Oslo Logging"))
    LOG.debug("A debugging message")  # Debug messages are not translated
    LOG.warning(_LW("A warning occurred"))
    LOG.error(_LE("An error occurred"))
    try:
        raise Exception(_("This is exceptional"))
    except Exception:
        LOG.exception(_LE("An Exception occurred"))
```
