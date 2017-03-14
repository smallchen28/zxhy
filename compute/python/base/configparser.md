# configparser

## 基本概念
配置文件解析器，提供了一系列解析类似INI配置文件的方法和类。

基本的配置文件由段组成，每个段有[section]开头，后续有key:value或key=value这样形式的实际内容。以#或;进行注释

## 模块使用

### RawConfigParser 基本配置对象

class ConfigParser.RawConfigParser([defaults[, dict_type[, allow_no_value]]]) 

构建一个基本的配置解析对象，使用默认的内部字典(collections.OrderedDict)保存配置内容，可以指定字典类型，指定默认值，指定是否允许没有value的key。

#### 对象方法

| 对象方法 | 说明 | 其他|
|--------|---------|--------|
|defaults()|返回默认的内部字典？||
|sections()|返回section名称的list|不包含default段|
|add_section(section)|增加段名称|如果名称已存在抛出异常，不能传入default|
|has_section(section)|判断段名称是否存在|不处理default|
|options(section)|返回某段的所有选项名称list||
|has_option(section, option)|判断指定段和选项是否存在||
|read(filenames)|尝试打开一个文件名list，返回转换成功的文件名list|无法打开的文件会被忽略|
|readfp(fp[, filename])|||
|get(section, option)|获取值||
|getint(section, option)|获取int值||
|getfloat(section, option)|获取float值||
|getboolean(section, option)|获boolean取值||
|items(section)|返回某段的包含键值对的dict||
|set(section, option, value)|设置值||
|write(fileobject)|写配置文件||
|remove_option(section, option)|移除选项||
|remove_section(section)|移除段||
|set(section, option, value)|设置值||

### ConfigParser 衍生配置对象

class ConfigParser.ConfigParser([defaults[, dict_type[, allow_no_value]]])

在上一层的基础上实现了魔术转换特性和get/items方法的可选参数

魔术转换是指值可以包含引用其他同一节中的值或在[default]节中的格式字符串。

```
[My Section]
foodir: %(dir)s/whatever
dir=frob
long: this value continues
   in the next line
```

#### 对象方法

| 对象方法 | 说明 | 其他|
|--------|---------|--------|
|get(section, option[, raw[, vars]])|可增加默认值的get|参看下面示例|
|items(section[, raw[, vars]])|可增加默认值的items||

### SafeConfigParser 安全配置对象

在上一层的基础上实现了更合理的魔术转换特性。

#### 对象方法

| 对象方法 | 说明 | 其他|
|--------|---------|--------|
|set(section, option, value)|设置值，必须是str/unicode||

## 示例

生成配置文件
```
import ConfigParser
config = ConfigParser.RawConfigParser()
config.add_section('Section1')
config.set('Section1', 'an_int', '15')
config.set('Section1', 'a_bool', 'true')
config.set('Section1', 'a_float', '3.1415')
config.set('Section1', 'baz', 'fun')
config.set('Section1', 'bar', 'Python')
config.set('Section1', 'foo', '%(bar)s is %(baz)s!')
# Writing our configuration file to 'example.cfg'
with open('example.cfg', 'wb') as configfile:
    config.write(configfile)
```

读取配置
```
>>> import ConfigParser
>>> rconf = ConfigParser.RawConfigParser()
>>> rconf.read('example.cfg')
['example.cfg']
>>> print rconf.getint('Section1', 'an_int')
15
>>> print rconf.get('Section1','foo')
%(bar)s is %(baz)s!
# 要支持魔术转换必须使用configparse或safe
>>> conf = ConfigParser.ConfigParser()
>>> conf.read('example.cfg')
['example.cfg']
>>> print conf.get('Section1','foo', 1)
%(bar)s is %(baz)s!
>>> print conf.get('Section1','foo', 0)
Python is fun!
>>> print conf.get('Section1','foo')
Python is fun!
>>> print conf.get('Section1','foo', 0, {'bar':'java'})
java is fun!
```

默认设置
```
# New instance with 'bar' and 'baz' defaulting to 'Life' and 'hard' each
config = ConfigParser.SafeConfigParser({'bar': 'Life', 'baz': 'hard'})
config.read('example.cfg')

print config.get('Section1', 'foo') # -> "Python is fun!"
config.remove_option('Section1', 'bar')
config.remove_option('Section1', 'baz')
print config.get('Section1', 'foo') # -> "Life is hard!"
```

allow_no_value参数和readfp
```
>>> import ConfigParser
>>> import io

>>> sample_config = """
... [mysqld]
... user = mysql
... pid-file = /var/run/mysqld/mysqld.pid
... skip-external-locking
... """
>>> config = ConfigParser.RawConfigParser(allow_no_value=True)
>>> config.readfp(io.BytesIO(sample_config))

>>> # Settings with values are treated as before:
>>> config.get("mysqld", "user")
'mysql'

>>> # Settings without values provide None:
>>> config.get("mysqld", "skip-bdb")

>>> # Settings which aren't specified still raise an error:
>>> config.get("mysqld", "does-not-exist")
Traceback (most recent call last):
```