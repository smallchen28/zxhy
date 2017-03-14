# oslo.config


## 简介

oslo.config库是openstack项目中被广泛使用的库，该子项目工作的主要目的就是解析OpenStack中命令行（CLI）或配置文件（.conf）中的配置信息。

### 基本概念

- 配置文件：具有INI风格的配置文件，通常以cnf/conf结尾
- 配置项：配置文件或命令行参数中键值对的key部分
- 配置项值：键值对中value部分
- 配置组：逻辑上相关的一组配置项/值，以[section]命名组名
- 配置项模式：在解析配置获取配置项值之前，模块需要声明本模块内需要的配置项。说明了配置项的转换规则
- 注册：模块在使用配置项前必须注册自己要使用的配置项模式

### 基本使用原则/步骤

1.配置文件准备

2.在模块中声明要使用的配置项模式

3.创建配置对象，将配置项模式注册进配置对象

4.通过配置对象转换配置文件或命令行参数

5.使用配置对象解析出的配置项

## 模块说明

### cfg模块

本模块定义了这个库的核心部分，一般的使用只需要导入cfg模块即可。

#### opt类及其子类

```
# 配置项模式定义
class oslo_config.cfg.Opt(name, type=None, dest=None, short=None, default=None, positional=False, metavar=None, help=None, secret=False, required=False, deprecated_name=None, deprecated_group=None, deprecated_opts=None, sample_default=None, deprecated_for_removal=False, deprecated_reason=None, deprecated_since=None, mutable=False, advanced=False)
```

配置项模式定义了大量的参数用来控制参数的转换

|参数|说明|备注|
|--------|--------|--------|
|name|配置项名称||
|type|配置项类型|是一个callable对象，将str入参转换为指定类型|
|dest|配置项在配置项对象中的属性名||
|short|命令行短参数| |
|default|默认值||
|positional|||
|metavar|使用--help显示时名称||
|help|帮助说明信息||
|secret|安全特性，不在日志中输出内容||
|required|选项是否必须提供||
|deprecated_name|不建议的名称|为兼容考虑|
|deprecated_opts|不建议的组名||
|deprecated_for_removal|需要移除不建议再使用||
|deprecated_reason|不建议原因||
|deprecated_since|不建议的版本||
|sample_default|简单默认值||
|mutable|选项是否可重载||
|advanced|高级选项，此类选项通常在配置文件的最下端||

Opt的子类，通过传递特定type类型和其他参数更精确的控制。一般配置模式都是使用这些类

|类定义|说明|
|--------|--------|
|StrOpt(name, choices=None, quotes=None, regex=None, ignore_case=None, max_length=None, **kwargs)||
|BoolOpt(name, **kwargs)|转换boolean型参数，命令行参数支持表达形式–optname和–nooptname|
|IntOpt(name, min=None, max=None, **kwargs)|转换int型参数|
|FloatOpt(name, min=None, max=None, **kwargs)|转换float型参数|
|ListOpt(name, item_type=None, bounds=None, **kwargs)|转换list型参数，可以指定item的类型和[]边界|
|DictOpt(name, **kwargs)|转换dict型参数，配置项值是k1:v1,k2:v2形式|
|MultiOpt(name, item_type, **kwargs)|多项时参数，参见下面示例|
|MultiStrOpt(name, **kwargs)|转换多字符串参数|
|IPOpt(name, version=None, **kwargs)|转换ip形式的参数|
|PortOpt(name, min=None, max=None, choices=None, **kwargs)|转换端口形式的参数|
|HostnameOpt(name, **kwargs)|转换主机名形式的参数|
|HostAddressOpt(name, version=None, **kwargs)|转换主机名或IP形式的参数|
|URIOpt(name, max_length=None, schemes=None, **kwargs)|转换URI形式的参数|
|DeprecatedOpt(name, group=None)|不建议的参数，参见下面示例|
|SubCommandOpt(name, dest=None, handler=None, title=None, description=None, help=None)||
|OptGroup(name, title=None, help=None)|定义配置模式中的组|


#### ConfigOpts类

作为主体用来进行一系列操作的类，用来注册配置模式，获取配置项值，管理配置项，初始化或解析配置文件

各种方法

|方法定义|说明|
|--------|--------|
|clear(*args, **kwargs)||
|clear_default(*args, **kwargs)||
|clear_override(*args, **kwargs)||
|reset()||
|find_file(name)||
|mutate_config_files()|重新加载|
|reload_config_files(*args, **kwargs)||
|set_default(*args, **kwargs)|设置默认选项和值|
|set_override(*args, **kwargs)||
|register_cli_opt(*args, **kwargs)|注册命令行选项|
|register_cli_opts(*args, **kwargs)||
|register_group(group)|注册组|
|register_opt(*args, **kwargs)|注册选项|
|register_opts(*args, **kwargs)||
|unregister_opt(*args, **kwargs)|注销选项|
|unregister_opts(*args, **kwargs)||
|import_group(group, module_str)|使用其他模块已定义的配置组|
|import_opt(name, module_str, group=None)||
|list_all_sections()|列出所有section|
|log_opt_values(logger, lvl)|日志输出所有选项值|
|print_help(file=None)|显示帮助信息|
|print_usage(file=None)||

### cfgfilter模块

### generator模块

### types模块

本模块定义了可用的类型，这些类型是向Opt类中传递type时的参数类型。

|类定义|说明|
|--------|--------|
|oslo_config.types.Boolean(type_name='boolean value')|boolean型|
|Dict(value_type=None, bounds=False, type_name='dict value')|dict型|
|Float(min=None, max=None, type_name='floating point value')|float型|
|HostAddress(version=None, type_name='host address value')||
|Hostname(type_name='hostname value')|主机名型|
|IPAddress(version=None, type_name='IP address value')|IP地址型|
|Integer(min=None, max=None, type_name='integer value', choices=None)|整型|
|List(item_type=None, bounds=False, type_name='list value')|list型|
|MultiString(type_name='multi valued')||
|Number(num_type, type_name, min=None, max=None, choices=None)|数值型|
|Port(min=None, max=None, type_name='port', choices=None)|端口型|
|Range(min=None, max=None, inclusive=True, type_name='range value')|范围型|
|String(choices=None, quotes=False, regex=None, ignore_case=False, max_length=None, type_name='string value')|字符串型|
|URI(max_length=None, schemes=None, type_name='uri value')|URI型|

### 杂项

#### CONF全局变量

oslo_config.cfg模块中提供了一个ConfigOpts类实例CONF，提供了全局变量。可以一次初始化被各个模块引用。

```
from oslo_config import cfg

opts = [
    cfg.StrOpt('bind_host', default='0.0.0.0'),
    cfg.PortOpt('bind_port', default=9292),
]

CONF = cfg.CONF
CONF.register_opts(opts)

def start(server, app):
    server.start(app, CONF.bind_port, CONF.bind_host)
```

#### 内置选项

提供了两个默认选项

config_file:表示配置文件列表

默认值为 ~/.project/project.conf,~/project.conf,/etc/project/project.conf,/etc/project.conf

config_dir:表示配置文件目录

默认值为 ~/.project/project.conf.d/,~/project.conf.d/,/etc/project/project.conf.d/,/etc/project.conf.d/


#### 辅助方法find_config_files

oslo_config.cfg.find_config_files(project=None, prog=None, extension='.conf')

根据项目名以上面的默认规则返回配置文件列表。

#### help部分编码规范

配置模式中的help部分有助于生成帮助信息/文档和从代码反向生成配置项。[openstack配置规范](http://docs.openstack.org/draft/config-reference/index.html)

一般遵循如下规则

1.帮助语句首字母大写

2.使用单空格

3.专有名称大写

4.以句号.结尾

5.多行时在行结尾加单空格，不要在行首加空格

6.使用\n在内容中显式换行

#### oslo.config与oslo_config

最新的代码库(M版本开始)应该使用oslo_config作为模块名，原模块名oslo.config不建议使用。原因参见

## 示例

一个非常全的例子
```
# 配置文件
#-*-coding:utf-8-*-
# my.conf

[DEFAULT]
#[DEFAULT]不可省略
enabled_apis = ec2, osapi_keystone, osapi_compute
bind_host = 196.168.1.111
bind_port = 9999

[rabbit]
host = 127.0.0.1
port = 12345
use_ssl=true
user_id = guest
password = guest

# 使用配置的代码段
#-*-coding:utf-8-*-
# config.py
# Author: D. Wang

from oslo.config import cfg
# 声明配置项模式
# 单个配置项模式
enabled_apis_opt = cfg.ListOpt('enabled_apis',
                               default=['ec2', 'osapi_compute'],
                               help='List of APIs to enable by default.')
# 多个配置项组成一个模式
common_opts = [cfg.StrOpt('bind_host',
                          default='0.0.0.0',
                          help='IP address to listen on.'),
               cfg.IntOpt('bind_port',
                          default=9292,
                          help='Port number to listen on.')]
# 配置组
rabbit_group = cfg.OptGroup(name='rabbit', 
                            title='RabbitMQ options'
)
# 配置组中的模式，通常以配置组的名称为前缀（非必须）
rabbit_ssl_opt = cfg.BoolOpt('use_ssl',
                             default=False,
                             help='use ssl for connection') 
# 配置组中的多配置项模式 
rabbit_Opts = [cfg.StrOpt('host',
                          default='localhost',
                          help='IP/hostname to listen on.'),
               cfg.IntOpt('port',
                          default=5672,
                          help='Port number to listen on.')]

# 创建对象CONF，用来充当容器
CONF = cfg.CONF
# 注册单个配置项模式
CONF.register_opt(enabled_apis_opt)
# 注册含有多个配置项的模式
CONF.register_opts(common_opts)
# 配置组必须在其组件被注册前注册！
CONF.register_group(rabbit_group)
# 注册配置组中含有多个配置项的模式，必须指明配置组
CONF.register_opts(rabbit_Opts, rabbit_group)
# 注册配置组中的单配置项模式，指明配置组
CONF.register_opt(rabbit_ssl_opt, rabbit_group)

if __name__ =="__main__":
# 调用容器对象，传入要解析的文件（可以多个） 
　　CONF(default_config_files=['my.conf'])
    
    for i in CONF.enabled_apis:
        print ("DEFAULT.enabled_apis: " + i)
    
    print("DEFAULT.bind_host: " + CONF.bind_host)
    print ("DEFAULT.bind_port: " + str(CONF.bind_port))
    print("rabbit.use_ssl: "+ str(CONF.rabbit.use_ssl))
    print("rabbit.host: " + CONF.rabbit.host)
    print("rabbit.port: " + str(CONF.rabbit.port))
	
# 执行结果	
DEFAULT.enabled_apis: ec2
DEFAULT.enabled_apis: osapi_keystone
DEFAULT.enabled_apis: osapi_compute
DEFAULT.bind_host: 196.168.1.111
DEFAULT.bind_port: 9999
rabbit.use_ssl: True
rabbit.host: 127.0.0.1
rabbit.port: 12345

# 另一个模块，引用前一个模块。读取已定义的配置项
# config_test.py

from config import CONF

if __name__ =="__main__":
#   CONF(default_config_files=['my.conf'])
    CONF()
    for i in CONF.enabled_apis:
        print ("DEFAULT.enabled_apis: " + i)
    
    print("DEFAULT.bind_host: " + CONF.bind_host)
    print ("DEFAULT.bind_port: " + str(CONF.bind_port))
    print("rabbit.use_ssl: "+ str(CONF.rabbit.use_ssl))
    print("rabbit.host: " + CONF.rabbit.host)
    print("rabbit.port: " + str(CONF.rabbit.port))
	
# 和之前的输出差别，这里没有加载配置文件，实际都是默认值
DEFAULT.enabled_apis: ec2
DEFAULT.enabled_apis: osapi_compute
DEFAULT.bind_host: 0.0.0.0
DEFAULT.bind_port: 9292
rabbit.use_ssl: False
rabbit.host: localhost
rabbit.port: 5672
```

基于命令行选项代码和shot参数
```
cli_opts = [cfg.BoolOpt('verbose',
                        short='v',
                        default=False,
                        help='Print more verbose output.'),
            cfg.BoolOpt('debug',
                        short='d',
                        default=False,
                        help='Print debugging output.'),]
# 多选项配置foo
foo_opt = cfg.MultiOpt('foo',
                       item_type=types.Integer(),
                       default=None,
                       help="Multiple foo option")

def add_common_opts(conf):
    conf.register_cli_opts(cli_opts)
    conf.register_cli_opt(foo_opt)

# 将--foo=1 --foo=2 转换为foo=[1,2]
# 当命令行参数需要适配组时，可以使用--group-config1的形式对应	
```

配置组和按组获取配置项
```
rabbit_group = cfg.OptGroup(name='rabbit',
                            title='RabbitMQ options')
rabbit_host_opt = cfg.StrOpt('host',
                             default='localhost',
                             help='IP/hostname to listen on.'),
rabbit_port_opt = cfg.PortOpt('port',
                              default=5672,
                              help='Port number to listen on.')

def register_rabbit_opts(conf):
    conf.register_group(rabbit_group)
    # options can be registered under a group in either of these ways:
    conf.register_opt(rabbit_host_opt, group=rabbit_group)
    # 还可以直接传递组名，没有组名的参数都属于DEFAULT
    conf.register_opt(rabbit_port_opt, group='rabbit')

# 以对象属性的方式获取配置项值	
host = conf.rabbit.host
port = conf.rabbit.port
```

魔术转换
```
opts = [
    cfg.StrOpt('state_path',
               default=os.path.join(os.path.dirname(__file__), '../'),
               help='Top-level directory for maintaining nova state.'),
    cfg.StrOpt('sqlite_db',
               default='nova.sqlite',
               help='File name for SQLite.'),
    # 一个配置项由其他配置项组合而成
    cfg.StrOpt('sql_connection',
               default='sqlite:///$state_path/$sqlite_db',
               help='Connection string for SQL database.'),
]
# 使用$$防止转换，带组的形式${mygroup.myopt}
```

不建议的配置项
```
conf = cfg.ConfigOpts()
opt_1 = cfg.StrOpt('opt_1', default='foo', deprecated_name='opt1')
opt_2 = cfg.StrOpt('opt_2', default='spam', deprecated_group='DEFAULT')
opt_3 = cfg.BoolOpt('opt_3', default=False, deprecated_for_removal=True)

conf.register_opt(opt_1, group='group_1')
conf.register_opt(opt_2, group='group_2')
conf.register_opt(opt_3)

conf(['--config-file', 'config.conf'])

# 实际加载配置项时，日志输出会提示不建议的配置项信息
[group_1]
opt1 = bar

[DEFAULT]
opt_2 = eggs
opt_3 = True
```