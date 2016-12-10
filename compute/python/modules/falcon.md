# falcon

参考 [falcon Documentation](http://falcon.readthedocs.io/en/stable/)



## 简介

Falcon -- Falcon is a minimalist WSGI library for building speedy web APIs and app backends. 

Falcon是一个构建云API的高性能Python框架，它鼓励使用REST架构风格，尽可能以最少的力气做最多的事情。

### 基本特性

 - 通过 URI 模板和资源类可直观的了解路由信息
 - 轻松访问请求和响应类来访问 header 和 body 信息
 - 通过方便的异常类实现对 HTTP 错误响应的处理
 - 通过全局、资源和方法钩子实现 DRY 请求处理
 - 通过 WSGI helper 和 mock 实现单元测试
 - 使用 Cython 可提升 20% 的速度
 - 支持 Python 2.6, Python 2.7, PyPy 和 Python 3.3/3.4
 - 高性能！！！

## 教程

此教程以创建一个图像共享app为例，介绍了falcon提供的功能。

### 第一步

创建一个app。这个对象实现了__call__方法，所以是可调用对象。

```
import falcon

api = application = falcon.API()

# 再看下call方法，是符合WSGI规范的。
>>> help(falcon.API.__call__)
Help on method __call__ in module falcon.api:

__call__(...) unbound falcon.api.API method
    WSGI `app` method.
    
    Makes instances of API callable from a WSGI server. May be used to
    host an API or called directly in order to simulate requests when
    testing the API.
    
    See also PEP 3333.
    
    Args:
        env (dict): A WSGI environment dictionary
        start_response (callable): A WSGI helper function for setting
            status and headers on a response.

>>> 
```

### 托管应用

将WSGI服务器和APP关联起来。

```
app = falcon.API(before=[auth, check_media_type])

# 在本地8000端口启动了一个web服务。
if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
```

### 创建资源

Falcon从REST架构风格引入了一些术语，如果你熟悉REST概念，那么对Falcon应该会比较熟悉。不过，就算完全不懂REST，也不用担心。Falcon的设计理念是，尽可能直观地让所有人理解HTTP基本原理。

在Falcon中，我们可以把传入的请求(incoming requests)称为资源(Resources)。

资源只是一个常规class，包含一些遵循一定命名规则的方法(method)。每个方法对应一个动作(API客户端为了获取或转换资源，去请求执行的动作)

```
import falcon

class Resource(object):

    # 当发生对应资源的GET请求时将执行的动作
    def on_get(self, req, resp):
        # 默认将application/json作为mimetype。可以设置成任何你想使用的类型
        resp.body = '{"message":"Hello woeld!"}'
        resp.status = falcon.HTTP_200

api = application = falcon.API()

# 将资源和路由对应
images = images.Resource()
api.add_route('/images', images)
```

此处定义了单一方法on_get。对于resource想要支持的任何HTTP方法，只需要简单在resource上加on_x类方法(class method)，x可以是标准HTTP方法中的任何一个，例如on_get,on_put,on_head(小写)等等。

我们将这些方法称作responders(响应器)。每个responder至少需要两个参数，一个代表HTTP请求，另一个代表对应请求的HTTP响应。
根据习惯，我们一般写作req和resp。route(路由)模板和hooks(钩子)可以添加一些额外的参数。

### 请求对象和响应对象

前面说到responders(响应器)有两个重要的参数。具体可以参考API

falcon.Requst请求对象代表了请求相关的信息，可以用来获取headers，查询参数和请求body等。

falcon.Response应答对象代表了业务处理进行应答的结果。可以用来设置HTTP状态码，headers和响应body等。

```
# 对一个资源的post请求进行处理
def on_post(self, req, resp):
    # 从req中获取相关内容
    image_id = str(uuid.uuid4())
    ext = req.content_type[6:]
    filename = image_id + '.' + ext

    image_path = os.path.join(self.storage_path, filename)
    # 将上传的图像文件保存
    with open(image_path, 'wb') as image_file:
        while True:
            chunk  = req.stream.read(4096)
            if not chunk:
                break

            image_file.write(chunk)

    # 设置应答
    resp.status = falcon.HTTP_201
    resp.location = '/images/' + image_id
```

### 显示图片

之前实现了图片的post和保存，现在需要将图片显示给用户。

```
def on_get(self, req, resp, name):
    ext = os.path.splitext(name)[1][1:]
    # 设置header类型
    resp.content_type = _ext_to_media_type(ext)

    # 打开文件，以流的方式输出
    image_path = os.path.join(self.storage_path, name)
    resp.stream = open(image_path, 'rb')
    resp.stream_len = os.path.getsize(image_path)
	
# 新定义的路由，将name作为参数传递给on_get响应器
api.add_route('/images/(name)', image)
```

### 钩子(hooks)介绍

这里的钩子是WSGI规范中的middleware。用来在正式的响应器前或后进行附加的处理动作。

例如在处理post前需要检查上传文件的格式是否有效

```
ALLOWED_IMAGE_TYPES = (
    'image/gif',
    'image/jpeg',
    'image/png',
)

# 钩子方法，用来检查输入
# 必须使用三个参数，params参数，可以在此中添加额外的设置传递其他参数给响应器。
def validate_image_type(req, resp, params):
    if req.content_type not in ALLOWED_IMAGE_TYPES:
        msg = 'Image type not allowed. Must be PNG, JPEG, or GIF'
        raise falcon.HTTPBadRequest('Bad request', msg)

# 以装饰器的方式加了钩子
@falcon.before(validate_image_type)
def on_post(self, req, resp):		
```

在API类初始化时将钩子作为参数传递进去，我们可以全局应用:

```
falcon.API(before=[extract_project_id])
```

### 错误处理

通常来讲，Falcon假定资源的响应器(on_get,on_post等)在大部分情况下能正确运作。也就是说，Falcon在保护响应器代码上没有做太多工作。

因此需要应用编写符合一定的原则：

1.资源响应器将响应变量设置为完整值

2.大部分代码易于测试

3.错误应该是可预见、易查明，并且能在每个响应器中做作相应处理。

大多数情况下，碰到简单或轻度的错误。我们可以手工设置错误状态，合适的响应headers和resp中的body内容。

还可以抛出httperror相关的异常，让falcon自己捕获并适配错误响应。

```
# 在文件不存在时，抛出404
try:
    resp.stream = open(image_path, 'rb')
except IOError:
    raise falcon.HTTPNotFound()
```


## 示例

```
import json
import logging
import uuid
from wsgiref import simple_server

import falcon
import requests


class StorageEngine(object):

    def get_things(self, marker, limit):
        return [{'id': str(uuid.uuid4()), 'color': 'green'}]

    def add_thing(self, thing):
        thing['id'] = str(uuid.uuid4())
        return thing


class StorageError(Exception):

    @staticmethod
    def handle(ex, req, resp, params):
        description = ('Sorry, couldn\'t write your thing to the '
                       'database. It worked on my box.')

        raise falcon.HTTPError(falcon.HTTP_725,
                               'Database Error',
                               description)


class SinkAdapter(object):

    engines = {
        'ddg': 'https://duckduckgo.com',
        'y': 'https://search.yahoo.com/search',
    }

    def __call__(self, req, resp, engine):
        url = self.engines[engine]
        params = {'q': req.get_param('q', True)}
        result = requests.get(url, params=params)

        resp.status = str(result.status_code) + ' ' + result.reason
        resp.content_type = result.headers['content-type']
        resp.body = result.text


class AuthMiddleware(object):

    def process_request(self, req, resp):
        token = req.get_header('Authorization')
        account_id = req.get_header('Account-ID')

        challenges = ['Token type="Fernet"']

        if token is None:
            description = ('Please provide an auth token '
                           'as part of the request.')

            raise falcon.HTTPUnauthorized('Auth token required',
                                          description,
                                          challenges,
                                          href='http://docs.example.com/auth')

        if not self._token_is_valid(token, account_id):
            description = ('The provided auth token is not valid. '
                           'Please request a new token and try again.')

            raise falcon.HTTPUnauthorized('Authentication required',
                                          description,
                                          challenges,
                                          href='http://docs.example.com/auth')

    def _token_is_valid(self, token, account_id):
        return True  # Suuuuuure it's valid...


class RequireJSON(object):

    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
                href='http://docs.examples.com/api/json')

        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                    href='http://docs.examples.com/api/json')


class JSONTranslator(object):

    def process_request(self, req, resp):
        # req.stream corresponds to the WSGI wsgi.input environ variable,
        # and allows you to read bytes from the request body.
        #
        # See also: PEP 3333
        if req.content_length in (None, 0):
            # Nothing to do
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

        try:
            req.context['doc'] = json.loads(body.decode('utf-8'))

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

    def process_response(self, req, resp, resource):
        if 'result' not in req.context:
            return

        resp.body = json.dumps(req.context['result'])


def max_body(limit):

    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = ('The size of the request is too large. The body must not '
                   'exceed ' + str(limit) + ' bytes in length.')

            raise falcon.HTTPRequestEntityTooLarge(
                'Request body is too large', msg)

    return hook


class ThingsResource(object):

    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp, user_id):
        marker = req.get_param('marker') or ''
        limit = req.get_param_as_int('limit') or 50

        try:
            result = self.db.get_things(marker, limit)
        except Exception as ex:
            self.logger.error(ex)

            description = ('Aliens have attacked our base! We will '
                           'be back as soon as we fight them off. '
                           'We appreciate your patience.')

            raise falcon.HTTPServiceUnavailable(
                'Service Outage',
                description,
                30)

        # An alternative way of doing DRY serialization would be to
        # create a custom class that inherits from falcon.Request. This
        # class could, for example, have an additional 'doc' property
        # that would serialize to JSON under the covers.
        req.context['result'] = result

        resp.set_header('Powered-By', 'Falcon')
        resp.status = falcon.HTTP_200

    @falcon.before(max_body(64 * 1024))
    def on_post(self, req, resp, user_id):
        try:
            doc = req.context['doc']
        except KeyError:
            raise falcon.HTTPBadRequest(
                'Missing thing',
                'A thing must be submitted in the request body.')

        proper_thing = self.db.add_thing(doc)

        resp.status = falcon.HTTP_201
        resp.location = '/%s/things/%s' % (user_id, proper_thing['id'])


# Configure your WSGI server to load "things.app" (app is a WSGI callable)
app = falcon.API(middleware=[
    AuthMiddleware(),
    RequireJSON(),
    JSONTranslator(),
])

db = StorageEngine()
things = ThingsResource(db)
app.add_route('/{user_id}/things', things)

# If a responder ever raised an instance of StorageError, pass control to
# the given handler.
app.add_error_handler(StorageError, StorageError.handle)

# Proxy some things to another service; this example shows how you might
# send parts of an API off to a legacy system that hasn't been upgraded
# yet, or perhaps is a single cluster that all data centers have to share.
sink = SinkAdapter()
app.add_sink(sink, r'/search/(?P<engine>ddg|y)\Z')

# Useful for debugging problems in your API; works with pdb.set_trace(). You
# can also use Gunicorn to host your app. Gunicorn can be configured to
# auto-restart workers when it detects a code change, and it also works
# with pdb.
if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
```
