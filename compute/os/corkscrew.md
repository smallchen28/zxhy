# Corkscrew代理工具

## 简介

Corkscrew是专门为ssh提供http代理的软件，要使用corkscrew需要http代理支持HTTP CONNECT方法，建议使用squid或者ATS这类专业的代理软件，代理不建议设置认证

## 使用

### 安装

下载
```
wget http://agroman.net/corkscrew/corkscrew-2.0.tar.gz
```
编译安装
```
./configure
make && make install
```

### 连接

使用SSH通过HTTP代理连接远程服务器

基本格式：

```
ssh user@server -o "ProxyCommand corkscrew 代理地址 代理端口 ssh服务器地址 ssh端口 "
```

通过公司http代理连接到yj的服务器上
```
[root@db1 ~]# ssh -p9022 root@a.b.c.d -o "ProxyCommand corkscrew proxy.ttcom.cn 80 a.b.c.d 9022"
root@a.b.c.d's password: 
Last login: Thu Mar 16 09:30:18 2017 from e.f.g.h
[root@VMCentOS7Lyx ~]# 
[root@VMCentOS7Lyx ~]# 
[root@VMCentOS7Lyx ~]# ifconfig
```

通过配置文件简化输入

主要参考ssh命令中-o参数说明
```
-o option
    Can be used to give options in the format used in the configuration file.  This is useful for specifying options for which there is no separate command-line flag.  For full details of the options listed below, and their possible values, see ssh_config(5).
```

修改/etc/ssh/ssh_config文件
```
Host 52os  #别名，可以不设置
Hostname server.52os.net  #域名或者ip
User root
Port 2862
#IdentityFile 证书路径
ProxyCommand corkscrew proxy.52os.net 8080  %h %p

直接执行
ssh 52os
```

## ssh over socks

corkscrew不支持socks代理，如果是socks代理要使用nc(netcat/ncat)，或者其它支持socks的软件，配置和上面类似：

ProxyCommand nc -X 5 -x socks5.52os.net:1080 %h %p

nc非常强大，我的http代理支持CONNECT方法，即能打开https的网站，也可以用nc代替corkscrew：

ProxyCommand nc -X connect -x proxy.52os.net:8080 %h %p

个人更喜欢用nc，因为各发行版的包管理中都有，使用起比方便。proxycommand 命令相当的灵活，不只是http和socks代理，如果有其它形式的代理,只要有客户端支持都可以用