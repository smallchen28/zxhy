# rpm和rpmbuild

## rpm

### 简介

RPM是RPM Package Manager（RPM软件包管理器）的缩写，是redhat发行的linux版本及centos/suse/turbolinux等版本的软件包管理工具。

RPM包命名方式：name-version-release.architecture.rpm

### 命令帮助

```
[root@zxdb97 ~]# rpm --help
Usage: rpm [OPTION...]

Query/Verify package selection options:
  -a, --all                        query/verify all packages
  -f, --file                       query/verify package(s) owning file
  -g, --group                      query/verify package(s) in group
  -p, --package                    query/verify a package file
  --pkgid                          query/verify package(s) with package identifier
  --hdrid                          query/verify package(s) with header identifier
  --triggeredby                    query the package(s) triggered by the package
  --whatrequires                   query/verify the package(s) which require a dependency
  --whatprovides                   query/verify the package(s) which provide a dependency
  --nomanifest                     do not process non-package files as manifests

Query options (with -q or --query):
  -c, --configfiles                list all configuration files
  -d, --docfiles                   list all documentation files
  -L, --licensefiles               list all license files
  --dump                           dump basic file information
  -l, --list                       list files in package
  --queryformat=QUERYFORMAT        use the following query format
  -s, --state                      display the states of the listed files

Verify options (with -V or --verify):
  --nofiledigest                   don't verify digest of files
  --nofiles                        don't verify files in package
  --nodeps                         don't verify package dependencies
  --noscript                       don't execute verify script(s)

Install/Upgrade/Erase options:
  --allfiles                       install all files, even configurations which might otherwise be skipped
  --allmatches                     remove all packages which match <package> (normally an error is generated if <package> specified multiple packages)
  --badreloc                       relocate files in non-relocatable package
  -e, --erase=<package>+           erase (uninstall) package
  --excludedocs                    do not install documentation
  --excludepath=<path>             skip files with leading component <path> 
  --force                          short hand for --replacepkgs --replacefiles
  -F, --freshen=<packagefile>+     upgrade package(s) if already installed
  -h, --hash                       print hash marks as package installs (good with -v)
  --ignorearch                     don't verify package architecture
  --ignoreos                       don't verify package operating system
  --ignoresize                     don't check disk space before installing
  -i, --install                    install package(s)
  --justdb                         update the database, but do not modify the filesystem
  --nodeps                         do not verify package dependencies
  --nofiledigest                   don't verify digest of files
  --nocontexts                     don't install file security contexts
  --noorder                        do not reorder package installation to satisfy dependencies
  --noscripts                      do not execute package scriptlet(s)
  --notriggers                     do not execute any scriptlet(s) triggered by this package
  --nocollections                  do not perform any collection actions
  --oldpackage                     upgrade to an old version of the package (--force on upgrades does this automatically)
  --percent                        print percentages as package installs
  --prefix=<dir>                   relocate the package to <dir>, if relocatable
  --relocate=<old>=<new>           relocate files from path <old> to <new>
  --replacefiles                   ignore file conflicts between packages
  --replacepkgs                    reinstall if the package is already present
  --test                           don't install, but tell if it would work or not
  -U, --upgrade=<packagefile>+     upgrade package(s)

Common options for all rpm modes and executables:
  -D, --define='MACRO EXPR'        define MACRO with value EXPR
  --undefine=MACRO                 undefine MACRO
  -E, --eval='EXPR'                print macro expansion of EXPR
  --macros=<FILE:...>              read <FILE:...> instead of default file(s)
  --noplugins                      don't enable any plugins
  --nodigest                       don't verify package digest(s)
  --nosignature                    don't verify package signature(s)
  --rcfile=<FILE:...>              read <FILE:...> instead of default file(s)
  -r, --root=ROOT                  use ROOT as top level directory (default: "/")
  --dbpath=DIRECTORY               use database in DIRECTORY
  --querytags                      display known query tags
  --showrc                         display final rpmrc and macro configuration
  --quiet                          provide less detailed output
  -v, --verbose                    provide more detailed output
  --version                        print the version of rpm being used

Options implemented via popt alias/exec:
  --scripts                        list install/erase scriptlets from package(s)
  --setperms                       set permissions of files in a package
  --setugids                       set user/group ownership of files in a package
  --conflicts                      list capabilities this package conflicts with
  --obsoletes                      list other packages removed by installing this package
  --provides                       list capabilities that this package provides
  --requires                       list capabilities required by package(s)
  --info                           list descriptive information from package(s)
  --changelog                      list change logs for this package
  --xml                            list metadata in xml
  --triggers                       list trigger scriptlets from package(s)
  --last                           list package(s) by install time, most recent first
  --dupes                          list duplicated packages
  --filesbypkg                     list all files from each package
  --fileclass                      list file names with classes
  --filecolor                      list file names with colors
  --fscontext                      list file names with security context from file system
  --fileprovide                    list file names with provides
  --filerequire                    list file names with requires
  --filecaps                       list file names with POSIX1.e capabilities

Help options:
  -?, --help                       Show this help message
  --usage                          Display brief usage message
```

### 使用说明

#### 安装，升级，删除

rpm -ivh proxysql-1.3.7-1.1.el7.x86_64.rpm 

rpm -Uvh proxysql-1.3.7-1.1.el7.x86_64.rpm 

rpm -e proxysql-1.3.7-1.1

#### 查询

- 对已安装包的操作

rpm -qa|grep proxysql    查询已安装包

rpm -ql proxysql         查询安装包对应文件

rpm -qi proxysql         查询安装包对应信息

rpm -qf /usr/bin/proxysql-admin  查询文件对应安装包

- 对未安装包的操作

rpm -qpl proxysql-1.3.7-1.1.el7.x86_64.rpm 显示安装包内文件

rpm -qpi proxysql-1.3.7-1.1.el7.x86_64.rpm 显示安装包信息

rpm -qpR proxysql-1.3.7-1.1.el7.x86_64.rpm 显示安装包依赖

#### 验证

rpm -V proxysql-1.3.7-1.1.el7.x86_64.rpm 


## rpmbuild

### 简介

rpmbuild 用于创建软件的二进制包和源代码包。一个"包"包括文件的归档以及用来安装和卸载归档中文件的元数据。元数据包括辅助脚本、文件属性、以及相关的描述性信息。

软件包有两种：

- 二进制包，用来封装已经编译好的二进制文件；

- 源代码包，用来封装源代码和要构建二进制包需要的信息。

### 使用说明

```
[root@zxdb97 ~]# rpmbuild --help
Usage: rpmbuild [OPTION...]

Build options with [ <specfile> | <tarball> | <source package> ]:
  -bp                           build through %prep (unpack sources and apply patches) from <specfile>
  -bc                           build through %build (%prep, then compile) from <specfile>
  -bi                           build through %install (%prep, %build, then install) from <specfile>
  -bl                           verify %files section from <specfile>
  -ba                           build source and binary packages from <specfile>
  -bb                           build binary package only from <specfile>
  -bs                           build source package only from <specfile>
  -tp                           build through %prep (unpack sources and apply patches) from <tarball>
  -tc                           build through %build (%prep, then compile) from <tarball>
  -ti                           build through %install (%prep, %build, then install) from <tarball>
  -ta                           build source and binary packages from <tarball>
  -tb                           build binary package only from <tarball>
  -ts                           build source package only from <tarball>
  --rebuild                     build binary package from <source package>
  --recompile                   build through %install (%prep, %build, then install) from <source package>
  --buildroot=DIRECTORY         override build root
  --clean                       remove build tree when done
  --nobuild                     do not execute any stages of the build
  --nodeps                      do not verify build dependencies
  --nodirtokens                 generate package header(s) compatible with (legacy) rpm v3 packaging
  --noclean                     do not execute %clean stage of the build
  --nocheck                     do not execute %check stage of the build
  --rmsource                    remove sources when done
  --rmspec                      remove specfile when done
  --short-circuit               skip straight to specified stage (only for c,i)
  --target=CPU-VENDOR-OS        override target platform

Common options for all rpm modes and executables:
  -D, --define='MACRO EXPR'     define MACRO with value EXPR
  --undefine=MACRO              undefine MACRO
  -E, --eval='EXPR'             print macro expansion of EXPR
  --macros=<FILE:...>           read <FILE:...> instead of default file(s)
  --noplugins                   don't enable any plugins
  --nodigest                    don't verify package digest(s)
  --nosignature                 don't verify package signature(s)
  --rcfile=<FILE:...>           read <FILE:...> instead of default file(s)
  -r, --root=ROOT               use ROOT as top level directory (default: "/")
  --dbpath=DIRECTORY            use database in DIRECTORY
  --querytags                   display known query tags
  --showrc                      display final rpmrc and macro configuration
  --quiet                       provide less detailed output
  -v, --verbose                 provide more detailed output
  --version                     print the version of rpm being used

Options implemented via popt alias/exec:
  --with=<option>               enable configure <option> for build
  --without=<option>            disable configure <option> for build
  --buildpolicy=<policy>        set buildroot <policy> (e.g. compress man pages)
  --sign                        generate GPG signature (deprecated, use command rpmsign instead)

Help options:
  -?, --help                    Show this help message
  --usage                       Display brief usage message
```

#### 目录规范

在构建软件包之前先构建目录树

```
[root@zxdb97 ~]# mkdir -pv ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
mkdir: created directory ‘/root/rpmbuild’
mkdir: created directory ‘/root/rpmbuild/BUILD’
mkdir: created directory ‘/root/rpmbuild/BUILDROOT’
mkdir: created directory ‘/root/rpmbuild/RPMS’
mkdir: created directory ‘/root/rpmbuild/SOURCES’
mkdir: created directory ‘/root/rpmbuild/SPECS’
mkdir: created directory ‘/root/rpmbuild/SRPMS’
[root@zxdb97 ~]# ll /root/rpmbuild/
total 24
drwxr-xr-x. 2 root root 4096 Sep  7 11:04 BUILD     #编译之前，如解压包后存放的路径
drwxr-xr-x. 2 root root 4096 Sep  7 11:04 BUILDROOT #编译后存放的路径
drwxr-xr-x. 2 root root 4096 Sep  7 11:04 RPMS      #打包完成后rpm包存放的路径
drwxr-xr-x. 2 root root 4096 Sep  7 11:04 SOURCES   #源包所放置的路径
drwxr-xr-x. 2 root root 4096 Sep  7 11:04 SPECS     #spec文档放置的路径
drwxr-xr-x. 2 root root 4096 Sep  7 11:04 SRPMS     #源码rpm包放置的路径
```   

#### 命令说明

rpmbuild命令支持以下几种生成模式

- 从 spec 构建

```
rpmbuild -bp aaaa.spec #只执行spec的%pre 段(解开源码包并打补丁，即只做准备)
rpmbuild -bc  #执行spec的%pre和%build 段(准备并编译make)
rpmbuild -bi  #执行spec中%pre，%build与%install(准备，编译并安装makeinstall)
rpmbuild -bl  #检查spec中的%file段(查看文件是否齐全)
rpmbuild -ba  #建立源码与二进制包(常用)
rpmbuild -bb  #只建立二进制包(常用)
rpmbuild -bs  #只建立源码包
```

- 从 Tar 构建

```
rpbuild -tp aaa.tar.gz #对应-bp
rpbuild -tc #对应-bc
rpbuild -ti #对应-bi
rpbuild -ta #对应-ba
rpbuild -tb #对应-bb
rpbuild -ts #对应-bs
```

- 从Src 构建

```
--rebuild    #建立二进制包，通-bb
--recompile  #同-bi
```

- 其他选项

```
--buildroot DIRECTORY  在构建时，使用 DIRECTORY 目录覆盖默认的 BuildRoot 值
--clean                在打包完成之后删除构建树
--nobuild              不执行任何实际的构建步骤。可用于测试 spec 文件。
--noclean              不执行 spec 文件的"%clean"阶段(即使它确实存在)。
--nocheck              不执行 spec 文件的"%check"阶段(即使它确实存在)。
--nodeps               不检查编译依赖条件是否满足
--rmsource             在构建后删除源代码(也可以单独使用，例如"rpmbuild --rmsource foo.spec")
--rmspec               在构建之后删除 spec 文件(也可以单独使用，例如"rpmbuild --rmspec foo.spec")
--short-circuit        直接跳到指定阶段(也就是跳过指定阶段前面的所有步骤)，只有与 c 或 i 或 b 连用才有意义。
--target PLATFORM      在构建时，将 PLATFORM 解析为 arch-vendor-os ，并以此设置宏 %_target, %_target_cpu, %_target_os 的值。
```

### spec编写

Spec文件分成文件头部和文件本体。头部用来定义基本信息，本地定义了执行动作。

#### 头部关键字信息

| 关键字 | 说明 |
|--------|--------|
|Name| 软件包的名称，后面可使用%{name}引用|
|Summary| 软件包的内容概要|
|Version| 软件包的版本号，后面可使用%{version}引用|
|Release| 发布序列号标明第几次打包，后面可使用%{release}引用|
|Group  | 软件分组，建议使用标准分组|
|License| 软件授权方式，例如GPL|
|Source | 源代码包，可以带多个用Source1、Source2等源，后面也可以用%{source1}、%{source2}引用|
|BuildRoot| 这个是安装或编译时使用的“虚拟目录”，后面可使用$(RPM_BUILD_ROOT}方式引用|
|URL    | 软件的主页|
|Vendor | 发行商或打包组织的信息，例如RedFlag Co,Ltd|
|Disstribution| 发行版标识|
|Patch| 补丁源码，可使用Patch1、Patch2等标识多个补丁，使用%patch0或%{patch0}引用|
|Build Arch| 指编译的目标处理器架构，noarch标识不指定|
|Requires| 该rpm包所依赖的软件包名称，可以用>=或<=表示大于或小于某一特定版本|
|Prefix:%{_prefix}| 安装程序指定路径|
|Prefix:%{_sysconfdir}| 安装配置文件指定路径|
|Provides| 指明本软件一些特定的功能，以便其他rpm识别|
|Packager|  打包者的信息|
|%description| 软件的详细说明|

#### spec主体部分

- %prep 预处理脚本

- %setup 把源码包解压并放好-n %{name}-%{version}，将源码包解压到这个路径。 

- %patch 打补丁

- %configure 这个不是关键字，而是rpm定义的标准宏命令。意思是执行源代码的configure配置

- %build 开始构建包，在BUILD/%{name}-%{version}目录中进行make的工作 

- %install 开始把软件安装到虚拟的根目录中，在BUILD/%{name}-%{version}目录中进行makeinstall的工作 

- %clean 清理临时文件

- %pre rpm安装前执行的脚本

- %post rpm安装后执行的脚本

- %preun rpm卸载前执行的脚本

- %postun rpm卸载后执行的脚本

- %files 定义那些文件或目录会放入rpm中。这里会在虚拟根目录下进行，千万不要写绝对路径，而应用宏或变量表示相对路径。

- %config 表示以配置文件的形式，从虚拟根目录下面打包到RPM里面去。当升级/卸载时，配置文件处理方式和程序文件不一样。

- %defattr (-,root,root) 指定包装文件的属性，分别是(mode,owner,group)，-表示默认值，对文本文件是0644，可执行文件是0755

- %exclude 列出不想打包到rpm中的文件

- %changelog 变更日志

#### 其他

rpm软件包系统的标准分组：/usr/share/doc/rpm-4.x.x/GROUPS

各种宏定义： /usr/lib/rpm/macros

已经安装的rpm包数据库： /var/lib/rpm

如果要避免生成debuginfo包：这个是默认会生成的rpm包。则可以使用下面的命令：

echo '%debug_package %{nil}' >> ~/.rpmmacros 