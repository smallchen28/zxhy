# GIT分支与标签

有人把 Git 的分支模型称为它的`‘必杀技特性’'，也正因为这一特性，使得 Git 从众多版本控制系统中脱颖而出。 

为何 Git 的分支模型如此出众呢？ Git 处理分支的方式可谓是难以置信的轻量，创建新分支这一操作几乎能在瞬间完成，并且在不同分支之间的切换操作也是一样便捷。 与许多其它版本控制系统不同，Git 鼓励在工作流程中频繁地使用分支与合并，哪怕一天之内进行许多次。 

理解和精通这一特性，你便会意识到 Git 是如此的强大而又独特，并且从此真正改变你的开发方式。

## branch

branch命令用来创建/显示/删除分支

```
git branch 列出本地分支，当前分支前用*标志

git branch -a 列出本地和远程分支

git branch -r 列出远程分支

git branch bname 创建分支bname

git branch -d bname 删除分支

git branch -vv 查看本地分支对应的远程分支

git branch -m bname cname 分支改名

git branch bname startpoint 从某个位置创一个新分支，可以是某个分支，某个提交或远端分支
```

## checkout

checkout用来切换分支或恢复工作区文件

```
git checkout bname 切换到bname分支

git checkout - 切换到上一个分支

git checkout -b bname 切换到bname分支，如果没有则创建分支

git checkout -B bname 切换到bname分支，如果分支已存在则覆盖

git checkout commit 检出某个版本，此时进入detachedHEAD状态(相当于创建某个临时分支)

git checkout commitid filename 检出某个版本的某个文件覆盖当前工作区和暂存区对应文件

git checkout -- '*.c' 从暂存区从检出所有c文件覆盖工作区，--用来区分文件防止和分支名混淆
```

### checkout的本质是什么？

### checkout和reset的对比

两者的传入参数包括分支，版本，版本+文件共3种情况
```
# head一列中的REF表示该命令移动了HEAD指向的分支引用，而“HEAD”则表示只移动了HEAD自身。
# wdsafe一列，YES表示不会懂你在workdir的修改，NO代表会动你在workdir的修改。
                         head    index   workdir  wdsafe
Commit Level
reset --soft [commit]    REF     NO      NO        YES
reset [commit]           REF     YES     NO        YES
reset --hard [commit]    REF     YES     YES       NO
checkout [commit]        HEAD    YES     YES       YES

File Level
reset (commit) [file]    NO      YES     NO        YES
checkout (commit) [file] NO      YES     YES       NO
```

## merge

一旦某分支有了独立内容，最终需要将它合并回到你的主分支。你可以使用merge命令将任何分支合并到当前分支中去

几种合并模式：


## rebase

## tag

标签可以针对某一时间点的版本做标记，常用于版本发布。

git标签分为两种类型：轻量标签和附注标签。轻量标签是指向提交对象的引用，附注标签则是仓库中的一个独立对象，建议使用附注标签，日后还可以查看标签信息。

```
git tag 列出当前库的所有标签

git tag -l 'v0.1.*' 列出指定条件的标签

git show tname 显示某个标签的详细信息

git tag tname 在当前的分支的最后版本上打上标签tname

git tag tname commitid 在指定版本上打上标签

git tag v0.2.0 -light 轻量标签

git tag -a v0.1.0 -m "release 0.1.0 version"  创建了附属标签

git tag -d tname 删除本地标签

# 远程操作部分参考gitremote.md文档
```

## tag和branch的比较

