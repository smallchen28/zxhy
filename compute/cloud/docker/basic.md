docker基本使用

## 简介

### docker版本

从2017开始docker开始区分社区版本CE和企业版EE，企业版增加了安全性和可管理特性。一般使用仍可使用CE版。

支持比较好的操作系统包括CENTOS/UBUNTU。本文档基于CENTOS，docker1.12

### docker安装

在centos7上直接通过yum安装。
```
[root@VMCentOS7Lyx ~]# yum install docker
# 启动服务端
[root@VMCentOS7Lyx ~]# systemctl start docker
# 查看版本
[root@VMCentOS7Lyx ~]# docker version
Client:
 Version:         1.12.6
 API version:     1.24
 Package version: docker-common-1.12.6-11.el7.centos.x86_64
 Go version:      go1.7.4
 Git commit:      96d83a5/1.12.6
 Built:           Tue Mar  7 09:23:34 2017
 OS/Arch:         linux/amd64

Server:
 Version:         1.12.6
 API version:     1.24
 Package version: docker-common-1.12.6-11.el7.centos.x86_64
 Go version:      go1.7.4
 Git commit:      96d83a5/1.12.6
 Built:           Tue Mar  7 09:23:34 2017
 OS/Arch:         linux/amd64
```

## 基础命令

### 启动第一个容器

docker run命令
```
[root@VMCentOS7Lyx ~]# docker run -it centos /bin/bash 
Unable to find image 'centos:latest' locally
Trying to pull repository docker.io/library/centos ... 
latest: Pulling from docker.io/library/centos
Digest: sha256:4eda692c08e0a065ae91d74e82fff4af3da307b4341ad61fa61771cc4659af60
# 进入了容器的的sh
[root@46c7fc0f9c40 /]# 
[root@46c7fc0f9c40 /]# ls
anaconda-post.log  bin  dev  etc  home  lib  lib64  lost+found  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
[root@46c7fc0f9c40 /]# ps -aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.1  0.0  11768  1884 ?        Ss   07:05   0:00 /bin/bash
root        13  0.0  0.0  47440  1680 ?        R+   07:06   0:00 ps -aux                                                                                                        
# 退出容器
[root@46c7fc0f9c40 /]# exit
exit
[root@VMCentOS7Lyx ~]# 
``` 

### 镜像使用

#### docker images 显示当前的镜像

```
[root@VMCentOS7Lyx ~]# docker images
REPOSITORY                       TAG                 IMAGE ID            CREATED             SIZE
daocloud.io/library/rabbitmq     3.6.9               8cc5f4e7fb90        9 days ago          179.4 MB
docker.io/mysql                  latest              d5127813070b        9 days ago          407.1 MB
docker.io/centos                 latest              a8493f5f50ff        2 weeks ago         192.5 MB
daocloud.io/centos               7                   a8493f5f50ff        2 weeks ago         192.5 MB
docker.io/busybox                latest              00f017a8c2a6        6 weeks ago         1.11 MB
daocloud.io/library/mongo        2.6.11              f36fb0070896        13 months ago       390.9 MB
daocloud.io/daocloud/minecraft   latest              c403a260b854        16 months ago       418.9 MB
```

我们在镜像列表中看到三个至关重要的东西。

- 来自什么镜像源，例如 ubuntu
- 每个镜像都有标签(tags)，例如 14.04
- 每个镜像都有镜像ID

#### docker pull 拉取镜像

一般都可以从官方dockerhub获取或者从其他第三方库拉取指定镜像。如果运行时本地没有库会从官方库尝试拉取

命令帮助
```
[root@VMCentOS7Lyx ~]# docker help pull

Usage:  docker pull [OPTIONS] NAME[:TAG|@DIGEST]

Pull an image or a repository from a registry

Options:
  -a, --all-tags                Download all tagged images in the repository
      --disable-content-trust   Skip image verification (default true)
      --help                    Print usage
```

#### docker search 搜索镜像

使用示例
```
[root@VMCentOS7Lyx ~]# docker search mariadb
INDEX       NAME                                DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
docker.io   docker.io/mariadb                   MariaDB is a community-developed fork of M...   1289      [OK]       
docker.io   docker.io/bitnami/mariadb           Bitnami MariaDB Docker Image                    33                   [OK]
docker.io   docker.io/paintedfox/mariadb        A docker image for running MariaDB 5.5, a ...   29                   [OK]
docker.io   docker.io/million12/mariadb         MariaDB 10 on CentOS-7 with UTF8 defaults       14                   [OK]
docker.io   docker.io/toughiq/mariadb-cluster   Dockerized Automated MariaDB Galera Cluste...   9                    [OK]
docker.io   docker.io/webhippie/mariadb         Docker images for mariadb                       8                    [OK]
docker.io   docker.io/panubo/mariadb-galera     MariaDB Galera Cluster                          7                    [OK]
```

#### docker rmi 删除镜像
```
[root@VMCentOS7Lyx ~]# docker rmi daocloud.io/centos
Error response from daemon: No such image: daocloud.io/centos:latest
[root@VMCentOS7Lyx ~]# docker rmi daocloud.io/centos:7
Untagged: daocloud.io/centos:7
Untagged: daocloud.io/centos@sha256:80aa348201b7f4e4d68e68c5ef97f875473b035b1f9646e44c88d2975a424223
```

### 容器使用

#### docker create 创建容器

#### docker ps 列出容器

支持选项-l显示最后创建的容器，-a显示所有容器。默认只显示运行的。-s显示所有文件大小。

示例
```
[root@VMCentOS7Lyx ~]# docker ps -a 
CONTAINER ID        IMAGE                      COMMAND                  CREATED             STATUS                     PORTS               NAMES
46c7fc0f9c40        centos                     "/bin/bash"              3 hours ago         Exited (0) 3 hours ago                         tiny_wing
a4eb3237b976        docker.io/busybox:latest   "sh"                     24 hours ago        Exited (0) 24 hours ago                        box
0d3c87ed6236        d5127813070b               "docker-entrypoint.sh"   2 days ago          Exited (255) 4 hours ago   3306/tcp            mysqltest
f42b506096d6        mysql                      "docker-entrypoint.sh"   2 days ago          Exited (1) 2 days ago                          tiny_shannon
[root@VMCentOS7Lyx ~]# 
```

#### docker start 启动容器

命令帮助
```
[root@VMCentOS7Lyx ~]# docker help start

Usage:  docker start [OPTIONS] CONTAINER [CONTAINER...]

Start one or more stopped containers

Options:
  -a, --attach               Attach STDOUT/STDERR and forward signals
      --detach-keys string   Override the key sequence for detaching a container
      --help                 Print usage
  -i, --interactive          Attach container's STDIN
# 示例
[root@VMCentOS7Lyx ~]# docker start -i tiny_wing
[root@46c7fc0f9c40 /]# 
```

#### docker restart 重启容器

命令帮助
```
[root@VMCentOS7Lyx ~]# docker help restart

Usage:  docker restart [OPTIONS] CONTAINER [CONTAINER...]

Restart a container

Options:
      --help       Print usage
  -t, --time int   Seconds to wait for stop before killing the container (default 10)
```

#### docker stop 停止容器

命令帮助
```
[root@VMCentOS7Lyx ~]# docker help stop

Usage:  docker stop [OPTIONS] CONTAINER [CONTAINER...]

Stop one or more running containers

Options:
      --help       Print usage
  -t, --time int   Seconds to wait for stop before killing it (default 10)
```

#### docker rm 删除容器

命令帮助
```
[root@VMCentOS7Lyx ~]# docker help rm

Usage:  docker rm [OPTIONS] CONTAINER [CONTAINER...]

Remove one or more containers

Options:
  -f, --force     Force the removal of a running container (uses SIGKILL)
      --help      Print usage
  -l, --link      Remove the specified link
  -v, --volumes   Remove the volumes associated with the container
```

#### docker rename 容器重命名

命令帮助
```
[root@VMCentOS7Lyx ~]# docker help rename

Usage:  docker rename CONTAINER NEW_NAME

Rename a container

Options:
      --help   Print usage
```

### 更多容器使用

#### docker run 在新容器中运行命令

#### docker attach 

命令帮助
```
[root@VMCentOS7Lyx ~]# docker help attach

Usage:  docker attach [OPTIONS] CONTAINER

Attach to a running container

Options:
      --detach-keys string   Override the key sequence for detaching a container
      --help                 Print usage
      --no-stdin             Do not attach STDIN
      --sig-proxy            Proxy all received signals to the process (default true)
```

#### docker cp 在容器和本地系统之间拷贝文件/目录

命令帮助
```
[root@VMCentOS7Lyx ~]# docker help cp

Usage:  docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-
        docker cp [OPTIONS] SRC_PATH|- CONTAINER:DEST_PATH

Copy files/folders between a container and the local filesystem

Options:
  -L, --follow-link   Always follow symbol link in SRC_PATH
      --help          Print usage
```

#### docker exec 在容器中执行另外的命令

命令帮助
```
[root@VMCentOS7Lyx ~]# docker help exec

Usage:  docker exec [OPTIONS] CONTAINER COMMAND [ARG...]

Run a command in a running container

  -d, --detach         Detached mode: run command in the background
  --detach-keys        Override the key sequence for detaching a container
  --help               Print usage
  -i, --interactive    Keep STDIN open even if not attached
  --privileged         Give extended privileges to the command
  -t, --tty            Allocate a pseudo-TTY
  -u, --user           Username or UID (format: <name|uid>[:<group|gid>])
[root@VMCentOS7Lyx ~]# 
```

使用示例
```
[root@VMCentOS7Lyx ~]# docker exec mysqltest my_print_defaults mysqld
--skip-host-cache
--skip-name-resolve
--pid-file=/var/run/mysqld/mysqld.pid
--socket=/var/run/mysqld/mysqld.sock
--datadir=/var/lib/mysql
--symbolic-links=0
```

#### docker kill 杀死容器

命令帮助
```
[root@VMCentOS7Lyx ~]# docker help kill

Usage:  docker kill [OPTIONS] CONTAINER [CONTAINER...]

Kill one or more running containers

Options:
      --help            Print usage
  -s, --signal string   Signal to send to the container (default "KILL")
```

#### docker logs 获取日志

命令帮助
```
[root@VMCentOS7Lyx ~]# docker help logs

Usage:  docker logs [OPTIONS] CONTAINER

Fetch the logs of a container

Options:
      --details        Show extra details provided to logs
  -f, --follow         Follow log output
      --help           Print usage
      --since string   Show logs since timestamp
      --tail string    Number of lines to show from the end of the logs (default "all")
  -t, --timestamps     Show timestamps
```

使用示例
```
[root@VMCentOS7Lyx ~]# docker logs --tail 10 mysqltest
2017-04-20T06:10:03.399316Z 0 [Warning] 'user' entry 'mysql.sys@localhost' ignored in --skip-name-resolve mode.
2017-04-20T06:10:03.399336Z 0 [Warning] 'db' entry 'sys mysql.sys@localhost' ignored in --skip-name-resolve mode.
2017-04-20T06:10:03.399345Z 0 [Warning] 'proxies_priv' entry '@ root@localhost' ignored in --skip-name-resolve mode.
2017-04-20T06:10:03.400626Z 0 [Warning] 'tables_priv' entry 'sys_config mysql.sys@localhost' ignored in --skip-name-resolve mode.
2017-04-20T06:10:03.405767Z 0 [Note] Event Scheduler: Loaded 0 events
2017-04-20T06:10:03.405865Z 0 [Note] mysqld: ready for connections.
Version: '5.7.18'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server (GPL)
2017-04-20T06:10:03.405871Z 0 [Note] Executing 'SELECT * FROM INFORMATION_SCHEMA.TABLES;' to get a list of tables using the deprecated partition engine. You may use the startup option '--disable-partition-engine-check' to skip this check. 
2017-04-20T06:10:03.405873Z 0 [Note] Beginning of list of non-natively partitioned tables
2017-04-20T06:10:03.414675Z 0 [Note] End of list of non-natively partitioned tables
```

#### docker port 显示或设置端口映射

命令帮助
```
[root@VMCentOS7Lyx ~]# docker help port

Usage:  docker port CONTAINER [PRIVATE_PORT[/PROTO]]

List port mappings or a specific mapping for the container

Options:
      --help   Print usage
```

使用示例
```
[root@VMCentOS7Lyx ~]# docker port mysqltest
```

#### docker top 显示容器内进程

命令帮助
```
[root@VMCentOS7Lyx ~]# docker help top

Usage:  docker top CONTAINER [ps OPTIONS]

Display the running processes of a container

Options:
      --help   Print usage
[root@VMCentOS7Lyx ~]# 
```