# tox

## [官方文档](http://tox.readthedocs.io/en/latest/)

## 简介

tox的目标是用来自动化和标准化python软件测试。更大的目标是作为简化打包，测试，分发python软件工具

当前特性包括

- 自动化测试和统一的输出。

- 对测试环境的定制化和虚拟化，适配多种测试框架。

- 跨操作系统平台和跨python版本的。

- 与第三方工具的良好的交互性，例如jenkins,devpi。

- 简单的INI风格配置文件。

- 2.0版本开始支持插件丰富功能。


## 配置与使用

### 基本用法

- 最简单的示例

```
# content of: tox.ini , put in same dir as setup.py
[tox]
envlist = py26,py27
[testenv]
deps=pytest # or 'nose' or ...
commands=py.test  # or 'nosetests' or ...
```
envlist指定了产生两个虚拟环境，通过tox -e py27的命令指定运行某个虚拟环境测试。不带参数则运行全部

- 指定平台

platform = linux2|win32，正则表达式适配平台名称。如果通过sys.platform和这个平台不匹配则不运行测试。

- 非虚拟环境命令白名单

当需要运行某些独立于虚拟环境的命令时，可以使用白名单
```
[testenv]
whitelist_externals = make
                      /bin/bash
```

- 导入requirement

deps = -rrequirements.txt，在虚拟环境执行pip命令时根据requirements文件导入依赖包。

- 使用不同的PyPI源

可以通过命令行参数或配置项指定pypi源
```
tox -i http://pypi.my-alternative-index.org

[tox]
indexserver =
    default = http://pypi.my-alternative-index.org
```
更复杂的用法，分别指定多个源
```
[tox]
indexserver =
    DEV = http://mypypiserver.org

[testenv]
deps =
    docutils        # comes from standard PyPI
    :DEV:mypackage  # will be installed from custom "DEV" pypi url
```

- 安装第三方包时的定制

默认情况下tox使用pip安装包，如果需要使用其他命令或带更多参数，可以指定
```
[testenv]
install_command = easy_install {opts} {packages}
[testenv]
install_command = pip install --pre --find-links http://packages.example.com --no-index {opts} {packages}
```

- 重建虚拟环境

tox --recreate -e py27。通常情况下运行过一次后，虚拟环境将一直存在。可以通过命令重建虚拟环境。

- 传递和设置环境变量

默认情况下只传递PATH环境变量，如果需要传递更多环境变量需要如下设置
```
[testenv]
passenv = LANG
```
还可以指定当前测试用例需要的环境变量
```
[testenv]
setenv =
    PYTHONPATH = {toxinidir}/subdir
```

- 忽略命令返回
某些情况下需要忽略一些命令的返回值，使用-前缀在命令前可以忽略此行命令的返回
```
[testenv:py27]
commands = coverage erase
       {envbindir}/python setup.py develop
       coverage run -p setup.py test
       coverage combine
       - coverage html
       {envbindir}/flake8 loads
```

- 虚拟环境不使用链接
默认情况下，虚拟环境使用软连接指向python的系统文件，模块等。使用–always-copy创建虚拟环境。
```
[testenv]
alwayscopy = True
```

### 一些技巧

- 交互传递更多参数
调用tox命令时，可以传递更多参数给实际底层名
```
tox -- -x tests/test_something.py
此时--后面的参数被截取传递到{posargs}
# in the testenv or testenv:NAME section of your tox.ini
commands =
    py.test {posargs}
指定了默认的posargs参数，当没有传递时使用默认值
commands =
    nosetests {posargs:--with-coverage}
```

- 集成sphinx

- 避免sdist

### 多种测试框架

- pytest

- unitest2,discover

- nose

### 与jenkins的集成


