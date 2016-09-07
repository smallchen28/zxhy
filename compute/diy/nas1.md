# 四盘位8核16线程128GBDDR4内存NAS

本文转自https://www.chiphell.com/thread-1356741-1-1.html

主机品牌：Supermicro（超微）

主机型号：SuperServer 5028D-TN4T

内存品牌：Samsung（三星）

内存型号：M393A4K40BB0（单条容量32GB 288pin DDR4 REG ECC）

**为什么入这货？**

在家里提供Windows文件共享服务；顺便运行几（十）个虚拟机玩玩。

之前的装备：

HP MicroServer Gen8。

这玩意儿让我深深的意识到即使是家用，iLO之类的硬件级远程控制功能也是非常必要的。
可以开机之后扔到角落里，通过网络随时的折腾，而不用为了装个操作系统什么的需要满地找显示器、键盘什么的。

唯一美中不足的是这玩意只有两条DDR3 UDIMM（Unbuffered ECC）内存槽，这种内存现在最大的单条容量只有8GB，两条也才16GB。在CPU i3-3220T的情况下，运行三四个虚拟机之后，CPU的性能还有富余，内存已经告急了。再加上MS SQL Server，稍微一运行查询什么的，内存几乎满载。

大致需求是这样的，需要同时满足下述条件，不能部分满足：

  体积与MicroServer Gen8相当；
  带有完整IPMI功能（IPMI是硬件级远程控制的通称，惠普的叫iLO，戴尔的叫RAC……）；
  可以安装更大内存的主板或主机，32GB，64GB或者更大……show版有个“狂魔”，16*16GB=256GB的主机，口水啊

注意，是（1）&（2）&（3）。

于是苦苦寻觅：

Plan A：单条容量16GB的UDIMM内存条，无解；转而尝试

Plan B：四内存槽的ITX主板带，几乎无解。

之所以说“几乎无解”，是因为上面的Plan B将我引领到了Supermicro和ASRock的几个“小强”级别的特殊主板上：
比如ASRock的C2750D4I以及Supermicro的A1SRi-2758F等，这些都是四内存槽基于Atom CPU的mini ITX主板。内存都可以轻松上64GB，不过Atom C2758F、C2750之类的性能大体与i3-3220T相当或稍低。

**Supermicro和ASRock两个牌子各有利弊：**

Supermicro有完整的SuperServer产品出售，包括机箱、热插拔笼子、背板、主板、电源等组成的准系统服务器，做工靠谱，所有配件都是服务器级别的产品，品质容易量化，不用看实物也可以放心下单，全球海淘。

ASRock则仅有主板；

四盘位机箱目前只有山寨牌子，做工太不靠谱；热插拔笼子和小电源更是难找。
这里说的不靠谱、难找等是指：难以量化，很难坐在电脑前全球比价、远程下单。因为都是些杂牌、小牌，其做工无法与惠普的MicroServer Gen8相提并论。甚至于都不如Abee的品质靠谱。

有鉴于此，不考虑纯DIY方案。

准备在Supermicro的SuperServer准系统中选一个。

关于Supermicro的SuperServer：
SuperServer的Mimi-Tower系列中有两个四盘位小机箱带IPMI的型号：

 - 5028A-TN4，Atom C2758F，4x DDR3笔记本纯ECC内存，4x 千兆网卡。
 - 5028D-TN4T，Xeon D-1540，4x DDR4 REG ECC内存，2x 万兆网卡，2x 千兆网卡。


经过考虑，最终选择的是5028D-TN4T。原因有两个：

一是16GB单条的DDR3笔记本纯ECC内存难买，全球只有一个型号，而且价格和DDR4的32GB单条几乎一样。

二是Xeon D-1540是8核心16线程，理论性能和i7-4790K相当；Atom C2758F则是8核心8线程，理论性能略低于i3-3220T。

**5028D-TN4T准系统：**

包括下述部件（所有部件均为Supermicro原厂，品质杠杠的）：

    主板：MBD-X10SDV-TLN4F，含集成CPU D-1540；
    机箱：CSE-721TQ-250B，含四盘位热插拔笼子，体积14L（Gen8体积为13L）；
    背板：CSE-SAS-733TQ，四口热插拔SAS/SATA背板；
    电源：250W Flex ATX 80 Plus铜牌电源；
    数据线若干。


可见，要组成系统，至少还需要内存和硬盘。硬盘自不必说，手里还有几块6TB硬盘。

剩下的就是寻找32GB单条的DDR4 REC ECC内存了。

在Supermicro官网的X10SDV-TLN4F主板页面，有兼容内存列表，其中就有32GB单条容量的D288Pin DDR4 Registered DIMM内存，型号为M393A4K40BB0。
经过上述功课，下单了5028D-TN4T + 4x32GB套装。

**5028D-TN4T和MicroServer Gen8的简单对比：**

两者体积基本相当，分别为14L和13L。5028D-TN4T功耗略高。

理论性能分数：

    5028D-TN4T（D-1540）：11000
    Gen8 E3-1265L v2：8100
    Gen8 i3-3220T：3700

5028D-TN4T优于Gen8的地方：

    5028D-TN4T支持单条32GB的内存，且有4个内存槽，内存总容量可达128GB；
    5028D-TN4T是标准的ITX主板，可以更换其他主板；
    5028D-TN4T机箱标配4个热插拔3.5位置，和2个2.5位置；
    5028D-TN4T标配支持硬盘热插拔；
    5028D-TN4T主板有6个SATA3（6Gbps）接口；
    5028D-TN4T的BIOS允许设置从任意SATA接口启动；
    5028D-TN4T是标准的12cm 4针风扇，可以随便更换风扇；
    5028D-TN4T在SATA模式下，IPMI依然可以读硬盘温度，不会像Gen8那样SATA模式无法读取硬盘温度，从而出现风扇暴力问题；
    5028D-TN4T主板集成双万兆网卡，更加YY；


Gen8优于5028D-TN4T的地方：

    Gen8容易购买，价格便宜。
    Gen8的做工好于5028D-TN4T，尽管5028D-TN4T的做工也是相当不错。
    Gen8可以换CPU。


**为什么没有提到RAID？**

我都是SATA单盘直接用的，从没考虑过RAID。简而言之，四盘位家用，RAID还不如备份更管用；而且SATA单盘使用非常灵活。原因就这么简单。

**功耗实测：**

关机功耗8.5W左右，因为此时虽然主机关闭，但是IPMI依然是运行的。BIOS界面的功耗约30～40W。

从下单到收货不到两周，下面上开箱图：

美国西海岸发来的箱子
![package1](https://www.chiphell.com/data/attachment/forum/201508/27/165208wh4vuvkbxncumv4u.jpg)

标签上标明了型号、序列号等信息
![package2](https://www.chiphell.com/data/attachment/forum/201508/27/165210ieo89z7o7446o39o.jpg)

打开包装箱，浓浓的工业包装风格
![package3](https://www.chiphell.com/data/attachment/forum/201508/27/165211x5hhk46sc5y4y286.jpg)

主机外观
![package5](https://www.chiphell.com/data/attachment/forum/201508/27/165213yr18g1yz8wrp8h1z.jpg)

主机背面，一个标准的12cm风扇；挡板上共有5个网口：1个IPMI，2个千兆，另外2个万兆电口
![package6](https://www.chiphell.com/data/attachment/forum/201508/27/165214ycutzi7w11w5h3ic.jpg)

主板PCIE插槽，可以见SATA接口
![package4](https://www.chiphell.com/data/attachment/forum/201508/27/165231kzbe8v8ewlyw85iz.jpg)

4条内存插好了
![package7](https://www.chiphell.com/data/attachment/forum/201508/27/165233s0yp3ipiy2mh0g13.jpg)

开机了，自检需要1～2分钟
![package7](https://www.chiphell.com/data/attachment/forum/201508/27/165237zkylgm0f0ng8iik1.jpg)

BIOS显示CPU为Xeon D-1540
![package8](https://www.chiphell.com/data/attachment/forum/201508/27/165240xzkw1vkxs3kv4nw1.jpg)

顶视图-机箱顶部的2.5寸SSD位置
![package9](https://www.chiphell.com/data/attachment/forum/201508/27/165236aw9pdqxdpw6sxx4w.jpg)














