# GIT基础知识

## GIT是什么

Git是目前世界上最先进的分布式版本控制系统(没有之一)。

## GIT常用命令

如下显示了git最常用的命令，掌握这些基本命令就可以很好的进行版本管理。

git help <command> 能够用来显示具体子命令的帮助信息。

按照功能进行简单的划分:

- 版本库管理 init,status

- 文件处理 add,rm,mv,commit

- 版本管理 diff,log,grep,rebase,reset

- 分支与标签 branch,checkout,cherry-pick,tag,merge

- 远程库协作 clone,fetch,pull,push

- 其他功能 bisect,show

```
[root@db3 ~]# git help
usage: git [--version] [--help] [-c name=value]
           [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
           [-p|--paginate|--no-pager] [--no-replace-objects] [--bare]
           [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
           <command> [<args>]

The most commonly used git commands are:
   add        Add file contents to the index
   bisect     Find by binary search the change that introduced a bug
   branch     List, create, or delete branches
   checkout   Checkout a branch or paths to the working tree
   clone      Clone a repository into a new directory
   commit     Record changes to the repository
   diff       Show changes between commits, commit and working tree, etc
   fetch      Download objects and refs from another repository
   grep       Print lines matching a pattern
   init       Create an empty Git repository or reinitialize an existing one
   log        Show commit logs
   merge      Join two or more development histories together
   mv         Move or rename a file, a directory, or a symlink
   pull       Fetch from and merge with another repository or a local branch
   push       Update remote refs along with associated objects
   rebase     Forward-port local commits to the updated upstream head
   reset      Reset current HEAD to the specified state
   rm         Remove files from the working tree and from the index
   show       Show various types of objects
   status     Show the working tree status
   tag        Create, list, delete or verify a tag object signed with GPG

'git help -a' and 'git help -g' lists available subcommands and some
concept guides. See 'git help <command>' or 'git help <concept>'
to read about a specific subcommand or concept.
```

## init

init命令用来本地创建一个版本库。版本库又名仓库，英文名repository。可以理解为一个目录，目录内的文件可以通过git进行版本管理。

```
# 直接初始化
[root@db3 ~]# git init mycode
Initialized empty Git repository in /root/mycode/.git/
# 进入目录再初始化
[root@db3 ~]# mkdir mycodeb
[root@db3 ~]# cd mycodeb
[root@db3 mycodeb]# git init
Initialized empty Git repository in /root/mycodeb/.git/
# 产生的隐藏目录.git
[root@db3 mycodeb]# ll -a
total 12
drwxr-xr-x   3 root root 4096 Apr 12 16:21 .
dr-xr-x---. 32 root root 4096 Apr 12 16:21 ..
drwxr-xr-x   7 root root 4096 Apr 12 16:21 .git
```

## status

status命令可以让我们时刻掌握仓库当前的状态

```
# 显示当前目录状态，包括分支信息，工作目录下变化文件
[root@db3 mycodeb]# git status
# On branch master
#
# Initial commit
#
# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
#
#       aaa.txt

# -s简短输出模式，-b同时显示分支信息
[root@db3 mycodeb]# git status -s -b
## Initial commit on master
A  aaa.txt

在short模式下，一行信息表示如下
XY PATH1 -> PATH2
```

## clone

clone命令用来从一个已有版本库复制一个新的库。可以从远程，也可以使本地复制到当前指定目录

```
git clone <repo> <directory>

# 从本地的库复制到另一个目录
[root@db1 ~]# git clone /home/developer/dbdev.git mydev
Cloning into 'mydev'...
done.

# 从远程机器上复制到本机目录
[root@zxdb205 ~]# git clone ssh://root@10.43.174.141/home/developer/dbdev.git
Cloning into 'dbdev'...
The authenticity of host '10.43.174.141 (10.43.174.141)' can't be established.
ECDSA key fingerprint is SHA256:DNg0eXJfKkDOU7UkCWufDV7WBqivNsfjHLbOMj3EoW4.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.43.174.141' (ECDSA) to the list of known hosts.
root@10.43.174.141's password:
remote: Counting objects: 209, done.
remote: Compressing objects: 100% (191/191), done.
Receiving objects:  33% (69/209), 8.19 MiB | 8.15 MiB/s
remote: Total 209 (delta 71), reused 0 (delta 0)
Receiving objects: 100% (209/209), 82.86 MiB | 10.38 MiB/s, done.
Resolving deltas: 100% (71/71), done.

# 从第三方服务器上复制库
git clone git://github.com/CosmosHua/locate.git new
```

## add

add命令用于将改的存入暂存区

```
# 未加入到stage区时的提示
[root@db1 dbdev.git]# git status
# On branch master
# Changes not staged for commit:
#   (use "git add <file>..." to update what will be committed)
#   (use "git checkout -- <file>..." to discard changes in working directory)
#
#       modified:   dbmanager/backup/mysqlbackup.sh
#       modified:   dbmanager/common/mysql_common.sh
#       modified:   dbmanager/hascript/galeramanager
#
no changes added to commit (use "git add" and/or "git commit -a")
# 加入到stage区后的提示
[root@db1 dbdev.git]# git status
# On branch master
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
#
#       modified:   dbmanager/backup/mysqlbackup.sh
#       modified:   dbmanager/common/mysql_common.sh
#       modified:   dbmanager/hascript/galeramanager
#

# 另一种short模式，注意区分前两个字段
[root@db1 dbdev.git]# git status -s
 M dbmanager/backup/mysqlbackup.sh
 M dbmanager/common/mysql_common.sh
 M dbmanager/hascript/galeramanager
[root@db1 dbdev.git]# git add .
[root@db1 dbdev.git]# git status -s
M  dbmanager/backup/mysqlbackup.sh
M  dbmanager/common/mysql_common.sh
M  dbmanager/hascript/galeramanager
```

## commit

通过commit命令将暂存区内容提交到版本库中

```
# 提交到版本库
[root@db1 testgit]# git commit -m "add a file for task1"
[master (root-commit) e92deda] add a file for task1
 1 file changed, 8 insertions(+)
 create mode 100644 aa.txt

# -a参数表示跳过add阶段，直接将修改和删除的文件提交到版本库
[root@db1 testgit]# rm -f aa.txt
[root@db1 testgit]# touch bbb.txt
[root@db1 testgit]# git status
# On branch master
# Changes not staged for commit:
#   (use "git add/rm <file>..." to update what will be committed)
#   (use "git checkout -- <file>..." to discard changes in working directory)
#
#       deleted:    aa.txt
#
# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
#
#       bb.txt
no changes added to commit (use "git add" and/or "git commit -a")
[root@db1 testgit]# git commit -am "add file bbb for task2"
[master f7ac1b8] add file bbb for task2
 1 file changed, 8 deletions(-)
 delete mode 100644 aa.txt
[root@db1 testgit]# git status
# On branch master
# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
#
#       bb.txt
nothing added to commit but untracked files present (use "git add" to track)

# --amend表示追加操作，继续完善本次提交
[root@db1 testgit]# git add bb.txt
[root@db1 testgit]# git commit --amend
[master 8e7e4b4] add file bbb for task2
 2 files changed, 8 deletions(-)
 delete mode 100644 aa.txt
 create mode 100644 bb.txt
```

## mv

用于改变或移动目录,文件,软链接

```
# 将文件名修改同时加入到暂存区中
[root@db1 testgit]# git mv bb.txt bbb.txt
[root@db1 testgit]# git status
# On branch master
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
#
#       renamed:    bb.txt -> bbb.txt
#
```

## rm

用于删除文件或目录

```
# 删除一个文件并加入到暂存区
[root@db1 testgit]# git status
# On branch master
nothing to commit, working directory clean
[root@db1 testgit]# ll
total 0
-rw-r--r-- 1 root root 0 Apr 14 14:47 bb.txt
[root@db1 testgit]# git rm bb.txt
rm 'bb.txt'
[root@db1 testgit]# git status
# On branch master
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
#
#       deleted:    bb.txt
#
```

## log

显示版本库提交历史日志

```
# 普通显示包含4行内容：依次为提交版本号，提交人，提交日期，提交的message
git log

# 输出形式调整
git log --oneline  精简显示，每条日志一行

git log --pretty=raw|short|oneline|medium|full等  原生显示及其他格式

git log --graph 显示分支提交的历史线索，够成一个有向图

git log --name-only, --name-status  显示每次提交对应的文件清单(及状态变化)

git log -p  以patch的方式显示每条日志的修改内容

git log -stat  以统计(文件改动的行数)的方式显示每条日志的修改内容

# 按条件显示部分日志
git log -n 显示最近N条日志

git log --skip=n 跳过几条

git log -- filename1 显示某文件(路径)涉及的变更，用--和其他参数隔要开放到最后面

git log commit 查看commit版本号之前的日志，包括commit

git log commit1 commit2 查看commit1到commit2之间的日志，包括c1/c2

git log commit1..commit2 查看commit1到commit2之间的日志，不包括c1

git log --no-merges, --merges 忽略掉合并或仅显示合并

git log branchname 显示某个分支的提交日志

git log branchA..branchB 显示两个分支的差异？

git log branch -- filename 显示某个分支的某个文件的修改日志

# 搜索日志
git log --author=yourname,--committer= 按作者名搜索

git log --grep keyword 按关键字搜索,--all-match 当有多个条件时与关系

git log --since=<date>, --after=<date> 按日期搜索

git log --until=<date>, --before=<date> 按日期搜索

git log -S"Hello,World!", -G"reg" 搜索某行代码段相关的日志,G支持正则表达式

# 一个稍复杂的例子
$ git log --pretty="%h - %s" --author=gitster --since="2008-10-01" --before="2008-11-01" --no-merges -- t/
5610e3b - Fix testcase failure when extended attribute
acd3b9e - Enhance hold_lock_file_for_{update,append}()
f563754 - demonstrate breakage of detached checkout wi
d1a43f2 - reset --hard/read-tree --reset -u: remove un
51a94af - Fix "checkout --track -b newbranch" on detac
b0ad11e - pull: allow "git pull origin $something:$cur

# 其他功能
git shortlog 创建发布通知，将commit按作者分组

```
