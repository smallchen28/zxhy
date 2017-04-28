# Docker进阶使用

## 导入导出

导入导出功能提供了将容器/镜像和本地文件转换的机制，方便在各机器之间进行迁移。

### 导出(export)

一般步骤是先暂停容器，然后将当前容器做一个快照导出，导出后再unpause

使用示例
```
[root@VMCentOS7Lyx ~]# docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
dd9785729b0f        centos:7            "/bin/bash"              2 days ago          Up 7 seconds                            c7test
0d3c87ed6236        d5127813070b        "docker-entrypoint.sh"   8 days ago          Up 2 days           3306/tcp            mysqltest
[root@VMCentOS7Lyx ~]# docker pause c7test
c7test
[root@VMCentOS7Lyx ~]# docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                       PORTS               NAMES
dd9785729b0f        centos:7            "/bin/bash"              2 days ago          Up About a minute (Paused)                       c7test
0d3c87ed6236        d5127813070b        "docker-entrypoint.sh"   8 days ago          Up 2 days                    3306/tcp            mysqltest
# 将当前容器导出到tar包
[root@VMCentOS7Lyx ~]# docker export c7test > c7.tar
[root@VMCentOS7Lyx ~]# docker unpause c7test
c7test
```

### 保存(save)

将镜像保存为一个tar包

```
[root@VMCentOS7Lyx ~]# docker save --help

Usage:  docker save [OPTIONS] IMAGE [IMAGE...]

Save one or more images to a tar archive (streamed to STDOUT by default)

Options:
      --help            Print usage
  -o, --output string   Write to a file, instead of STDOUT
```

### 导入

将导出的tar包导入为镜像。分为load和import两种机制

```
# 丢弃历史数据和元数据，可以重新指定标签等元数据
[root@VMCentOS7Lyx ~]# docker import --help

Usage:  docker import [OPTIONS] file|URL|- [REPOSITORY[:TAG]]

Import the contents from a tarball to create a filesystem image

Options:
  -c, --change value     Apply Dockerfile instruction to the created image (default [])
      --help             Print usage

# 加载save的tar包为镜像，由于保留了元数据和历史信息，会比export的大些。
[root@VMCentOS7Lyx ~]# docker load --help

Usage:  docker load [OPTIONS]

Load an image from a tar archive or STDIN

Options:
      --help           Print usage
  -i, --input string   Read from tar archive file, instead of STDIN
  -q, --quiet          Suppress the load output
```

## 卷管理

从存储数据和运行程序分离的角度考虑，大量独立的数据应该和容器分开管理。这里提供了两种基本的方法进行数据的管理。

### 数据卷(Data volumes)

数据卷是指在存在于一个或多个容器中的特定目录，此目录能够绕过Union File System提供一些用于持续存储或共享数据的特性。

- 数据卷可在容器之间共享或重用
- 数据卷中的更改可以直接生效
- 数据卷中的更改不会包含在镜像的更新中
- 数据卷默认会一直存在，即使容器被删除

使用示例
```
# 在容器中创建了数据卷/webapp。这个卷会从本机临时分配并给容器挂载？
$ sudo docker run -d -P --name web -v /opt/webapp training/webapp python app.py
# 将宿主机的目录挂载到对应数据卷
$ sudo docker run -d -P --name web -v /src/webapp:/opt/webapp training/webapp python app.py
# 数据卷是只读的
$ sudo docker run -d -P --name web -v /src/webapp:/opt/webapp:ro training/webapp python app.py
# 除了目录还可以挂载单个文件
$ sudo docker run --rm -it -v ~/.bash_history:/.bash_history ubuntu /bin/bash
```

### 数据卷容器(Data volume containers)

如果想要容器之间共享数据，可以通过创建一个专门挂载数据的数据卷容器。将此容器和应用容器配合使用。

使用示例
```
# 创建一个数据卷容器
$ sudo docker run -d -v /dbdata --name dbdata training/postgres echo Data-only container for postgres
# 给多个容器挂载使用
$ sudo docker run -d --volumes-from dbdata --name db1 training/postgres
$ sudo docker run -d --volumes-from dbdata --name db2 training/postgres
# 链式挂载
$ sudo docker run -d --name db3 --volumes-from db1 training/postgres
```

要删在磁盘上删除这个数据卷，只能针对最后一个挂载了数据卷的容器显式地调用docker rm -v命令。

### 数据卷的备份恢复和迁移

通过挂载的方式，可以将容器中的数据备份出来并进行恢复和迁移

使用示例
```
# 启动了一个挂载dbdata数据卷的容器，将dbdata目录打包存到另一个挂载目录下
$ sudo docker run --volumes-from dbdata -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar /dbdata
# 启动新容器并创建了卷
$ sudo docker run -v /dbdata --name dbdata2 ubuntu /bin/bash
# 将打包文件在新容器中解压给dbdata2容器
$ sudo docker run --volumes-from dbdata2 -v $(pwd):/backup busybox tar xvf /backup/backup.tar
```

### 卷单独管理

docker还提供了volume命令单独管理卷

```
[root@VMCentOS7Lyx ~]# docker volume --help

Usage:  docker volume COMMAND

Manage Docker volumes

Options:
      --help   Print usage

Commands:
  create      Create a volume
  inspect     Display detailed information on one or more volumes
  ls          List volumes
  rm          Remove one or more volumes

Run 'docker volume COMMAND --help' for more information on a command.
```

使用示例
```
[root@VMCentOS7Lyx ~]# docker volume ls
DRIVER              VOLUME NAME
local               2865f5e69f3b413428c39855d6603c5abbce24cce92eab3db0b7f6fa0d65ee1c
local               45f77350cc34e5416c8ae53a21e69b4a580f75cfd7c0b74caebe3503e10b6616
[root@VMCentOS7Lyx ~]# docker volume  inspect 45f77350cc34e5416c8ae53a21e69b4a580f75cfd7c0b74caebe3503e10b6616
[
    {
        "Name": "45f77350cc34e5416c8ae53a21e69b4a580f75cfd7c0b74caebe3503e10b6616",
        "Driver": "local",
        "Mountpoint": "/var/lib/docker/volumes/45f77350cc34e5416c8ae53a21e69b4a580f75cfd7c0b74caebe3503e10b6616/_data",
        "Labels": null,
        "Scope": "local"
    }
]
```

## 网络管理

### 网络端口映射

端口映射可以将容器内的服务提供给宿主机及外部使用。docker会使用宿主机的高端口49000到49900。

使用示例
```
# -P参数指定了动态映射
$ sudo docker run -d -P training/webapp python app.py
# 通过命令查看端口映射
$ sudo docker ps nostalgic_morse
CONTAINER ID  IMAGE                   COMMAND       CREATED        STATUS        PORTS                    NAMES
bc533791f3f5  training/webapp:latest  python app.py 5 seconds ago  Up 2 seconds  0.0.0.0:49155->5000/tcp  nostalgic_morse

# 指定端口映射
$ sudo docker run -d -p 5000:5000 training/webapp python app.py
# 指定ip
$ sudo docker run -d -p 127.0.0.1:5001:5002 training/webapp python app.py
$ sudo docker run -d -p 127.0.0.1::5002 training/webapp python app.py

# 绑定UDP端口
$ sudo docker run -d -p 127.0.0.1:5000:5000/udp training/webapp python app.py
```

## 容器连接

docker有一个连接系统允许将多个容器连接在一起，共享连接信息。docker连接会创建一个父子关系，其中父容器可以看到子容器的信息。

连接允许容器之间可见并且安全地进行通信。使用--link创建连接。在此假设一个web容器连接db容器。

使用示例
```
# 创建db容器
$ sudo docker run -d --name db training/postgres
# 创建web容器，并进行连接--link name:alias
$ sudo docker run -d -P --name web --link db:db training/webapp python app.py
# 查看容器连接关系，web是父，db是子关系
$ docker ps
CONTAINER ID  IMAGE                     COMMAND               CREATED             STATUS             PORTS                    NAMES
349169744e49  training/postgres:latest  su postgres -c '/usr  About a minute ago  Up About a minute  5432/tcp                 db
aed84ee21bde  training/webapp:latest    python app.py         16 hours ago        Up 2 minutes       0.0.0.0:49154->5000/tcp  db/web,web
```

你会注意到当你启动db容器的时候我们没有使用-P或者-p标识。docker在容器之间打开一个安全连接隧道不需要暴露任何端口给容器外部。

父容器获取到子容器中相关信息的方法包括环境变量和/etc/hosts配置两种方法。

环境变量，DB_前缀和别名是对应的。这里向web暴露了db相关的属性
```
$ sudo docker run --rm --name web2 --link db:db training/webapp env
        . . .
    DB_NAME=/web2/db
    DB_PORT=tcp://172.17.0.5:5432
    DB_PORT_5000_TCP=tcp://172.17.0.5:5432
    DB_PORT_5000_TCP_PROTO=tcp
    DB_PORT_5000_TCP_PORT=5432
    DB_PORT_5000_TCP_ADDR=172.17.0.5
       . . .
```

hosts配置，指定了IP，则web可以通过ip直接访问db相关服务。
```
root@aed84ee21bde:/opt/webapp# cat /etc/hosts
172.17.0.7  aed84ee21bde
. . .
172.17.0.5  db
```

## 容器管理

### diff

### events

### history

### inspect

### stats

### tag