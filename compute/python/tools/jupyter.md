# jupyter

## [官方文档](http://jupyter.org/documentation)

## 简介

在介绍 Jupyter Notebook 之前，让我们先来看一个概念：文学编程[Literate programming](http://www.literateprogramming.com/)，这是由 Donald Knuth 提出的编程方法。

传统的结构化编程，人们需要按计算机的逻辑顺序来编写代码；与此相反，文学编程则可以让人们按照自己的思维逻辑来开发程序。

简单来说，文学编程的读者不是机器，而是人。 我们从写出让机器读懂的代码，过渡到向人们解说如何让机器实现我们的想法，其中除了代码，更多的是叙述性的文字、图表等内容。

Jupyter脱胎于IPython项目，IPython顾名思义是专注于Python的项目，但随着项目发展壮大已经不仅仅局限于Python这一种编程语言了。

Jupyter的名字就很好地释义了这一发展过程，它是Julia、Python 以及R语言的组合，字形相近于木星（Jupiter），而且现在支持的语言也远超这三种了。

是一种强大的交互式开发和演示环境。能够方便的将代码、公式、图表、文字在一个文档中全面的展示出来，并方便导出成多种格式输出。

### 优点

以下列举了Jupyter Notebook 的众多优点：

- 极其适合数据分析
- 支持多语言
- 分享便捷
- 远程运行
- 交互式展现

## 安装部署

### 安装

```
# 在虚拟环境上安装
(jupyter) [root@db137 jupyter]# pip -v install jupyter notebook
Collecting jupyter
...
...
Successfully installed backports-abc-0.5 backports.ssl-match-hostname-3.5.0.1 certifi-2017.7.27.1 ipykernel-4.6.1 ipython-5.5.0 ipywidgets-7.0.1 jupyter-1.0.0 jupyter-client-5.1.0 jupyter-console-5.2.0 notebook-5.1.0 pathlib2-2.3.0 pickleshare-0.7.4 python-dateutil-2.6.1 pyzmq-16.0.2 qtconsole-4.3.1 scandir-1.5 simplegeneric-0.8.1 singledispatch-3.4.0.3 terminado-0.6 tornado-4.5.2 widgetsnbextension-3.0.3
Cleaning up...

# 安装的包
(jupyter) [root@zxdb137 jupyter]# pip list
backports-abc (0.5)
backports.shutil-get-terminal-size (1.0.0)
...
...
terminado (0.6)
testpath (0.3.1)
tornado (4.5.2)
traitlets (4.3.2)
wcwidth (0.1.7)
webencodings (0.5.1)
wheel (0.29.0)
widgetsnbextension (3.0.3)
```

### 启动服务

服务的配置
```
(jupyter) [root@db137 jupyter]# jupyter notebook --generate-config
Writing default config to: /root/.jupyter/jupyter_notebook_config.py

修改几个默认配置
c.NotebookApp.ip
c.NotebookApp.notebook_dir
c.NotebookApp.open_browser
c.NotebookApp.port
c.NotebookApp.password
```

服务启动
```
(jupyter) [root@db137 jupyter]# jupyter notebook &
(jupyter) [root@db137 jupyter]# jupyter notebook list
(jupyter) [root@db137 jupyter]# jupyter notebook stop
```

运行程序的关闭
```
# 每创建或打开一个pynb，后台对应创建一个进程
# 可以通过点击这个文件前的复选框或在running页中选择，执行shutdown关闭
[root@zxdb137 data]# ps -ef|grep jupyter
root     12586     1  0 Jul26 ?        00:00:08 /home/liuyx/pydev/jupyter/bin/python /home/liuyx/pydev/jupyter/bin/jupyter-notebook
root     22894 12586 21 10:21 ?        00:00:00 /home/liuyx/pydev/jupyter/bin/python -m ipykernel_launcher -f /run/user/0/jupyter/kernel-0f92d231-dc9a-4277-851b-e70821e0b486.json
```

## Notebook使用

### 界面

打开笔记本后，你会看到顶部有三个选项卡：Files、Running 和 Clusters。其中，Files 基本上就是列出所有文件，Running 是展示你当前打开的终端和笔记本，Clusters 是由 IPython 并行提供的。

Notebook 文档是由一系列单元（Cell）构成，主要有两种形式的单元：

- 代码单元：这里是你编写代码的地方，通过按 Shift + Enter 运行代码，其结果显示在本单元下方。代码单元左边有 In [1]: 这样的序列标记，方便人们查看代码的执行次序。

- Markdown 单元：在这里对文本进行编辑，采用 markdown 的语法规范，可以设置文本格式、插入链接、图片甚至数学公式。同样使用 Shift + Enter 运行 markdown 单元来显示格式化的文本。

### 快捷键

类似于Linux的Vim编辑器，在notebook 中也有两种模式：

- 编辑模式：编辑文本和代码。选中单元并按 Enter 键进入编辑模式，此时单元左侧显示绿色竖线。

- 命令模式：用于执行键盘输入的快捷命令。通过 Esc 键进入命令模式，此时单元左侧显示蓝色竖线。

如果要使用快捷键，首先按 Esc 键进入命令模式，然后按相应的键实现对文档的操作。

- 切换成代码单元（Y）或 markdown单元（M）
- 在本单元的下方增加一单元（B）
- 执行当前cell，并自动跳到下一个cell：Shift Enter
- 删除当前的cell：DD
- 进入下一个cell：AA （前面）或 Alt+Enter（后面）
- 为当前的cell加入line number：L
- 为一行或者多行添加/取消注释：Crtl /
- 查看所有快捷命令可以按H。

### 单元格操作

高级单元格操作，将让编写 notebook 变得更加方便。举例如下：

- 如果想删除某个单元格，可以选择该单元格，然后依次点击Edit -> Delete Cell；

- 如果想移动某个单元格，只需要依次点击Edit -> Move cell [up | down]；

- 如果想剪贴某个单元测，可以先点击Edit -> Cut Cell，然后在点击Edit -> Paste Cell [Above | Below]；

- 如果你的notebook中有很多单元格只需要执行一次，或者想一次性执行大段代码，那么可以选择合并这些单元格。点击Edit -> Merge Cell [Above | below]。

记住这些操作，它们可以帮助你节省许多时间。

### Jupyter中的代码

#### 将py文件导入到cell中

```
%load test.py #test.py是当前路径下的一个python文件
运行结果是%load test.py被自动加入了注释符号#，test.py中的所有代码都被load到了当前的cell中

# 将远程py文件导入
%load http://aaa/test.py
```

直接运行py程序，输出结果到out
```
%run test.py
```

#### 在cell中使用unix命令
```
# 在unitx command前面加入一个感叹号“！”
!python --version
```
![shortcuts](./cell1.png)

#### 使用Matplotlib绘图

```
# cell中插入代码段
import matplotlib.pyplot as plt # 需要先包含绘图包 
import numpy as np
x = np.arange(20)
y = x**2
plt.plot(x, y)
plt.show() # 显示图形
```

![shortcuts](./cell2.png)

#### 更多的magicfunc

魔术关键字（magic keywords），正如其名是用于控制 notebook 的特殊的命令。它们运行在代码单元中，以 % 或者 %% 开头，前者控制一行，后者控制整个单元。

更详细的清单请参考 [Built-in magic commands](http://ipython.readthedocs.io/en/stable/interactive/magics.html)

### Jupyter中的Markdown

#### 支持嵌入html内容

```
# 跳入的锚点
<a id='the_destination'></a>

# 跳出的地方
[需要添加连接的文字](#the_destination)
```

#### 使用 LaTeX 的语法来插入数学公式

```
# 插入质能方程式
$E = mc^2$
```

## 导出和分享功能

notebook另一个强大的功能就是导出功能。你可以把你的notebook（例如是个图解代码课程）导出为如下多种形式：

HTML，Markdown，ReST，PDF(Through LaTex)，Raw Python

### nbconvert



## 扩展

### 为markdown增加目录功能

### 多语言内核

jupyter-kernelspec提供了查看和管理内核的命令

```
(jupyter) [root@zxdb137 ~]# jupyter-kernelspec list
Available kernels:
  c          /root/.local/share/jupyter/kernels/c
  python3    /root/.local/share/jupyter/kernels/python3
  python2    /home/liuyx/pydev/jupyter/share/jupyter/kernels/python2
  bash       /usr/local/share/jupyter/kernels/bash
(jupyter) [root@zxdb137 ~]#
```

可用的内核参考 https://github.com/jupyter/jupyter/wiki/Jupyter-kernels

以安装C语言支持内核为例

https://github.com/brendan-rius/jupyter-c-kernel
```
(jupyter) [root@zxdb137 jupyter-c-kernel-master]# python setup.py install
running install
running bdist_egg
running egg_info

Installed /home/liuyx/pydev/jupyter/lib/python3.6/site-packages/jupyter_c_kernel-1.2.1-py3.6.egg
Processing dependencies for jupyter-c-kernel==1.2.1
Finished processing dependencies for jupyter-c-kernel==1.2.1
(jupyter) [root@zxdb137 jupyter-c-kernel-master]#
(jupyter) [root@zxdb137 jupyter-c-kernel-master]# install_c_kernel
Installing IPython kernel spec
```

### 更换主题

## JupyterLab
