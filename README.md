## IP 备案防漏报核查工具

本工具用于 IP 地址备案完整性自查。

同时支持 IPv4，IPv6 地址。

### 功能汇总

1. 根据预设的全量 IP 地址范围。与已有 IP 地址进行对比，找出遗漏的 IP 地址。
2. IP 地址格式(批量)转换，在 ip / mask 与 ip_start - ip_end 之间转换（自动识别）。
3. 输入若干 IP 地址段，输出 IP 地址段合并后的结果。

## 使用方法

### 功能1

**根据预设的全量 IP 地址范围。与已有 IP 地址进行对比，找出遗漏的 IP 地址。**

方式1：在命令行运行小工具：(假设小工具文件名为 `integrity.exe`)

> 首先要学会如何打开命令行(cmd)：
>
> 方法1： 在小工具所在文件夹，按住 `shift` 键，在空白处点击右键。选择“在此处打开命令窗口”，如果是 `windows 10`，可能显示的是“在此处打开 Powershell 窗口”
>
> 方法2： 在小工具所在文件夹的地址栏，直接输入：`cmd`，按回车打开。

命令格式：

```sh
integrity compare <全量ip.txt> <已存在ip.txt>
integrity cp <全量ip.txt> <已存在ip.txt>
```

例子：

```sh
integrity cp all.txt input.txt
```

方式2：直接运行小工具。

根据提示输入全量的 IP 地址所在 `txt` 文件。

  > 每行一个 IP（段）

根据提示输入已存在的 IP 地址所在 `txt` 文件。

  > 每行一个 IP（段）或者每行包含起始 IP + 终止 IP 

输出对比结果到文件。

### 功能2

**IP 地址格式转换，在 ip / mask 与 ip_start - ip_end 之间转换。（自动识别）**

需要在命令行运行小工具：(假设小工具文件名为 `integrity.exe`)

命令格式：

```sh
integrity convert <ip>
integrity convert -f <文件名>
integrity cv <ip>
integrity cv -f <文件名>
```

例子：

```sh
integrity cv 10.0.1.0/23
integrity cv 192.168.0.128-192.168.2.3
integrity cv 2021:abcd::f00/120
integrity cv 2021:abcd::f00-2021:abcd::8888:abc
integrity cv -f input.txt
```

若想输出到文件，可在命令后面加`> result.txt`，即把结果输出到`result.txt`文件。

```sh
integrity cv 10.0.1.0/23 > result.txt
integrity cv 192.168.0.128-192.168.2.3 > result.txt
integrity cv 2021:abcd::f00/120 > result.txt
integrity cv 2021:abcd::f00-2021:abcd::8888:abc > result.txt
integrity cv -f input.txt > result.txt
```

### 功能3

**输入若干 IP 地址段，输出 IP 地址段合并后的结果**

需要在命令行运行小工具：(假设小工具文件名为 `integrity.exe`)

```sh
integrity merge <ip1> <ip2> <ip3> <...>
integrity merge -f <文件名>
integrity m <ip1> <ip2> <ip3> <...>
integrity m -f <文件名>
```

例子：

```sh
integrity m 192.168.0.0/25 192.168.0.128/25 192.168.1.0/24
integrity m 192.168.0.0-192.168.0.25 192.168.0.26-192.168.0.127 192.168.0.128-192.168.0.255
integrity m 2021:abcd::8888:a80/123 2021:abcd::8888:aa0/124 2021:abcd::8888:ab0/124
integrity m input.txt
```

若想输出到文件，可在命令后面加`> result.txt`，即把结果输出到`result.txt`文件。

```sh
integrity m 192.168.0.0/25 192.168.0.128/25 192.168.1.0/24 > result.txt
integrity m 192.168.0.0-192.168.0.25 192.168.0.26-192.168.0.127 192.168.0.128-192.168.0.255 > result.txt
integrity m 2021:abcd::8888:a80/123 2021:abcd::8888:aa0/124 2021:abcd::8888:ab0/124 > result.txt
integrity m input.txt > result.txt
```

### 输入文件格式说明

传入的 `input.txt` 内容为一行一个 IP (段)，起始和终止 IP 直接用`-`或`制表符`间隔开。（从 excel 表中复制出来的 2 列便是`制表符`）


```txt
192.168.0.0/25
192.168.0.0-192.168.0.127
192.168.0.0	192.168.0.127
2021:abcd:8888::/120
2021:abcd:8888::-2021:abcd:8888::ff
2021:abcd:8888::	2021:abcd:8888::ff
```

