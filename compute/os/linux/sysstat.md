sysstat

## 简介

SYSSTAT是一个软件包，包含监测系统性能及效率的一组工具，这些工具对于我们收集系统性能数据，比如CPU使用率、硬盘和网络吞吐数据，

这些数据的收集和分析，有利于我们判断系统是否正常运行，是提高系统运行效率、安全运行服务器的得力助手

下表是包含在sysstat包中的工具

- iostat: 输出CPU的统计信息和所有I/O设备的输入输出（I/O）统计信息。
- mpstat: 关于CPU的详细信息（单独输出或者分组输出）。
- pidstat: 关于运行中的进程/任务、CPU、内存等的统计信息。
- sar: 保存并输出不同系统资源（CPU、内存、IO、网络、内核等。。。）的详细信息。
- sadc: 系统活动数据收集器，用于收集sar工具的后端数据。
- sa1: 系统收集并存储sadc数据文件的二进制数据，与sadc工具配合使用
- sa2: 配合sar工具使用，产生每日的摘要报告。
- sadf: 用于以不同的数据格式（CVS或者XML）来格式化sar工具的输出。
- Sysstat: sysstat工具的man帮助页面。
- nfsiostat: NFS（Network File System）的I/O统计信息。
- cifsiostat: CIFS(Common Internet File System)的统计信息。

### [官方文档](http://sebastien.godard.pagesperso-orange.fr/documentation.html)

## iostat

iostat用于输出CPU和磁盘I/O相关的统计信息

iostat  [  -c ] [ -d ] [ -h ] [ -k | -m ] [ -N ] [ -t ] [ -V ] [ -x ] [ -y ] [ -z ] [ -j { ID | LABEL | PATH | UUID | ... } ] [ [ -T ] -g group_name ] [ -p [ device
       [,...] | ALL ] ] [ device [...] | ALL ] [ interval [ count ] ]

主要参数

-c 仅显示cpu统计

-d 仅显示设备统计

-k/M 字节显示单位

-N 显示磁盘阵列(LVM)信息

-p 指定设备

-y 清除第一个统计包含系统启动后总数据
 
-x 输出扩展信息

示例
```
# 指定设备，显示还包括时间，扩展信息
[root@db2 ~]# iostat -d -x -t -p vdb 2 4
Linux 3.10.0-123.el7.x86_64 (db2)       01/04/2018      _x86_64_        (4 CPU)

01/04/2018 10:29:48 AM
Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
vdb               0.00     0.00    0.00    0.00     0.00     0.00     8.00     0.00    0.75    0.75    0.00   0.75   0.00

01/04/2018 10:29:50 AM
Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
vdb               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00    0.00    0.00   0.00   0.00

01/04/2018 10:29:52 AM
Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
vdb               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00    0.00    0.00   0.00   0.00

01/04/2018 10:29:54 AM
Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
vdb               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00    0.00    0.00   0.00   0.00

# 清除历史统计
[root@db2 ~]# iostat -d -y 2 10
Linux 3.10.0-123.el7.x86_64 (db2)       01/04/2018      _x86_64_        (4 CPU)

Device:            tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
vda               0.00         0.00         0.00          0          0
vdb               0.00         0.00         0.00          0          0
dm-0              0.00         0.00         0.00          0          0
dm-1              0.00         0.00         0.00          0          0

Device:            tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
vda               0.00         0.00         0.00          0          0
vdb               0.00         0.00         0.00          0          0
dm-0              0.00         0.00         0.00          0          0
dm-1              0.00         0.00         0.00          0          0

Device:            tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
vda               0.00         0.00         0.00          0          0
vdb               0.00         0.00         0.00          0          0
dm-0              0.00         0.00         0.00          0          0
dm-1              0.00         0.00         0.00          0          0
```

## mpstat

mpstat [ -A ] [ -u ] [ -V ] [ -I { SUM | CPU | SCPU | ALL } ] [ -P { cpu [,...] | ON | ALL } ] [ interval [ count ] ]

显示处理器统计信息。不带任何参数的使用mpstat命令将会输出所有CPU的平均统计信息一次

主要参数

-A 等于 -u -I ALL -P ALL

-u 报告cpu的各统计项，说明见最后

-P 指定处理器

-I 中断统计

示例
```
# 间隔2秒统计6次
[root@db2 ~]# mpstat 2 6
Linux 3.10.0-123.el7.x86_64 (db2)       01/03/2018      _x86_64_        (4 CPU)

04:12:24 PM  CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
04:12:26 PM  all    0.25    0.00    0.13    0.00    0.00    0.00    0.00    0.00    0.00   99.62
04:12:28 PM  all    0.25    0.00    0.13    3.00    0.00    0.00    0.00    0.00    0.00   96.62
04:12:30 PM  all    0.38    0.00    0.13    0.00    0.00    0.00    0.00    0.00    0.00   99.50
04:12:32 PM  all    0.38    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00   99.62
04:12:34 PM  all    0.25    0.00    0.25    0.00    0.00    0.00    0.00    0.00    0.00   99.50
04:12:36 PM  all    0.25    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00   99.75
Average:     all    0.29    0.00    0.10    0.50    0.00    0.00    0.00    0.00    0.00   99.10

# 只显示最后一个cpu
[root@db1 ~]# mpstat -u -P 3
Linux 3.10.0-123.el7.x86_64 (db1)       01/03/2018      _x86_64_        (4 CPU)

04:08:11 PM  CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
04:08:11 PM    3    1.14    0.01    0.83    0.05    0.00    0.00    0.00    0.00    0.00   97.98
```

## pidstat

pidstat [ -d ] [ -h ] [ -I ] [ -l ] [ -r ] [ -s ] [ -t ] [ -U [ username ] ] [ -u ] [ -V ] [ -w ] [ -C comm ] [ -p { pid [,...] | SELF | ALL } ] [ -T { TASK | CHILD
       | ALL } ] [ interval [ count ] ]

该命令是用于监控进程和当前受内核管理的线程。pidstat还可以检查子进程和线程的状态。

主要参数

-C 只显示匹配字符的命令，字符串可以是正则表达式

-d 包括io统计

-p 指定进程

-r 包括内存统计

-s 包括栈统计

-u 包括cpu统计

-U 将uid转换为用户名，如果指定用户名则显示对应用户的 

示例
```
# 对mysqld的io进行统计
[root@ctrl6 ~]# pidstat -d -p 20336 2 4
Linux 3.10.0-327.22.2.el7.x86_64 (ctrl6)        01/03/2018      _x86_64_        (40 CPU)

04:36:13 PM   UID       PID   kB_rd/s   kB_wr/s kB_ccwr/s  Command
04:36:15 PM    27     20336      0.00     16.00     16.00  mysqld
04:36:17 PM    27     20336      0.00      0.00      0.00  mysqld
04:36:19 PM    27     20336      0.00      0.00      0.00  mysqld
04:36:21 PM    27     20336      0.00      0.00      0.00  mysqld
Average:       27     20336      0.00      4.00      4.00  mysqld

# 按命令匹配显示指定进程的内存统计
[root@db1 ~]# pidstat -r -C http
Linux 3.10.0-123.el7.x86_64 (db1)       01/03/2018      _x86_64_        (4 CPU)

04:39:57 PM   UID       PID  minflt/s  majflt/s     VSZ    RSS   %MEM  Command
04:39:57 PM    48     12489      0.00      0.00  158136   6312   0.08  httpd
04:39:57 PM    48     12490      0.00      0.00  158136   6312   0.08  httpd
04:39:57 PM    48     12491      0.00      0.00  158136   6312   0.08  httpd
04:39:57 PM    48     12492      0.00      0.00  158136   6312   0.08  httpd
04:39:57 PM    48     12493      0.00      0.00  158136   6312   0.08  httpd
04:39:57 PM    48     12494      0.00      0.00  158136   6312   0.08  httpd
04:39:57 PM    48     12495      0.00      0.00  158136   6312   0.08  httpd
04:39:57 PM    48     12507      0.00      0.00  158136   6312   0.08  httpd
04:39:57 PM     0     23574      0.01      0.00  153884   5092   0.06  httpd
[root@db1 ~]# 
```

## sar

System Activity Reporter系统活动情况报告是目前 Linux 上最为全面的系统性能分析工具之一，可以从多方面对系统的活动进行报告，

包括：文件的读写情况、系统调用的使用情况、磁盘I/O、CPU效率、内存使用状况、进程活动及IPC有关的活动等。

Usage: sar [ options ] [ <interval> [ <count> ] ]
Options are:
[ -A ] [ -B ] [ -b ] [ -C ] [ -d ] [ -H ] [ -h ] [ -p ] [ -q ] [ -R ]
[ -r ] [ -S ] [ -t ] [ -u [ ALL ] ] [ -V ] [ -v ] [ -W ] [ -w ] [ -y ]
[ -I { <int> [,...] | SUM | ALL | XALL } ] [ -P { <cpu> [,...] | ALL } ]
[ -m { <keyword> [,...] | ALL } ] [ -n { <keyword> [,...] | ALL } ]
[ -j { ID | LABEL | PATH | UUID | ... } ]
[ -f [ <filename> ] | -o [ <filename> ] | -[0-9]+ ]
[ -i <interval> ] [ -s [ <hh:mm:ss> ] ] [ -e [ <hh:mm:ss> ] ]

重要参数

-b 物理设备的io和传输速率统计

-d 块设备统计

-m 电源管理统计

-n 网络统计

-u cpu统计

-r 内存和交换空间统计

-R 内存统计

-q 队列和负载统计

-P 指定cpu

-S 交换分区统计

-v inode、文件和其他内核表统计

-y 终端tty设备统计

-f 读取的统计文件，默认为/var/log/sa/sar[dd]

-o 输出的统计文件

示例
```
# 显示某网络接口的统计
[root@ctrl6 sa]# sar -n DEV 1 5|grep ens12f0
05:09:20 PM   ens12f0   6516.00  12056.00    470.85  16037.58      0.00      0.00      1.00
05:09:21 PM   ens12f0    958.00    740.00    668.61    340.85      0.00      0.00      9.00
05:09:22 PM   ens12f0   1369.00   1411.00    594.46   1102.71      0.00      0.00      3.00
05:09:23 PM   ens12f0   1079.00    802.00    682.80    293.00      0.00      0.00      2.00
05:09:24 PM   ens12f0    616.00    709.00    128.54    529.39      0.00      0.00      3.00
Average:      ens12f0   2107.60   3143.60    509.05   3660.71      0.00      0.00      3.60

# cpu使用统计，和mpstat类似，同时将结果输出到test文件
[root@db1 ~]# sar -u -o test 10 3
Linux 3.10.0-123.el7.x86_64 (db1)       01/03/2018      _x86_64_        (4 CPU)

05:22:08 PM     CPU     %user     %nice   %system   %iowait    %steal     %idle
05:22:18 PM     all      1.80      0.00      1.50      1.40      0.00     95.29
05:22:28 PM     all      0.03      0.03      0.07      0.47      0.00     99.40
05:22:38 PM     all      1.88      0.00      1.65      0.15      0.00     96.32
Average:        all      1.23      0.01      1.08      0.68      0.00     97.01

# 块设备操作统计
[root@db1 ~]# sar -d -p 3 3 
Linux 3.10.0-123.el7.x86_64 (db1)       01/03/2018      _x86_64_        (4 CPU)

05:26:38 PM       DEV       tps  rd_sec/s  wr_sec/s  avgrq-sz  avgqu-sz     await     svctm     %util
05:26:41 PM       vda      4.67      0.00     50.67     10.86      0.45     96.43     10.00      4.67
05:26:41 PM       vdb      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
05:26:41 PM       vdc      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
05:26:41 PM       vdd      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
05:26:41 PM       vde      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
05:26:41 PM vg_sys-lv_swap      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
05:26:41 PM vg_sys-lv_root      6.33      0.00     50.67      8.00      0.48     75.47      7.37      4.67
05:26:41 PM vg_home-lvol0      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
```

## sadc/sa1/sa2/sadf
