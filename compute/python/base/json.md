# json

## 基本概念
JSON(JavaScript Object Notation)javascript对象表示法。是一种轻量级的数据交换格式，与XML相比是一种更易读的结构化数据表达方式。
更多信息可以访问[http://json.org](http://json.org)

json库是从2.6开始新增的模块，提供了与marshal和pickle模块相似的对外接口。

JSON 是YAML 1.2 的一个子集。通过此模块的默认设置 （尤其是，默认分隔符值） 生成的 JSON 也是一个子集的 YAML 1.0 和 1.1。此模块，因而也可用作 YAML 的序列化程序。

### json和python对象转换表

json作为对外提供的数据格式和python对象本身有部分差异。如果一个字典的键有非字符串形式的，转换为json再转为dic将和原来不一样。

| json   | python2 | python3|
|--------|---------|--------|
|object  | dict    | dict   |
|array   | list tuple| list tuple|
|string  | unicode | str    |
|number(int)| int,long| int |
|number(real)| float| float |
|true    | True    | True   |
|false   | False   | False  |
|null    | None    | None   |

```
# 看一段格式对比
BOOKS={
    '111111': {
	    'title': 'core aaabbbb',
		'edition': 2,
		'year': 2007,
	},
	'222222': {
	    'title': 'python fundamental',
		'authors': ['Jack', 'Paul', 'Wesley'],
	},
}

printf('\n*************')
printf(BOOKS)

printf('\n*************')
pprint(BOOKS)

printf('\n*************')
printf(dumps(BOOKS))

printf('\n*************')
printf(dumps(BOOKS, indent=4))

# 实际输出
# 注意细节上的差异，json的字符串都是""，并且没有字典，元组最后的,
*************
{'111111': {'edition': 2, 'year': 2007, 'title': 'core aaabbbb'}, '222222': {'authors': ['Jack', 'Paul', 'Wesley'], 'title': 'python fundamental'}}

*************
{'111111': {'edition': 2, 'title': 'core aaabbbb', 'year': 2007},
 '222222': {'authors': ['Jack', 'Paul', 'Wesley'],
            'title': 'python fundamental'}}

*************
{"111111": {"edition": 2, "year": 2007, "title": "core aaabbbb"}, "222222": {"authors": ["Jack", "Paul", "Wesley"], "title": "python fundamental"}}

*************
{
    "111111": {
        "edition": 2, 
        "year": 2007, 
        "title": "core aaabbbb"
    }, 
    "222222": {
        "authors": [
            "Jack", 
            "Paul", 
            "Wesley"
        ], 
        "title": "python fundamental"
    }
}
```
### 模块级方法

1. dump根据转换表将一个对象序列化为json格式流输出到fp

json.dump(obj, fp, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, encoding="utf-8", default=None, sort_keys=False, **kw) 

| 参数 |说明|
|--------|--------|
|obj|要转换的对象|
|fp| 支持.write()操作的类文件对象|
|skipkeys|为true时非基本类型的关键字将被跳过，否则抛出typeerror|
|ensure_ascii|使用非ascii字符|
|check_circular|false时容器类型循环引用检查将关闭|
|allow_nan||
|cls|使用指定的encoder，参考下面的JSONEncoder|
|indent|输出缩进，一般使用4|
|separators|使用元组(item_separator, dict_separator)作为分割符参数 (', ', '：')是最紧凑的 JSON 表示|
|encoding|编码，默认是UTF-8|
|default|obj默认函数default(obj)，用来返回序列化内容|
|sort_keys|按关键字排序后输出|
|kw|配合cls使用|

2. dumps根据转换表将一个对象序列化为json格式字符串str

json.dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, encoding="utf-8", default=None, sort_keys=False, **kw) 

3. load从fp读取json格式内容反序列化到python对象

json.load(fp[, encoding[, cls[, object_hook[, parse_float[, parse_int[, parse_constant[, object_pairs_hook[, **kw]]]]]]]])
| 参数 |说明|
|--------|--------|
|fp| 支持.read()操作的类文件对象|
|encoding|编码，默认是UTF-8||
|cls|使用指定的decoder，参考下面的JSONDecoder|
|object_hook|用于实现自定义的解码器，见下面示例|
|parse_float|默认使用float(num_str)，可以指定某种方法。见下面示例|
|parse_int|默认使用int(num_str)，可以指定方法|
|parse_constant|对常量的指定转换方法|
|object_pairs_hook|比object_hook有更高优先级|
|kw|配合cls使用，传递更多参数|

4.loads将str或unicode字符串对象反序列化到python对象

json.loads(s[, encoding[, cls[, object_hook[, parse_float[, parse_int[, parse_constant[, object_pairs_hook[, **kw]]]]]]]])

### Encoders和Decoders类

#### encoders

class json.JSONDecoder([encoding[, object_hook[, parse_float[, parse_int[, parse_constant[, strict[, object_pairs_hook]]]]]]])

#### decoders

class json.JSONEncoder([skipkeys[, ensure_ascii[, check_circular[, allow_nan[, sort_keys[, indent[, separators[, encoding[, default]]]]]]]]])


### 标准兼容

#### Character Encodings

#### Top-level Non-Object, Non-Array Values

#### Infinite and NaN Number Values

#### Repeated Names Within an Object

## 示例

- 将python对象转为json格式内容

```
>>> json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
'["foo", {"bar": ["baz", null, 1.0, 2]}]'
>>> print json.dumps("\"foo\bar")
"\"foo\bar"
>>> print json.dumps(u'\u1234')
"\u1234"
>>> print json.dumps('\\')
"\\"
>>> print json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True)
{"a": 0, "b": 0, "c": 0}
>>> from StringIO import StringIO
>>> io = StringIO()
>>> json.dump(['streaming API'], io)
>>> io.getvalue()
'["streaming API"]'
>>> print json.dumps({'4':   5, '6': 7}, sort_keys=True,indent=4, separators=(',', ': '))
{
    "4": 5,
    "6": 7
}
```

- 将json格式转换为python对象

```
>>> def as_complex(dct):
...     if '__complex__' in dct:
...         return complex(dct['real'], dct['imag'])
...     return dct
...
>>> json.loads('{"__complex__": true, "real": 1, "imag": 2}',
...     object_hook=as_complex)
(1+2j)
>>> import decimal
>>> json.loads('1.1', parse_float=decimal.Decimal)
Decimal('1.1')
```

- 实现自定义的encoder

```
>>> import json
>>> class ComplexEncoder(json.JSONEncoder):
...     def default(self, obj):
...         if isinstance(obj, complex):
...             return [obj.real, obj.imag]
...         # Let the base class default method raise the TypeError
...         return json.JSONEncoder.default(self, obj)
...
>>> dumps(2 + 1j, cls=ComplexEncoder)
'[2.0, 1.0]'
>>> ComplexEncoder().encode(2 + 1j)
'[2.0, 1.0]'
>>> list(ComplexEncoder().iterencode(2 + 1j))
['[', '2.0', ', ', '1.0', ']']
```
