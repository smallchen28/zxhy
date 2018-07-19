# GIT����֪ʶ2

## ��Ҫ�ĸ���

�ճ������漰����������ͼ��ʾ

![gitbasic2](./bg2015120901.png)

- ������(workspace��worktree)�������㵱ǰ�ܿ�����Ŀ¼��

- �ݴ���(stage��index)��һ������ ".gitĿ¼��" �µ�index�ļ���.git/index���У������ݴ�����ʱҲ����������index����

- �汾��(repositroy)������������һ������Ŀ¼.git��������㹤����������Git�İ汾�⡣

- Զ�̿�(remote)�������Ŀ�Ǵ������ط�clone�����ģ�����Զ�̿⡣

```
[root@db3 .git]# ll -a
total 44
drwxr-xr-x 7 root root 4096 Apr 12 17:01 .
drwxr-xr-x 3 root root 4096 Apr 12 16:49 ..
drwxr-xr-x 2 root root 4096 Apr 12 16:21 branches    #branch��Ϣ
-rw-r--r-- 1 root root   92 Apr 12 16:21 config      #��������
-rw-r--r-- 1 root root   73 Apr 12 16:21 description
-rw-r--r-- 1 root root   23 Apr 12 16:21 HEAD        #headָ��
drwxr-xr-x 2 root root 4096 Apr 12 16:21 hooks
-rw-r--r-- 1 root root  104 Apr 12 16:54 index       #�ݴ���
drwxr-xr-x 2 root root 4096 Apr 12 16:21 info
drwxr-xr-x 5 root root 4096 Apr 12 16:54 objects
drwxr-xr-x 4 root root 4096 Apr 12 16:21 refs        #����
[root@db3 .git]#
```

�������ͼչʾ�˹��������汾���е��ݴ����Ͱ汾��֮��Ĺ�ϵ��

![git1](1352126739_7909.jpg)

ͼ�����Ϊ���������Ҳ�Ϊ�汾�⡣�ڰ汾���б��Ϊ "index" ���������ݴ�����stage, index�������Ϊ "master" ���� master ��֧�������Ŀ¼����

ͼ�����ǿ��Կ�����ʱ "HEAD" ʵ����ָ�� master ��֧��һ��"�α�"������ͼʾ�������г��� HEAD �ĵط������� master ���滻��

ͼ�е� objects ��ʶ������Ϊ Git �Ķ���⣬ʵ��λ�� ".git/objects" Ŀ¼�£���������˴����ĸ��ֶ������ݡ�

���Թ������޸ģ������������ļ�ִ�� "git add" ����ʱ���ݴ�����Ŀ¼�������£�ͬʱ�������޸ģ������������ļ����ݱ�д�뵽������е�һ���µĶ����У����ö����ID����¼���ݴ������ļ������С�

��ִ���ύ������git commit��ʱ���ݴ�����Ŀ¼��д���汾�⣨����⣩�У�master ��֧������Ӧ�ĸ��¡��� master ָ���Ŀ¼�������ύʱ�ݴ�����Ŀ¼����

��ִ�� "git reset HEAD" ����ʱ���ݴ�����Ŀ¼���ᱻ��д���� master ��ָ֧���Ŀ¼�����滻�����ǹ���������Ӱ�졣

��ִ�� "git rm --cached <file>" ����ʱ����ֱ�Ӵ��ݴ���ɾ���ļ����������������ı䡣

��ִ�� "git checkout ." ���� "git checkout -- <file>" ����ʱ�������ݴ���ȫ����ָ�����ļ��滻���������ļ������������Σ�գ��������������δ��ӵ��ݴ����ĸĶ���

��ִ�� "git checkout HEAD ." ���� "git checkout HEAD <file>" ����ʱ������ HEAD ָ��� master ��֧�е�ȫ�����߲����ļ��滻�ݴ������Լ��������е��ļ����������Ҳ�Ǽ���Σ���Եģ���Ϊ�����������������δ�ύ�ĸĶ���Ҳ������ݴ�����δ�ύ�ĸĶ���

HEAD�ĸ���

## diff

diff����������ʾ�ύ��Ĳ������Ŀ¼/�ݴ�����汾֮��Ĳ�������

```
git diff [filepath]  ��ʾ���������ݴ����Ĳ���[����ָ��·��]

git diff HEAD ��ʾ�������͵�ǰ�汾�Ĳ���(ͬ��)

git diff --cached ��ʾ�ݴ����͵�ǰ�汾�Ĳ���

git diff commit1 ��ʾ��������ĳ���汾�Ĳ���

git diff --cached commit1 ��ʾ�ݴ�����ĳ���汾֮��Ĳ���

git diff commit1 commit2 ��ʾ�����汾֮��Ĳ���

git diff branchname file ��ʾ��ǰ��֧��ָ����֧ĳ���ļ�·���Ĳ���

# ʾ��
[root@zxdb205 test]# git log --oneline
2ee45c0 b.txt add c
435eec9 b.txt add b
7ce7175 a.txt add 2
f52c948 first add
[root@zxdb205 test]# git diff f52c b.txt #2ee4��û�ύʱ�����ʼ�汾�ıȽ�
diff --git a/b.txt b/b.txt
index 7898192..8baef1b 100644
--- a/b.txt
+++ b/b.txt
@@ -1 +1 @@
-a
+abc
[root@zxdb205 test]# git diff 2ee4 435e #��������޸���b��diff������
diff --git a/b.txt b/b.txt
index 8baef1b..81bf396 100644
--- a/b.txt
+++ b/b.txt
@@ -1 +1 @@
-abc
+ab
[root@zxdb205 test]# git add c.txt  # �л���dev��֧,����c�ļ�������
[root@zxdb205 test]# git diff       # �Ѽ��뵽�ݴ���, ����û���
[root@zxdb205 test]# git diff HEAD  # �������͵�ǰ�汾�Ĳ���
diff --git a/c.txt b/c.txt
new file mode 100644
index 0000000..ce01362
--- /dev/null
+++ b/c.txt
@@ -0,0 +1 @@
+hello
[root@zxdb205 test]# git diff --cached # �ݴ����Ͱ汾�Ĳ���
diff --git a/c.txt b/c.txt
new file mode 100644
index 0000000..ce01362
--- /dev/null
+++ b/c.txt
@@ -0,0 +1 @@
+hello
[root@zxdb205 test]# git diff master  # ��������master��֧���汾�Ĳ��
diff --git a/c.txt b/c.txt
new file mode 100644
index 0000000..ce01362
--- /dev/null
+++ b/c.txt
@@ -0,0 +1 @@
+hello
```

## show

��ʾһ������git�еĶ���(blobs, trees, tags and commits)

```
git show [commit] ��ʾĳ���ύ��Ԫ���ݺ����ݱ仯��û��������ʾ���һ���ύ

git show --name-only [commit] ��ʾĳ���ύ���ļ�

git show commit filename ��ʾĳ���ύĳ���ļ���Ԫ���ݼ����ݱ仯
```

## reset

����HEAD���ض�״̬���������ͬʱ��Թ��������ݴ�������Ӱ�졣

```
git reset [<mode>] [<commit>] #��HEADָ��ĳ���汾��һ��5��ģʽ

git reset �C-mixed ��ΪĬ�Ϸ�ʽ�������κβ���ʱ�����ַ�ʽ������֧���ݴ�����λ��ָ��λ�ã�����������

git reset --soft ����֧��λ��ָ���汾λ�ã������ݴ����͹�����

git reset --hard ����֧,������,�ݴ���ȫ����λ��ָ���汾

git reset --merged ͬ--hard,�������������ݴ����Ĳ��졪���ϲ����µĹ���������ͻʱ����ʧ�ܡ�

git reset --keep ͬ--hard,������������HEAD�Ĳ��졪���ϲ����µĹ���������ͻʱ����ʧ�ܡ�

#����������ִ��resetͨ������������ع�ĳ�����޸�

git reset HEAD [file] ��add���ļ����ݴ�������λ���汾�Ķ�Ӧ�ļ������ݴ�������Ӱ�칤����

git reset HEAD^ [file] �ָ���һ���ύ���ݴ�������ʱrepo��Ӧ���ϴ�,index�ϴ�,����work���ļ��仯

git reset commitid  ���˵�ĳ���汾����������ͬ��

git reset --soft HEAD~3 �ָ���n��֮ǰ����ʱindex���������n���ύ�Ĳ��죬

git reset --hard  commitid ȫ�����˵�ĳ�汾������Ҳ������

git reset �C-hard origin/master ȫ�����˵���ӦԶ�̰汾

```

## reflog

reflog���Բ鿴���з�֧�����в�����¼��ͨ��������Ϊ�����reset������Ļָ�

```
# ͨ������-n������ʾ�����n�β���
[root@zxdb205 test]# git reflog
2ee45c0 HEAD@{0}: checkout: moving from dev to master
7ce7175 HEAD@{1}: checkout: moving from master to dev
2ee45c0 HEAD@{2}: checkout: moving from dev to master
7ce7175 HEAD@{3}: checkout: moving from dev to dev
7ce7175 HEAD@{4}: reset: moving to 7ce7
24c2da4 HEAD@{5}: commit: add c.txt
2ee45c0 HEAD@{6}: reset: moving to 2ee45c0
7ce7175 HEAD@{7}: reset: moving to HEAD^^
2ee45c0 HEAD@{8}: reset: moving to 2ee45c0
435eec9 HEAD@{9}: reset: moving to HEAD^
2ee45c0 HEAD@{10}: checkout: moving from master to dev
2ee45c0 HEAD@{11}: commit: b.txt add c
435eec9 HEAD@{12}: commit: b.txt add b
7ce7175 HEAD@{13}: commit: a.txt add 2
f52c948 HEAD@{14}: commit (initial): first add
# ��ʾָ����֧�ϵĲ�����ʷ
[root@zxdb205 test]# git reflog show master
2ee45c0 master@{0}: commit: b.txt add c
435eec9 master@{1}: commit: b.txt add b
7ce7175 master@{2}: commit: a.txt add 2
f52c948 master@{3}: commit (initial): first add
# ���Կ���dev�Ǵ�2ee4��������
[root@zxdb205 test]# git reflog show dev
7ce7175 dev@{0}: reset: moving to 7ce7
24c2da4 dev@{1}: commit: add c.txt
2ee45c0 dev@{2}: reset: moving to 2ee45c0
7ce7175 dev@{3}: reset: moving to HEAD^^
2ee45c0 dev@{4}: reset: moving to 2ee45c0
435eec9 dev@{5}: reset: moving to HEAD^
2ee45c0 dev@{6}: branch: Created from HEAD
# ͨ�����λ�ûص�c������ύ
[root@zxdb205 test]# git reset --hard dev@{1}
HEAD is now at 24c2da4 add c.txt
[root@zxdb205 test]#
```

## revert

revert��reset�������������ύ���������revert��ͨ���µ��ύ����ĳ��һ�Ρ�

## stash

��ʱ�洢�������Խ����������ݴ�������ʱ��ŵ�stash�

```
git stash save "message" �����������ݴ������ݴ洢�����ϱ���

git stash list �г��ѱ�����嵥�������ƶ�ջ�ķ�ʽ���棬���Կ���Pop

git stash drop ɾ��ĳ�����������

git stash pop �ָ����ݲ���stash��ɾ��

git stash apply �ָ����ݲ���ɾ��

git stash clear ������б��������

# ʾ��
[root@zxdb205 test]# git stash list
stash@{0}: On dev: b.txt add d
stash@{1}: On dev: c.txt add world
[root@zxdb205 test]# git stash apply stash@{1}
# On branch dev
# Changes not staged for commit:
#   (use "git add <file>..." to update what will be committed)
#   (use "git checkout -- <file>..." to discard changes in working directory)
#
#       modified:   c.txt
#
no changes added to commit (use "git add" and/or "git commit -a")
```

## config