# GPT和parted

## GPT

全局唯一标识分区表（GUID Partition Table，缩写：GPT）是一个实体硬盘的分区结构。是源自EFI标准的一种较新的磁盘分区表结构的标准，是未来磁盘分区的主要形式。

与MBR分区方式相比，具有如下优点：
- 突破MBR 4个主分区限制；
- 向后兼容MBR；
- 每个磁盘最多支持128个分区。支持大于2T的分区，最大卷可达18EB；
- Mac、LInux系统、Windows 7 64bit、Windows Server2008 64bit都能支持GPT分区格式。 

当然，GPT也有它的限制：
- 底层硬件必须支持UEFI（Intel提出的取代BIOS的新一代的引导系统）才能使用，
- 必须使用64位操作系统。

## parted

### [官方网站](http://www.gnu.org/software/parted/)

### 命令模式

parted [选项] <硬盘设备名> <子命令> [<子命令参数>]

子命令表
| 子命令 | 说明 |
|--------|--------|
|help [COMMAND]|打印命令的帮助信息，或指定命令的帮助信息|
|print [free|NUMBER|all]|显示分区表, 指定编号的分区, 或所有设备的分区表|
|mkpart PART-TYPE [FSTYPE] START END|创建新分区。PART-TYPE 是以下类型之一：primary（主分 区）、extended（扩展分区）、logical（逻辑分区）。START 和 END 是新分区开始和结束的具体位置。|
|set NUMBER FLAG STATE|对指定编号 NUMBER 的分区设置分区标记 FLAG。对于 PC 常用的 msdos 分区表来说，分区标记 FLAG 可有如下值：”boot”（引导）, “hidden”（隐藏）, “raid”（软RAID磁盘阵）, “lvm”（逻辑卷）, “lba” （LBA，Logic Block Addressing模式）。 状态STATE 的取值是：on 或 off|
|unit UNI|设置默认输出时表示磁盘大小的单位为 UNIT，UNIT 的常用取值可以为：‘MB’、‘GB’、‘%’（占整个磁盘设备的百分之多少）、‘compact’（人类易读方式，类似于 df 命令中 -h 参数的用）、‘s’（扇区）、‘cyl’ （柱面）、‘chs’ （柱面cylinders:磁头 heads:扇区 sectors 的地址）|
|cp [FROM-DEVICE] FROM-NUMBER TONUMBER|将分区 FROM-NUMBER 上的文件系统完整地复制到分区TO-NUMBER 中，作为可选项还可以指定一个来源硬盘的设备名称FROM-DEVICE，若省略则在当前设备上进行复制|
|move NUMBER START END|将指定编号 NUMBER 的分区移动到从 START 开始 END 结束的位置上。注意：（1）只能将分区移动到空闲空间中。（2）虽然分区被移动了，但它的分区编号是不会改变的|
|resize NUMBER START END|对指定编号 NUMBER 的分区调整大小。分区的开始位置和结束位置由 START 和 END 决定|
|rm NUMBER|删除指定编号 NUMBER 的分区。|
|check NUMBER|检查指定编号 NUMBER 分区中的文件系统是否有什么错误|
|rescue START END|恢复靠近位置 START 和 END 之间的分区|
|mklabel,mktable LABELTYPE|创建一个新的 LABEL-TYPE 类型的空磁盘分区表，对于PC而言 msdos 是常用的 LABELTYPE。 若是用 GUID 分区表，LABEL-TYPE 应该为 gpt|


### 交互模式

parted [选项] <硬盘设备名>

示例
```
[root@zxdb136 ~]# parted /dev/sdb 
GNU Parted 3.1
Using /dev/sdb
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) print                                                            
Model: TOSHIBA AL14SEB090N (scsi)
Disk /dev/sdb: 900GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: pmbr_boot

Number  Start  End  Size  File system  Name  Flags

(parted)
(parted) mkpart                                                           
Partition name?  []? root                                                 
File system type?  [ext2]? ext4                                                                                                            
Start? 1                                                                  
End? 400G
(parted) print free                                                       
Model: TOSHIBA AL14SEB090N (scsi)
Disk /dev/sdb: 900GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: pmbr_boot

Number  Start   End     Size    File system  Name  Flags
        17.4kB  1049kB  1031kB  Free Space
 1      1049kB  400GB   400GB   ext4         root
        400GB   900GB   500GB   Free Space
```
