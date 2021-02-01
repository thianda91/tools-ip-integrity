## IP 备案防漏报核查工具

本工具用于 IP 地址备案完整性自查。

同时支持 IPv4，IPv6 地址。

## 使用方法

### 功能1

**根据预设的全量 IP 地址范围。与已有 IP 地址进行对比，找出遗漏的 IP 地址。**

直接运行小工具。

根据提示输入全量的 IP 地址所在 `txt` 文件。

  > 每行一个 IP（段）

根据提示输入已存在的 IP 地址所在 `txt` 文件。

  > 每行一个 IP（段）或者每行包含起始 IP + 终止 IP 

输出对比结果到文件。

### 功能2

**IP地址格式转换，在 ip/mask 与 ip_start - ip_end 之间转换。（自动识别）**

需要在命令行运行小工具：(假设小工具文件名为 `integriry.exe`)

> 首先要学会如何打开命令行(cmd)：
> 
> 方法1： 在小工具所在文件夹，按住 `shift` 键，在空白处点击右键。选择“在此处打开命令窗口”，如果是 `windows 10`，可能显示的是“在此处打开 Powershell 窗口”
> 
> 方法2： 在小工具所在文件夹的地址栏，直接输入：`cmd`，按回车打开。

命令格式：

```sh
integriry convert <ip>
integriry convert -f <文件名>
integriry cv <ip>
integriry cv -f <文件名>
```

下面的例子都是正确的：

```sh
integriry cv 10.0.1.0/23
integriry cv 192.168.0.128-192.168.2.3
integriry cv 2021:abcd::f00/120
integriry cv 2021:abcd::f00-2021:abcd::8888:abc
integriry cv -f input.txt
```

### 功能3

**输入若干ip地址段，输出IP地址段合并后的结果**

```sh
integriry merge <文件名>
integriry m <文件名>
```

例子：

```sh
integriry m input.txt
```