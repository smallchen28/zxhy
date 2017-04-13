# pelican一个静态网站生成工具

## 简介

pelican是一个Python编写的静态网站生成工具，支持如下一些特性

- 支持将reStructuredText或Markdown格式文档转换为HTML网页

- 包括简单的命令行工具生成和发布网站

- 支持通过版本工具和网站管理内容，支持WORDPRESS等数据导入。

- 支持主题，评论，ATOM/RSS，代码段高亮，国际化等。

**pelican名称是来源于法语中记事本的单词calepin**

### 官方网站

[官方BLOG](https://blog.getpelican.com/)

[源代码](https://github.com/getpelican/pelican)

[官方文档](http://docs.getpelican.com/en/3.7.1/)

[主题下载](https://github.com/getpelican/pelican-themes)

[主题展示](http://www.pelicanthemes.com )

[插件下载](https://github.com/getpelican/pelican-plugins)

## 快速教程

### 安装相关模块

创建虚拟环境，通过pip安装模块

```
[root@db1 ~]# virtualenv myblog
New python executable in /root/myblog/bin/python
Please make sure you remove any previous custom paths from your /root/.pydistutils.cfg file.
Installing setuptools, pip, wheel...done.

(myblog) [root@db1 ~]# pip install pelican markdown tzlocal typogrify
```

### 初始目录

通过quickstart初始化目录

```
[root@db1 ~]# pelican-quickstart

#最终在当前目录下产生项目所有文件
(myblog) [root@db1 myweb]# ll
total 40
drwxr-xr-x 4 root root 4096 Apr 12 15:00 content #写的内容放这里
-rwxr-xr-x 1 root root 2224 Apr 11 17:19 develop_server.sh #部署用脚本
-rw-r--r-- 1 root root 2439 Apr 11 17:19 fabfile.py #部署用
-rw-r--r-- 1 root root 4370 Apr 11 17:19 Makefile #部署用
drwxr-xr-x 7 root root 4096 Apr 12 15:03 output #生成的静态文件
-rwxr--r-- 1 root root 1158 Apr 12 14:59 pelicanconf.py #配置文件
-rw-r--r-- 1 root root  508 Apr 11 17:19 publishconf.py #部署用
drwxr-xr-x 3 root root 4096 Apr 12 14:51 themes #主题
```

### 生成内容

将content中内容转化为静态html
```
(myblog) [root@db1 myweb]# pelican content
Done: Processed 2 articles, 0 drafts, 0 pages and 0 hidden pages in 0.36 seconds.
(myblog) [root@db1 myweb]# 
```

### 测试运行

启动python的http服务
```
cd ~/projects/yoursite/output
python -m pelican.server
```

可以通过浏览器看到了哦

![](http://)

### 站点部署

可以通过pelican的-s参数指定依赖的配置文件。默认提供了pelicanconf和publishconf连套配置以进行测试和实际发布的区分。

使用fabric自动部署

使用makefile自动部署


## 编写内容

### articles和pages

按时间发布的内容称为article

其他固定内容的称为pages(例如关于，联系，页头，页尾等信息页面)。这部分内容放在content/pages下

### 文件元数据

pelican需要通过一些元数据来获取文章相关的定义和分类等，还可以进行一些定制控制。

#### RST文件中元数据定义
```
My super title #标题
##############

:date: 2010-10-03 10:20 #创建日期
:modified: 2010-10-04 18:40 #修改日期
:tags: thats, awesome #标签
:category: yeah #分类
:slug: my-super-post #生成的静态文件名
:authors: Alexis Metaireau, Conan Doyle #作者
:summary: Short version for index and feeds #
```

#### markdown文件中元数据定义
```
Title: My super title
Date: 2010-12-03 10:20
Modified: 2010-12-05 19:30
Category: Python
Tags: pelican, publishing
Slug: my-super-post
Authors: Alexis Metaireau, Conan Doyle
Summary: Short version for index and feeds

This is the content of my super blog post.
```

#### html文件中元数据定义
```
<html>
    <head>
        <title>My super title</title>
        <meta name="tags" content="thats, awesome" />
        <meta name="date" content="2012-07-09 22:28" />
        <meta name="modified" content="2012-07-10 20:14" />
        <meta name="category" content="yeah" />
        <meta name="authors" content="Alexis Métaireau, Conan Doyle" />
        <meta name="summary" content="Short version for index and feeds" />
    </head>
    <body>
        This is the content of my super blog post.
    </body>
</html>
```

#### 草稿属性

当一篇文章还是草稿不想对外发布时，可以通过Status: draft属性控制。这样文章将输出到output/drafts目录，不会被其他文件关联显示。

相反的，如果所有文章默认都是草稿，只有正式发布的则要写成Status:published

```
# 在config中增加默认的元属性
DEFAULT_METADATA = {
    'status': 'draft',
}
```

#### 翻译属性

pelican通过slug属性判断多个语言文件对应一个显示文件。通过lang属性和DEFAULT_LANG配置控制只显示某种语言内容

如果要不被DEFAULT_LANG检查，需要使用translation: true属性

#### 其他属性

当有pages不想直接显示到menu中时，可以通过元属性status: hidden隐藏。例如定制的404反馈页。

### 文件的关联

### 文法高亮

## 高级设置

### 基本设置

| 参数 | 说明 |
|--------|--------|
|USE_FOLDER_AS_CATEGORY = True|将目录名作为分类|
|DEFAULT_CATEGORY = 'misc'|无法获取分类时的默认分类|
|DISPLAY_PAGES_ON_MENU = True|菜单栏显示pages|
|DISPLAY_CATEGORIES_ON_MENU = True|菜单栏显示分类|
|DOCUTILS_SETTINGS = {}|DOCUTILS的设置|
|DELETE_OUTPUT_DIRECTORY = False|每次生成前删除output目录|
|OUTPUT_RETENTION = []|在输出目录中保留不被删除的文件名后缀|
|JINJA_ENVIRONMENT = {'trim_blocks': True, 'lstrip_blocks': True}|jinja2环境变量|
|JINJA_FILTERS = {}|jinja2过滤器配置|
|LOG_FILTER = []|日志过滤器配置|
|READERS = {}|文件读取扩展，根据后缀名指定专门的读取器|
|IGNORE_FILES = ['.#*']|忽略处理的文件目录匹配模式|
|MARKDOWN = {...}|markdown配置，[参考](http://pythonhosted.org/Markdown/reference.html#markdown)|
|OUTPUT_PATH = 'output/'|输出目录|
|PATH|输入目录|
|PAGE_PATHS = ['pages']|相对输入目录的pages目录|
|PAGE_EXCLUDES = []|相对articlepaths的排除路径|
|ARTICLE_PATHS = ['']|相对path的articles路径|
|ARTICLE_EXCLUDES = []|相对page_excludes的目录|
|OUTPUT_SOURCES = False|同时输出原始文件|
|OUTPUT_SOURCES_EXTENSION = '.text'|输出原始文件时替换后缀|
|PLUGINS = []|使用的插件列表|
|PLUGIN_PATHS = []|插件路径|
|SITENAME = 'A Pelican Blog'|站点名称|
|SITEURL = []|站点的URL|
|STATIC_PATHS = ['images']|相对path静态文件路径，这部分内容会直接输出到output|
|STATIC_EXCLUDES = []||
|STATIC_EXCLUDE_SOURCES = True||
|TYPOGRIFY = False|排版增强|
|TYPOGRIFY_IGNORE_TAGS = []|排版忽略的标签|
|SUMMARY_MAX_LENGTH = 50|概要最大长度，如果没有指定元数据时生效|
|WITH_FUTURE_DATES = True|允许发布未到时间的文章|
|INTRASITE_LINK_REGEX = '[{|](?P<what>.*?)[|}]'|内部链接|
|PYGMENTS_RST_OPTIONS = []|rst文法高亮的参数|
|SLUGIFY_SOURCE = 'title'|未指定slug时slug生成规则|
|CACHE_CONTENT = False|生成缓存内容|
|CONTENT_CACHING_LAYER = 'reader'|缓存层，是读取或生成端|
|CACHE_PATH = 'cache'|缓存路径|
|GZIP_CACHE = True|缓存压缩|
|CHECK_MODIFIED_METHOD = 'mtime'|使用缓存时判断文件变化的方法|
|LOAD_CONTENT_CACHE = False|加载缓存的内容|
|WRITE_SELECTED = []||
|FORMATTED_FIELDS = ['summary']||

URL设置
| 参数 | 说明 |
|--------|--------|
|RELATIVE_URLS = False|使用相对路径，实际发布应该用绝对路径|
|ARTICLE_URL = '{slug}.html'|文档对应URL|
|ARTICLE_SAVE_AS = '{slug}.html'|文档存放路径|
|ARTICLE_LANG_URL = '{slug}-{lang}.html'|多语言时|
|ARTICLE_LANG_SAVE_AS = '{slug}-{lang}.html'||
|DRAFT_URL = 'drafts/{slug}.html'|草稿对应URL|
|DRAFT_SAVE_AS = 'drafts/{slug}.html'|草稿存放路径|
|DRAFT_LANG_URL = 'drafts/{slug}-{lang}.html'||
|DRAFT_LANG_SAVE_AS = 'drafts/{slug}-{lang}.html'||
|PAGE_URL = 'pages/{slug}.html'|页面对应URL|
|PAGE_SAVE_AS = 'pages/{slug}.html'|页面存放路径|
|PAGE_LANG_URL = 'pages/{slug}-{lang}.html'||
|PAGE_LANG_SAVE_AS = 'pages/{slug}-{lang}.html'||
|CATEGORY_URL = 'category/{slug}.html'|分类对应URL|
|CATEGORY_SAVE_AS = 'category/{slug}.html'|分类存放路径|
|CATEGORIES_SAVE_AS = 'categories.html'|所有分类存放路径|
|TAG_URL = 'tag/{slug}.html'|标签对应URL|
|TAG_SAVE_AS = 'tag/{slug}.html'|标签存放路径|
|TAGS_SAVE_AS = 'tags.html'|所有标签存放路径|
|AUTHOR_URL = 'author/{slug}.html'|作者对应URL|
|AUTHORS_SAVE_AS = 'authors.html'|所有作者存放路径|
|ARCHIVES_SAVE_AS = 'archives.html'|归档存储路径|
|YEAR_ARCHIVE_SAVE_AS = ''|年归档路径|
|MONTH_ARCHIVE_SAVE_AS = ''|月归档路径|
|DAY_ARCHIVE_SAVE_AS = ''|日归档路径|
|SLUG_SUBSTITUTIONS = ()|slug替换，按照(from, to, skip)原则处理|
|AUTHOR_SUBSTITUTIONS = ()|作者替换|
|CATEGORY_SUBSTITUTIONS = ()|分类替换|
|TAG_SUBSTITUTIONS = ()|标签替换|
|INDEX_SAVE_AS = 'index.html'|index存放路径|


时间设置
| 参数 | 说明 |
|--------|--------|
|TIMEZONE|时区设置|
|DEFAULT_DATE = None|如果没指定date元数据，产生date的方法|
|DEFAULT_DATE_FORMAT = '%a %d %B %Y'|默认的日期格式|
|DATE_FORMATS = {}|多语言时日期格式|
|LOCALE|local参数|

模板页配置
| 参数 | 说明 |
|--------|--------|
|EMPLATE_PAGES = None|配合jinja2使用的模板页|
|DIRECT_TEMPLATES = ['index', 'categories', 'authors', 'archives']|几种固定模板？|
|PAGINATED_DIRECT_TEMPLATES = ['index']|需要分页的模板|
|EXTRA_TEMPLATES_PATHS = []|其他模板路径|

元数据配置
| 参数 | 说明 |
|--------|--------|
|AUTHOR|默认的作者|
|DEFAULT_METADATA = {}|默认的元数据|
|FILENAME_METADATA = '(?P<date>d{4}-d{2}-d{2}).*'|根据文件名获取元数据|
|PATH_METADATA = ''|默认的元数据|
|EXTRA_PATH_METADATA = {}||

内容排序设置
| 参数 | 说明 |
|--------|--------|
|NEWEST_FIRST_ARCHIVES = True|按文件日期排序|
|REVERSE_CATEGORY_ORDER = False|分类按字母顺序排序|
|ARTICLE_ORDER_BY = 'reversed-date'|文章的排序规则|
|PAGE_ORDER_BY = 'basename'|page的排序|

主题设置
| 参数 | 说明 |
|--------|--------|
|THEME|主题名|
|THEME_STATIC_DIR = 'theme'|主题相关输出路径|
|THEME_STATIC_PATHS = ['static']||
|CSS_FILE = 'main.css'|按文件日期排序|

翻译设置
| 参数 | 说明 |
|--------|--------|
|DEFAULT_LANG = 'en'|默认语言|
|TRANSLATION_FEED_ATOM = 'feeds/all-%s.atom.xml'||
|TRANSLATION_FEED_RSS = None, i.e. no RSS||

分页设置
| 参数 | 说明 |
|--------|--------|
|DEFAULT_ORPHANS = 0|最后一页允许的文章数|
|DEFAULT_PAGINATION = False|默认一页的articles|
|PAGINATION_PATTERNS|分页的模式|

示例
```

PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)
```

## 主题与插件

### 主题管理

通过pelican-themes命令行工具管理主题

```
(pydev) [root@db1 myweb]# pelican-themes --help
usage: pelican-themes [-h] [-l | -p | -V] [-i theme path [theme path ...]]
                      [-r theme name [theme name ...]]
                      [-U theme path [theme path ...]]
                      [-s theme path [theme path ...]] [-c] [-v]

Install themes for Pelican

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            Show the themes already installed and exit
  -p, --path            Show the themes path and exit
  -V, --version         Print the version of this script
  -i theme path [theme path ...], --install theme path [theme path ...]
                        The themes to install
  -r theme name [theme name ...], --remove theme name [theme name ...]
                        The themes to remove
  -U theme path [theme path ...], --upgrade theme path [theme path ...]
                        The themes to upgrade
  -s theme path [theme path ...], --symlink theme path [theme path ...]
                        Same as `--install', but create a symbolic link
                        instead of copying the theme. Useful for theme
                        development
  -c, --clean           Remove the broken symbolic links of the theme path
  -v, --verbose         Verbose output
(pydev) [root@db1 myweb]# 
```

几个命令的演示
```
# 显示当前装的主题
(pydev) [root@db1 myweb]# pelican-themes -l -v
/home/liuyx/pydev/lib/python2.7/site-packages/pelican/themes/notmyidea
/home/liuyx/pydev/lib/python2.7/site-packages/pelican/themes/simple
/home/liuyx/pydev/lib/python2.7/site-packages/pelican/themes/voidy-bootstrap (symbolic link to `/home/liuyx/pydev/myweb/themes/voidy-bootstrap')

# 一次执行多个命令
pelican-themes --remove notmyidea-cms two-column \
               --install ~/Dev/Python/pelican-themes/notmyidea-cms-fr \
               --symlink ~/Dev/Python/pelican-themes/two-column \
               --verbose
```

### 主题定制

生成HTML文件时，pelican使用了jinja引起配合模板文件生成。因此主题就是对应的模板文件和样式定义。

可以通过pelican的-t参数指定主题，也可以在配置文件中通过THEME选项配置默认主题。

一个典型的主题布局

```
├── static
│   ├── css
│   └── images
└── templates
    ├── archives.html         // to display archives
    ├── period_archives.html  // to display time-period archives
    ├── article.html          // processed for each article
    ├── author.html           // processed for each author
    ├── authors.html          // must list all the authors
    ├── categories.html       // must list all the categories
    ├── category.html         // processed for each category
    ├── index.html            // the index (list all the articles)
    ├── page.html             // processed for each page
    ├── tag.html              // processed for each tag
    └── tags.html             // must list all the tags. Can be a tag cloud.
```

### 插件

从pelican3.0开始支持插件功能，插件扩展了pelican功能而不需要修改pelican代码。

使用方法
```
# 指定插件路径和插件包名
PLUGIN_PATHS = ["plugins", "/srv/pelican/plugins"]
PLUGINS = ["assets", "liquid_tags", "sitemap"]
```

插件功能基于python基础模块signals的使用。

## 常见问题