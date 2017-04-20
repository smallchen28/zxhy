# ClusterShell

## 简介

ClusterShell提供了一个轻量的，统一的，强壮的命令执行框架。非常适用于现代linux集群的日常维护。

主要特性包括

- 高效，并发，可扩展的命令行执行引擎

- 提供了统一的节点，组配置文法

- 为初步或日常管理提供了基本的命令工具

### 安装

适用于安装了python2.4-2.7的各个类unix系统。支持各种安装包形式，或者从pip安装。

### 配置

clush配置文件

```
/etc/clustershell/clush.conf
# 以下配置为用户独立配置
$XDG_CONFIG_HOME/clustershell/clush.conf
$HOME/.config/clustershell/clush.conf (only if $XDG_CONFIG_HOME is not defined)
$HOME/.local/etc/clustershell/clush.conf
$HOME/.clush.conf (deprecated, for 1.6 compatibility only)
```

可用配置项

|参数|值|备注|
|--------|--------|--------|
|fanout||滑动窗口大小|
|connect_timeout||创建一个连接的超时参数，该参数传递给ssh|
|command_timeout||命令超时参数|
|color|||
|fd_max||每个clush进程允许打开的文件句柄数|
|history_size||历史数，负数表示无限制|
|node_count|yes/no|是否在缓冲头显示节点数信息|
|verbosity|0(quiet),1(default),2(verbose),more(debug)|详细信息级别|
|ssh_user|远程连接用户||
|ssh_path|ssh命令路径||
|ssh_options|传递给ssh命令的其他参数||
|scp_path|scp命令路径||
|scp_options|scp命令参数||
|rsh_path|rsh命令路径||
|rsh_options|rsh命令参数||
|rcp_path|rcp命令路径||

节点组配置

将一组相关的节点统一管理，称为节点组。

group配置文件，配置文件通过python的configparser模块进行解析。
```
/etc/clustershell/groups.conf
# 以下配置为用户独立配置
$XDG_CONFIG_HOME/clustershell/groups.conf
$HOME/.config/clustershell/groups.conf (only if $XDG_CONFIG_HOME is not defined)
$HOME/.local/etc/clustershell/groups.conf
```

## 工具集

### nodeset/cluset 管理集群节点组和设置

对应clustershell库中NodeSet/RangeSet类的部分特性外部命令行实现。用来方便的管理集群节点和节点组定义。

### clush 并行执行命令工具

clush用来在集群环境中并行的执行命令并获取返回值。支持多种调用方式，可以交互式使用，也可以被其他应用或脚本调用。

基本命令帮助
```
[root@db1 ~]# clush --help
Usage: clush [options] command

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -s GROUPSOURCE, --groupsource=GROUPSOURCE
                        optional groups.conf(5) group source to use
  --nostdin             don't watch for possible input from stdin

  Selecting target nodes:
    -w NODES            nodes where to run the command
    -x NODES            exclude nodes from the node list
    -a, --all           run command on all nodes
    -g GROUP, --group=GROUP
                        run command on a group of nodes
    -X GROUP            exclude nodes from this group

  Output behaviour:
    -q, --quiet         be quiet, print essential output only
    -v, --verbose       be verbose, print informative messages
    -d, --debug         output more messages for debugging purpose
    -G, --groupbase     do not display group source prefix
    -L                  disable header block and order output by nodes
    -N                  disable labeling of command line
    -b, --dshbak        gather nodes with same output
    -B                  like -b but including standard error
    -r, --regroup       fold nodeset using node groups
    -S                  return the largest of command return codes
    --color=WHENCOLOR   whether to use ANSI colors (never, always or auto)
    --diff              show diff between gathered outputs

  File copying:
    -c, --copy          copy local file or directory to remote nodes
    --rcopy             copy file or directory from remote nodes
    --dest=DEST_PATH    destination file or directory on the nodes
    -p                  preserve modification times and modes

  Ssh/Tree options:
    -f FANOUT, --fanout=FANOUT
                        use a specified fanout
    -l USER, --user=USER
                        execute remote command as user
    -o OPTIONS, --options=OPTIONS
                        can be used to give ssh options
    -t CONNECT_TIMEOUT, --connect_timeout=CONNECT_TIMEOUT
                        limit time to connect to a node
    -u COMMAND_TIMEOUT, --command_timeout=COMMAND_TIMEOUT
                        limit time for command to run on the node
```

- 非交互式调用：clush -a | -g group | -w nodes  [OPTIONS] command

在指定节点上执行对应command命令

- 交互模式调用：clush -a | -g group | -w nodes  [OPTIONS]

进入类似shell的交互模式后支持的方法

|命令参数|说明|
|--------|--------|
|clush> ?|显示当前nodeset|
|clush> =<NODESET>|设置当前nodeset|
|clush> +<NODESET>|增加nodes到当前nodeset|
|clush> -<NODESET>|移除nodes|
|clush> !COMMAND|在本机执行命令|
|clush> =|切换输出格式，聚合或标准?|
|Ctrl + R|查询历史操作记录|
|Ctrl + D|退出交互模式|

- 文件拷贝模式：clush -a | -g group | -w nodes  [OPTIONS] --copy file | dir [ file | dir ...] [ --dest path ]

当指定-c/--copy选项时。尝试拷贝本地文件或路径到对应远程节点路径

- 反向文件拷贝模式：clush -a | -g group | -w nodes  [OPTIONS] --rcopy file | dir [ file | dir ...] [ --dest path ]

当指定--rcopy选项时。尝试将远程节点的文件或路径拷贝到本地

### clubak 收集和显示信息用

一般用来将clush输出的结果进行进一步处理，原始格式行为node:output。参数参照clush的格式输出参数部分。

## 示例

clush使用
```
# 在指定节点上执行uname -r命令
# clush -w node[3-5,62] uname -r
# 合并输出
# clush -w node[3-5,62] -bL uname -r
# 所有节点中排除部分节点
# clush -a -x node[5,7] uname -r
# 显示所有节点的这个文件并进行差异比较
# clush -a --diff cat /some/file
# 按组操作
# clush -g oss modprobe lustre
# clush -w @mds,@oss modprobe lustre
# 拷贝本地文件到远程
# clush -w node[3-5,62] --copy /etc/motd
# 反向拷贝
# clush -w node[3-5,62] --rcopy /etc/motd --dest /tmp
```

clubak使用
```
[root@db1 ~]# clush -a uname -r >/tmp/clush_output
[root@db1 ~]# cat /tmp/clush_output 
db1: 3.10.0-123.el7.x86_64
db2: 3.10.0-123.el7.x86_64
[root@db1 ~]# clubak -bL </tmp/clush_output
db[1-2]:  3.10.0-123.el7.x86_64
```

## 编程指南
