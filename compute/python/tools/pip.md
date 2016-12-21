# pip

## [官方文档](https://pip.pypa.io/en/stable/)

### 安装

从2.7.9版本或3.4版本开始，python安装里默认的带了pip。低版本的还需要手工安装。
安装完pip后，还会附带安装wheel和setuptools

安装pip

```
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```

安装中支持多种参数

--no-setuptools，不安装setuptools

--no-wheel，不安装wheel

### 基本使用

1.安装，升级，卸载包

从默认源安装指定包
```
$ pip install SomePackage          # latest version
$ pip install SomePackage==1.0.4   # specific version
$ pip install 'SomePackage>=1.0.4' # minimum version
```

卸载包
```
pip uninstall SomePackage
```

升级包
```
pip install -U somepackage
pip install --upgrade package
```

2.显示和查询包

显示当前包

```
$ pip list
docutils (0.9.1)
Jinja2 (2.6)
Pygments (1.5)
Sphinx (1.1.2)
# 显示过期包及最新版本
$ pip list --outdated
docutils (Current: 0.9.1 Latest: 0.10)
Sphinx (Current: 1.1.2 Latest: 1.1.3)
```

显示包详细信息
```
$ pip show sphinx
---
Name: Sphinx
Version: 1.1.3
Location: /my/env/lib/pythonx.x/site-packages
Requires: Pygments, Jinja2, docutils
```

查询包
```
pip search 'pelican'
```

3.从wheel或本地安装

wheel是一种编译归档过的文件，相比从源码下载编译安装具有更快的安装优势。
默认情况下pip优先使用wheel文件，如果安装时使用了--no-binary参数则不会安装。

从wheel文件直接安装
```
pip install SomePackage-1.0-py2.py3-none-any.whl
```

制作wheel包，再从本地安装
```
pip install wheel
pip wheel --wheel-dir=/local/wheels -r requirements.txt
pip install --no-index --find-links=/local/wheels -r requirements.txt
```

某些情况下安装包是本地文件，可以从本地安装

```
# 下载安装包
$ pip install --download DIR -r requirements.txt
# 首先检查wheel缓存，然后从本地路径安装
$ pip install --no-index --find-links=DIR -r requirements.txt
```

4.requirements，constraints文件

requirements文件遵循一定的格式，一般每行指定一个需要安装的包名称和版本。

通过req文件能较好的解决版本冲突问题，req文件常用的场景包括：

从req文件安装包
```
pip install -r requirements.txt
```

将当前包版本信息导出，以便在其他地方重建
```
pip freeze > requirements.txt
```

constraints文件的文法和内容与req文件类似，但这个文件只是用来控制安装的版本而不是进行安装。


### 配置文件和环境变量

pip允许通过ini风格的配置文件来设置通用的命令参数，从使用范围可以区分为用户，虚拟环境，整站点三个级别。
配置文件优先级上最低是站点，然后用户较高，最后虚环境的覆盖前面的。环境变量的高于文件，命令行参数优先级最高。

1.per-user

```
linux:
$HOME/.config/pip/pip.conf，可以通过XDG_CONFIG_HOME指定config目录？
$HOME/.pip/pip.conf 这是早期的路径
win:
%APPDATA%\pip\pip.ini
%HOME%\pip\pip.ini
```

2.virtualenv

```
linux:
$VIRTUAL_ENV/pip.conf
win:
%VIRTUAL_ENV%\pip.ini
```

3.sitewider

```
linux:
/etc/pip.conf，或者XDG_CONFIG_DIRS指定的目录下的pip目录
win:
C:\ProgramData\pip\pip.ini,
C:\Documents and Settings\All Users\Application Data\pip\pip.ini(XP系统)
```

4.命令行下可选的参数都可以作为配置项，每个子命令可以单独作为一个section，子命令的选项覆盖global的选项

```
[global]
timeout = 60

[freeze]
timeout = 10

# 布尔型参数和一个参数多行值的例子
[install]
no-compile = no
find-links =
    http://mirror1.example.com
    http://mirror2.example.com
```

5.环境变量

命令行参数可以通过环境变量的方式传递，变量名称参照PIP_<UPPER_LONG_NAME>，参数的-需要转换为_表示。

```
export PIP_FIND_LINKS="http://mirror1.example.com http://mirror2.example.com"
```

### 用户模式

### req文件格式

基本格式规范
```
[[--option]...]
<requirement specifier> [; markers] [[--option]...]
<archive url/path>
[-e] <local project path>
[-e] <vcs project url>

# 可选参数包括
-i, --index-url
--extra-index-url
--no-index
-f, --find-links
--no-binary
--only-binary
--require-hashes
```

```
#
####### example-requirements.txt #######
#
###### Requirements without Version Specifiers ######
nose
nose-cov
beautifulsoup4
#
###### Requirements with Version Specifiers ######
#   See https://www.python.org/dev/peps/pep-0440/#version-specifiers
docopt == 0.6.1             # Version Matching. Must be version 0.6.1
keyring >= 4.1.1            # Minimum version 4.1.1
coverage != 3.5             # Version Exclusion. Anything except version 3.5
Mopidy-Dirble ~= 1.1        # Compatible release. Same as >= 1.1, == 1.*
#
###### Refer to other requirements files ######
-r other-requirements.txt
#
#
###### A particular file ######
./downloads/numpy-1.9.2-cp34-none-win32.whl
http://wxpython.org/Phoenix/snapshot-builds/wxPython_Phoenix-3.0.3.dev1820+49a8884-cp34-none-win_amd64.whl
#
###### Additional Requirements without Version Specifiers ######
#   Same as 1st section, just here to show that you can put things in any order.
rejected
green
#
```