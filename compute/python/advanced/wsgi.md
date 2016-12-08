# WSGI -- Web Server Gateway Interface


## 基本概念

### 简介

WSGI不是web服务器，也不是用于与程序交互的API，而只是定义的一个接口规范。
其目标是在web服务器和web框架层之间提供一个通用的API标准，减少之间的互操作性并形成统一的调用方式。

几个重要的规范参考PEP333,PEP3333,PEP444

### WSGI服务器

服务器和应用之间传递两个固定参数，一个是含有服务器环境变量的字典。另一个是可调用对象，这个对象使用HTTP状态码
和返回给客户端的HTTP头来初始化响应，这个可调用对象必须返回一个可迭代对象。

 - 参考服务器调用app

```
# 标准库中的参考WSGI服务器实现
from wsgiref.simple_server import make_server

# 调用了app
httpd = make_server('', 8000, simple_wsgi_app)
print "start app serving on port 8000..."
httpd.serve_forever()
```

### APP应用

根据WSGI定义，其应用是一个可调用对象(python中的方法？)。

 - 一个app示例
 
```
def simple_wsgi_app(environ, start_respose):
    status = '200 OK'
	headers = [('Content-type', 'text/plain')]
	start_response(status, headers)
	return ['Hello World']
```

### middleware中间件

在某些情况下，除了app需要执行，在app执行前或后都可以添加一些处理程序，这些中间件在web服务器和web应用之间增加了额外功能。

预处理的动作可以是拦截，修改，添加，鉴权，修改环境变量，转发或重定向，根据URL路径分派应用等。

后期处理可以包括输出格式调整，增加时间戳，日志统计等等。
