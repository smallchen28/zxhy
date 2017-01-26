# qemu-kvm虚拟机网络配置

## 简介

qemu中支持的网络模式包括四种

1.基于网桥的虚拟网卡

2.基于NAT的虚拟网络

3.内置的用户模式网络

4.直接分配网络设备的网络(vt-d和sr-iov)

本文主要是对网卡设置相关命令和操作的介绍，具体的原理另外参见虚拟网络原理。

### qemu-kvm和virt-install

这是创建虚机的命令，其中qemukvm是比较底层的创虚机命令，virtinstall是通过libvirt创建虚机的命令。

virt-install具有更友好的交互性，因此本文更多使用virt-install来创建虚机。

qemu命令下网络选项
```
Network options:
-net nic[,vlan=n][,macaddr=mac][,model=type][,name=str][,addr=str][,vectors=v]
                create a new Network Interface Card and connect it to VLAN 'n'
-net user[,vlan=n][,name=str][,net=addr[/mask]][,host=addr][,restrict=on|off]
         [,hostname=host][,dhcpstart=addr][,dns=addr][,dnssearch=domain][,tftp=dir]
         [,bootfile=f][,hostfwd=rule][,guestfwd=rule][,smb=dir[,smbserver=addr]]
                connect the user mode network stack to VLAN 'n', configure its
                DHCP server and enabled optional services
-net tap[,vlan=n][,name=str][,fd=h][,fds=x:y:...:z][,ifname=name][,script=file][,downscript=dfile][,helper=helper][,sndbuf=nbytes][,vnet_hdr=on|off][,vhost=on|off][,vhostfd=h][,vhostfds=x:y:...:z][,vhostforce=on|off][,queues=n]
                connect the host TAP network interface to VLAN 'n'
                use network scripts 'file' (default=/etc/qemu-ifup)
                to configure it and 'dfile' (default=/etc/qemu-ifdown)
                to deconfigure it
                use '[down]script=no' to disable script execution
                use network helper 'helper' (default=/usr/libexec/qemu-bridge-helper) to
                configure it
                use 'fd=h' to connect to an already opened TAP interface
                use 'fds=x:y:...:z' to connect to already opened multiqueue capable TAP interfaces
                use 'sndbuf=nbytes' to limit the size of the send buffer (the
                default is disabled 'sndbuf=0' to enable flow control set 'sndbuf=1048576')
                use vnet_hdr=off to avoid enabling the IFF_VNET_HDR tap flag
                use vnet_hdr=on to make the lack of IFF_VNET_HDR support an error condition
                use vhost=on to enable experimental in kernel accelerator
                    (only has effect for virtio guests which use MSIX)
                use vhostforce=on to force vhost on for non-MSIX virtio guests
                use 'vhostfd=h' to connect to an already opened vhost net device
                use 'vhostfds=x:y:...:z to connect to multiple already opened vhost net devices
                use 'queues=n' to specify the number of queues to be created for multiqueue TAP
-net bridge[,vlan=n][,name=str][,br=bridge][,helper=helper]
                connects a host TAP network interface to a host bridge device 'br'
                (default=br0) using the program 'helper'
                (default=/usr/libexec/qemu-bridge-helper)
-netdev [user|tap|bridge|socket|hubport],id=str[,option][,option][,...]
```

### kvm模拟网卡

查询虚机支持的模拟网卡
```
[root@localhost ~]# /usr/libexec/qemu-kvm -net nic,model=?
qemu: Supported NIC models: ne2k_pci,i82551,i82557b,i82559er,rtl8139,e1000,pcnet,virtio
其中rtl8139是默认的模拟网卡，virtio是半虚机化的实现。
```

创建虚机时指定网络，如果没有进行任何指定将使用第三种模式，相当于 -net nic -net user，模拟的8139网卡。

## 基本使用

### 网桥模式

网桥模式让客户机和宿主机共享一个网卡，客户机通过这个网络连接到宿主机此网卡原来所在的网络，能被外部访问到。
可以通过参数3，4，5三种形式定义虚机使用网桥模式的网卡

tap设备，是一个虚拟网络设备，模拟了一个数据链路层设备（二层）。tap用于创建一个网络桥，在bridge和nat中都要用到。

tun设备，也是一个虚拟网络设备，模拟了网络层设备(三层)

helper参数，设置启动客户机时在宿主机中运行的辅助程序，一般用来建立一个tap虚拟设备，默认参考/usr/libexec/qemu-bridge-helper

#### 准备工作

宿主机上安装相关软件
```
[root@localhost liuyx]# yum install bridge-utils tunctl
[root@localhost liuyx]# lsmod|grep tun
tun                    27183  1 
[root@localhost boot]# ll /dev/net/tun 
crw-rw-rw-. 1 root root 10, 200 Jan 18 16:55 /dev/net/tun
```

#### 创建网桥

手工设置网桥
```
[root@localhost liuyx]# brctl addbr br9 //创建网桥
[root@localhost liuyx]# brctl addif br9 enp3s1 //将网桥与一个正常工作的网卡绑定
[root@localhost liuyx]# brctl stp br9 on //启用stp协议
[root@localhost liuyx]# ifconfig enp3s1 0//将原网卡置0，表示监听全网段？
[root@localhost liuyx]# dhclient br9//从网络中dhcp自动获取ip，也可以通过ifconfig,route命令手工设置静态参数
[root@localhost ~]# ifconfig
br9: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 129.160.0.105  netmask 255.255.255.0  broadcast 129.160.0.255
        inet6 fe80::e205:c5ff:feeb:7cce  prefixlen 64  scopeid 0x20<link>
        ether e0:05:c5:eb:7c:ce  txqueuelen 0  (Ethernet)
        RX packets 2278  bytes 247085 (241.2 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 23  bytes 4139 (4.0 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
[root@localhost ~]# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         129.160.0.2     0.0.0.0         UG    0      0        0 br9
default         129.160.0.2     0.0.0.0         UG    100    0        0 ens33
129.160.0.0     0.0.0.0         255.255.255.0   U     0      0        0 ens33
129.160.0.0     0.0.0.0         255.255.255.0   U     0      0        0 br9
192.168.122.0   0.0.0.0         255.255.255.0   U     0      0        0 virbr0
[root@localhost ~]# brctl show
bridge name     bridge id               STP enabled     interfaces
br9             8000.e005c5eb7cce       yes             enp3s1
virbr0          8000.525400f8136d       yes             virbr0-nic
```

#### 创建虚机

创建虚机，使用此前配置的网桥
```
[root@localhost ~]# qemu-kvm test.img -net nic -net tap,ifname=vnet0 //启动带网桥的虚机
[root@localhost liuyx]# brctl show
bridge name     bridge id               STP enabled     interfaces
br9             8000.e005c5eb7cce       yes             enp3s1
                                                        vnet0
virbr0          8000.525400f8136d       yes             virbr0-nic

//虚机中的网络和宿主机中的共享网卡一般具有类似的配置
virt-install --virt-type=kvm --name c7 --ram=1024 --disk path=/image/centos.img --network bridge=br9 --graphics vnc,listen=0.0.0.0 --noautoconsole 
```

### NAT模式

libvirt安装后，默认会生成一个virbr0的网卡，地址为192.168.122.1。可以理解为一个虚拟交换机(网关?)，挂接到此网络下的虚机网卡将在此小网下，通过宿主机的dhcp服务动态获取ip或手工静态配置。

客户机启动后将获得小网地址，如果要正确访问外部网络，需要配置/etc/resolv.conf找到dns服务。

#### 创建虚机
```
virt-install --virt-type=kvm --name zxdb2 --ram=6144 --disk path=/image/zxdb2.img,format=qcow2 --network network=default
[root@7fd3cfe2329b4f11b5c277dbea789b1e ~]# brctl show
bridge name     bridge id               STP enabled     interfaces
br0             8000.744aa4008a10       yes             enp3s0f3
virbr0          8000.525400649ffe       yes             virbr0-nic
                                                        vnet1.0
```

#### 添加端口映射

iptables提供端口映射功能，能让外部访问此内部机器
```
[root@localhost ~]# iptables -t nat -L
[root@localhost ~]# iptables -t nat -A PREROUTING -p tcp -d \ 10.43.17.99 --dport 19922 -j DNAT --to 192.168.122.199:22
//这样的配置将宿主机上19922端口映射到虚机22端口上，实现了从外部直接ssh访问虚机的功能。
```

### virtio_net

在选择kvm中的网络设备时，一般应优先选择半虚拟化设备而不是使用纯软件模拟。可以提高网络吞吐量和降低网络延迟，能达到和原生网络基本相当的性能。

要使用virtionet需要两部分支持，宿主机中qemu的支持和客户机中virtionet驱动的支持，2.6.32后的linux内核支持，而win系统需要另外安装。

#### 显示model
```
//如下命令显示了两个虚机使用的网络类型和模拟的网卡，分别是半虚拟化和rt8139的。
virsh # domiflist c7
Interface  Type       Source     Model       MAC
-------------------------------------------------------
-          network    br0        virtio      52:54:00:49:7d:8a
virsh # domiflist zxdb
Interface  Type       Source     Model       MAC
-------------------------------------------------------
-          bridge     br9        rtl8139     52:54:00:b8:c2:b0

//在客户机上执行可以看到该网卡是否半虚拟化的
[root@localhost ~]# lspci
00:03.0 Ethernet controller: Red Hat, Inc Virtio network device
```

### VT-d(virtualization technology for directed I/O)

intel定义的IO虚拟化技术规范，较新的X86平台都已经支持。

运行在支持vt-d平台上的qemu/kvm可以分配网卡，磁盘，usb，vga设备供客户机直接使用，因此具有更好的IO性能。

#### 准备工作

需要硬件设备支持，内核打开vtd。一般默认安装都支持，如果没有打开，在GRUB的kernel行中加入intel_iommu=on这个内核启动项

显示设备信息
```
[root@localhost ~]# virsh nodedev-list --tree
computer
  |
  +- net_lo_00_00_00_00_00_00
  +- net_virbr0_nic_52_54_00_f8_13_6d
  +- pci_0000_00_00_0
  +- pci_0000_00_02_0
  +- pci_0000_00_1b_0
  +- pci_0000_00_1c_0
  +- pci_0000_00_1c_1
  |   |
  |   +- pci_0000_02_00_0
  |       |
  |       +- net_ens33_90_fb_a6_03_7f_09
  |         
  +- pci_0000_00_1e_0
  |   |
  |   +- pci_0000_03_01_0  ////可以看到此处对应的网卡设备
  |   |   |
  |   |   +- net_enp3s1_e0_05_c5_eb_7c_ce
  |   |     
  |   +- pci_0000_03_02_0
  |       |
  |       +- net_enp3s2_e0_05_c5_eb_a9_ee
  |   

[root@localhost drivers]# lspci -Dn -s 03:02.0 查看设备的vendorid和deviceid
0000:03:02.0 0200: 10ec:8139 (rev 10)
domain:bus:slot:function///一般后面三个值用BDF(bus:device:function)简称。输出信息中10ec是vendorid，8139是devid  
```

#### 隐藏PCI设备

```
将对应设备从主机上解除或重新挂载
[root@7fd3cfe2329b4f11b5c277dbea789b1e ~]# virsh nodedev-dettach pci_0000_03_00_3
Device pci_0000_03_00_3 detached
[root@7fd3cfe2329b4f11b5c277dbea789b1e image]# virsh nodedev-reattach pci_0000_03_00_3
Device pci_0000_03_00_3 re-attached
```

#### 虚机使用此设备

解挂后将设备直接分配给虚机
```
[root@7fd3cfe2329b4f11b5c277dbea789b1e image]# virt-install --virt-type=kvm --name c7 --ram=4096 --disk path=/image/centos.img --network none --graphics vnc,listen=0.0.0.0 --noautoconsole --boot hd --os-type=linux --os-variant=rhel7 --hostdev pci_0000_03_00_3

//在客户机上可以直接看到此设备
[root@localhost ~]# lspci|grep Eth
00:06.0 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)

//在虚机的xml定义中可以看到对应的配置
    <hostdev mode='subsystem' type='pci' managed='yes'>
      <source>
        <address domain='0x0000' bus='0x03' slot='0x00' function='0x3'/>
      </source>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/>
    </hostdev>

//可以看到被虚机使用后的设备驱动是不同的
[root@7fd3cfe2329b4f11b5c277dbea789b1e image]# lspci -k -s 03:00.3 
03:00.3 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
        Kernel driver in use: vfio-pci
        Kernel modules: igb
[root@7fd3cfe2329b4f11b5c277dbea789b1e image]# lspci -k -s 03:00.2
03:00.2 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
        Kernel driver in use: igb
        Kernel modules: igb
```

### SR-IOV技术

该规范定义了一个标准化的机制用来原生的支持多个共享的设备，比vt-d的独占设备更有优势。

#### 准备工作

确定设备是否支持，一般只有中高端网卡支持
```
[root@7fd3cfe2329b4f11b5c277dbea789b1e ~]# lspci -v -s 03:00.0  查看对应的pci设备确定设备是否支持
03:00.0 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
        Physical Slot: 0-2
        Flags: bus master, fast devsel, latency 0, IRQ 77, NUMA node 0
        Memory at 93060000 (32-bit, non-prefetchable) [size=128K]
        I/O ports at 3060 [size=32]
        Memory at 9308c000 (32-bit, non-prefetchable) [size=16K]
        Capabilities: [40] Power Management version 3
        Capabilities: [50] MSI: Enable- Count=1/1 Maskable+ 64bit+
        Capabilities: [70] MSI-X: Enable+ Count=10 Masked-
        Capabilities: [a0] Express Endpoint, MSI 00
        Capabilities: [100] Advanced Error Reporting
        Capabilities: [140] Device Serial Number 74-4a-a4-ff-ff-00-8a-0d
        Capabilities: [150] Alternative Routing-ID Interpretation (ARI)
        Capabilities: [160] Single Root I/O Virtualization (SR-IOV)
        Capabilities: [1a0] Transaction Processing Hints
        Capabilities: [1c0] Latency Tolerance Reporting
        Capabilities: [1d0] Access Control Services
        Kernel driver in use: igb
        Kernel modules: igb

[root@7fd3cfe2329b4f11b5c277dbea789b1e ~]# modinfo igb 查看igb驱动的信息
filename:       /lib/modules/3.10.0-514.el7.x86_64/kernel/drivers/net/ethernet/intel/igb/igb.ko
version:        5.3.0-k
license:        GPL
description:    Intel(R) Gigabit Ethernet Network Driver
author:         Intel Corporation, <e1000-devel@lists.sourceforge.net>
rhelversion:    7.3
srcversion:     FAD286C6DDDCF6F7207E580
parm:           max_vfs:Maximum number of virtual functions to allocate per physical function (uint)
parm:           debug:Debug level (0=none,...,16=all) (int)
```

#### 创建vf

```
//重新加载驱动，设置vfs开启vf
[root@7fd3cfe2329b4f11b5c277dbea789b1e ~]#rmmod igb
[root@7fd3cfe2329b4f11b5c277dbea789b1e ~]#modprobe igb max_vfs=7
//或者修改启动加载时的参数
[root@e7e075eedc924227a0254d212df133e0 modprobe.d]# cat /etc/modprobe.d/tecs-sriov.conf
# default config the numbers of virtual function in using SR-IOV.
options igb max_vfs=2

//可以看到每个pf设备对应了两个vf设备
[root@7fd3cfe2329b4f11b5c277dbea789b1e ~]# lspci|grep Eth
03:00.0 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
03:00.1 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
03:00.2 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
03:00.3 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
03:10.0 Ethernet controller: Intel Corporation I350 Ethernet Controller Virtual Function (rev 01)
03:10.1 Ethernet controller: Intel Corporation I350 Ethernet Controller Virtual Function (rev 01)
03:10.2 Ethernet controller: Intel Corporation I350 Ethernet Controller Virtual Function (rev 01)
03:10.3 Ethernet controller: Intel Corporation I350 Ethernet Controller Virtual Function (rev 01)
03:10.4 Ethernet controller: Intel Corporation I350 Ethernet Controller Virtual Function (rev 01)
03:10.5 Ethernet controller: Intel Corporation I350 Ethernet Controller Virtual Function (rev 01)
03:10.6 Ethernet controller: Intel Corporation I350 Ethernet Controller Virtual Function (rev 01)
03:10.7 Ethernet controller: Intel Corporation I350 Ethernet Controller Virtual Function (rev 01)
06:00.0 Ethernet controller: Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection (rev 01)
06:00.1 Ethernet controller: Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection (rev 01)

//显示物理设备和虚拟设备之间的对应关系
[root@7fd3cfe2329b4f11b5c277dbea789b1e 0000:03:00.0]# ll /sys/bus/pci/devices/0000\:03\:00.0/virtfn*
lrwxrwxrwx 1 root root 0 Jan 24 18:14 /sys/bus/pci/devices/0000:03:00.0/virtfn0 -> ../0000:03:10.0
lrwxrwxrwx 1 root root 0 Jan 24 18:14 /sys/bus/pci/devices/0000:03:00.0/virtfn1 -> ../0000:03:10.4
[root@7fd3cfe2329b4f11b5c277dbea789b1e 0000:03:00.0]# ll /sys/bus/pci/devices/0000\:03\:10.4/physfn
lrwxrwxrwx 1 root root 0 Jan 24 18:14 /sys/bus/pci/devices/0000:03:10.4/physfn -> ../0000:03:00.0
```
#### 使用VF

将vf设备按照VT-d的方式直接分配给对应虚机。