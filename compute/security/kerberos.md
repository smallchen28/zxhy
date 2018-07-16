kerberos

## 简介

Kerberos是由美国麻省理工学院提出的基于可信赖的第三方的认证系统。

Kerberos提供了一种在开放式网络环境下进行身份认证的方法,它使网络上的用户可以相互证明自己的身份。

Kerberos采用对称密钥体制对信息进行加密。其基本思想是：能正确对信息进行解密的用户就是合法用户。

用户在对应用服务器进行访问之前，必须先从第三方（Kerberos服务器）获取该应用服务器的访问许可证（ticket）。

## 基本原理

### 名词解释

- KDC：即Key Distribution Center, 密钥分发中心，负责颁发凭证。包含AS和TGS两部分。

- AS：authentication service验证服务器，为client生成TGT

- TGS：ticket granting service授权服务器，为client生成最终的ticket

- TGT：ticket-granting ticket，获取最终ticket过程中的秘钥

- Kinit：Kerberos认证命令，可以使用密码或者Keytab。

- Realm：Kerberos的一个管理域，同一个域中的所有实体共享同一个数据库

- Principal：Kerberos主体，即我们通常所说的Kerberos账号(name@realm) ，可以为某个服务或者某个用户所使用 

- Keytab：以文件的形式呈现，存储了一个或多个Principal的长期的key，用途和密码类似，用于kerberos认证登录；其存在的意义在于让用户不需要明文的存储密码，和程序交互时不需要人为交互来输入密码。

- Client master key: KDC中存储的Client的密钥，下面称为cmk

- Server master key: KDC中存储的Server的密钥，下面称为smk

### 认证流程

1.client向AS请求，通过principal和keytab。AS确认了client已配置在白名单中，产生一个有时效的随机TGT，并将TGT使用对应cmk加密返回。

2.client用本地秘钥cmk解开TGT，用TGT加密客户端信息并向TGS请求某服务的ticket

3.TGS接收请求，确认client具有访问某server的权限。向client返回用smk加密的客户端信息和TGT(A部分)。

4.client将客户端信息用TGT加密(B部分)连同A部分分别传递给server端。

5.server端用本地秘钥smk解开A部分，再用A里的TGT解开B部分进行对比。server向client发出最终成功应答

6.client和server之间后续消息交互将通过TGT加密。


为什么要采用3步交互的形式来完成安全认证

kerberos使用场景是服务端/客户端需要互相认证的应用，引入KAS就是通过第三方平台完成互信。

如何确定客户端是可信任的？

首先client向as请求有初步的认证，第二client需要cmk才能解开as的应答，最后server收到了A/B两份信息，进行对比才最终确认客户端。

如何确定服务端是可信任的？

服务端接收的A部分，只有密码正确才能解开获得TGT，后续向客户端应答才能继续。

为什么要有TGT？

cmk/smk一般都是长期不变的，传递用cmk/smk加密的数据包理论上存在被截获后暴力破解的可能。tgt是有时效性的加密秘钥。

为什么要用时间戳？

和可靠性机制有关，还没完全理解。

## 实际应用

## 一些网址

[kerberos官网](http://web.mit.edu/kerberos/)

[kerberos认证流程详解](https://blog.csdn.net/jewes/article/details/20792021)

[kerberos认证原理](https://blog.csdn.net/wulantian/article/details/42418231)