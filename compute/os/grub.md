GRUB

### grub rescue 终端模式修复方法



1.  先使用ls命令，找到Ubuntu的安装在哪个分区：
    grub rescue>ls
    会罗列所有的磁盘分区信息，比方说：
    (hd0),(hd0,msdos3),(hd0,msdos2),(hd0,msdos1)

2. 然后依次调用如下命令： msdosX表示各个分区，注意 msdos 与 数字 之间没有空格！
    grub rescue>ls (hd0,msdosX)/boot/grub
    如果都找不到的话，需要查一下是否因为Linux版本差异，造成grub的路径不对，
    例如直接ls(hd0,X)/grub等等。

3. 假设找到（hd0,msdos3）时，显示了文件夹中的文件，则表示 Linux 安装在这个分区。

4. 调用如下命令：
    grub rescue>set root=(hd0,msdos3)    
    grub rescue>set prefix=(hd0,msdos3)/boot/grub    
    grub rescue>insmod /boot/grub/normal.mod

5. 然后调用如下命令，就可以显示出丢失的grub菜单了。
    grub rescue>normal

6. 不过不要高兴，如果这时重启，问题依旧存在，我们需要进入Linux中，对grub进行修复。
    进入Linux之后，在命令行执行：
    sudo update-grub    sudo grub-install /dev/sda
    （sda是你的硬盘号码，千万不要指定分区号码，例如sda1，sda5等都不对）

7. 重启测试是否已经恢复了grub的启动菜单。
