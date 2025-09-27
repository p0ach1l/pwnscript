# pwnscript - CTF PWN 工具包

一个精简而强大的CTF PWN题目辅助工具包，为CTF选手提供便捷的宏定义和连接管理功能。

## 🚀 新版本特性

### v2.1.0 新增功能
- **宏定义支持**: 常用pwntools函数的快捷方式
- **SSL连接支持**: 支持加密的远程连接
- **精简架构**: 移除异架构支持，专注本地架构
- **智能连接管理**: 自动设置当前连接

## 📦 安装

```bash
git clone https://github.com/p0ach1l/pwnscript.git
cd pwnscript
pip install -e .
```

### 依赖要求
- Python 3.6+
- pwntools >= 4.8.0

## 🎯 快速开始

### 基础使用示例

```python
from pwn import *
from pwnscript import *

# 题目信息
filename = "./binary"
url = "pwn.example.com:1337"

# GDB调试脚本
gdbscript = '''
b main
b *main+100
c
'''

# 设置环境
set_context(log_level='debug', arch='amd64', os='linux', endian='little', timeout=5)

# 连接目标（自动设置为当前连接）
p = pr(url=url, filename=filename, gdbscript=gdbscript)
elf = ELF(filename)

# 使用宏定义进行交互
sl(b"Hello World")      # 等同于 p.sendline(b"Hello World")
data = rl()             # 等同于 data = p.recvline()
lss(data)             # 高亮显示变量

# 构造payload
payload = flat(b'A'*64, p64(0x400123))
sl(payload)

# 进入交互模式
ia()                    # 等同于 p.interactive()
```

## 🛠 核心功能

### 1. 连接管理

```python
# 本地连接
p = pr(filename='./binary')

# 远程连接
p = pr(url='host:port')

# SSL远程连接
p = pr(url='host:port', ssl_mode=True)

# 调试模式
p = pr(filename='./binary', gdbscript='b main')
```

### 2. 运行模式

```bash
# 本地运行
python pwn_exp.py

# 调试模式 (需要tmux)
python pwn_exp.py de

# 远程模式
python pwn_exp.py re

# SSL远程模式
python pwn_exp.py ssl
```

### 3. 宏定义参考

#### 发送数据宏

| 宏定义 | 原函数 | 描述 |
|---------|----------|---------|
| `s(data)` | `p.send(data)` | 发送数据 |
| `sl(data)` | `p.sendline(data)` | 发送数据并换行 |
| `sa(delim, data)` | `p.sendafter(delim, data)` | 等待分隔符后发送 |
| `sla(delim, data)` | `p.sendlineafter(delim, data)` | 等待分隔符后发送并换行 |

#### 接收数据宏

| 宏定义 | 原函数 | 描述 |
|---------|----------|---------|
| `r(numb)` | `p.recv(numb)` | 接收指定字节 |
| `rl()` | `p.recvline()` | 接收一行 |
| `ra(delim)` | `p.recvafter(delim)` | 接收到分隔符 |
| `ru(delim)` | `p.recvuntil(delim)` | 接收直到分隔符 |
| `rt(timeout)` | `p.recvtimeout(timeout)` | 超时接收 |

#### 交互宏

| 宏定义 | 原函数 | 描述 |
|---------|----------|---------|
| `ia()` | `p.interactive()` | 进入交互模式 |
| `cl()` | `p.close()` | 关闭连接 |


### 4. 接收数据工具

```python
# 自动处理libc地址泄露
libc_addr = leak_libc()  # 自动处理 u64(p.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00'))
lss(libc_addr)  # 可以直接传入值也可以传入变量名

# 接收字符串地址
str_addr = leak_str()  # 自动处理 p.recvuntil(b'0x') + int(p.recv(12), 16)

# 接收字节地址
addr = leak_hex()

# 接受字符串canary
canary = leak_canary()

# 智能计算libc基址
libc_base = leak_base(0x80aa0)  # 传入已知函数偏移
```

### 5. 增强日志功能

```python
# 高亮显示变量 - 支持两种用法
addr = 0x400123
lss("addr")  # 传入变量名字符串
lss(addr)    # 直接传入变量值

# 高亮显示变量
addr = 0x400123
lss("addr")  # 显示: addr ---> 0x400123
# 高亮显示字节数
payload = b'a'*64
lsl(payload) # 显示: payload ---> 64 (0x40)
# 成功日志
ls("成功信息")
```

### 6. 初始化加载环境

```python
# 加载elf文件、libc文件
set_binary(elf,libc)
# 加载elf文件
set_elf(elf)
# 加载libc文件
set_libc(libc)
# 设置elf文件基地址
set_elf_base(elf_base)
# 设置libc文件基地址
set_libc_base(libc_base)

```

### 7. 获取函数或字符串偏移

```python
# 初始化加载环境后
# 获取plt、got表
puts_plt/got = plt\got("puts")

# 获取elf文件函数偏移
puts_addr = elf_sym("puts")

# 获取elf文件字符串偏移
string = elf_str("string")

# 获取libc文件函数偏移
puts_addr = libc_sym("puts")

# 获取libc文件字符串偏移
string = libc_str("string")

# 获取libc文件system函数偏移
system_addr = system()

# 获取libc文件/bin/sh字符串偏移
binsh_addr = binsh()

```



## 🎨 完整示例

### 基础栈溢出示例

```python
#!/usr/bin/env python3
from pwn import *
from pwnscript import *

# 题目信息
filename = "./vuln"
url = "pwn.example.com:1337"

gdbscript = '''
b main
b *vuln+50
c
'''

# 设置环境
set_context(log_level='debug', arch='amd64', os='linux')

def exploit():
    # 连接目标
    p = pr(url=url, filename=filename, gdbscript=gdbscript)
    elf = ELF(filename)
    
    # 构造payload
    offset = 72
    system_addr = 0x7ffff7a52390
    binsh_addr = 0x7ffff7b97e9a
    pop_rdi = 0x400743
    
    payload = flat(
        b'A' * offset,
        p64(pop_rdi),
        p64(binsh_addr),
        p64(system_addr)
    )
    
    # 使用宏定义发送
    sl(payload)
    
    # 高亮显示payload长度
    lss("payload")
    
    # 进入交互
    ia()

if __name__ == "__main__":
    exploit()
```

---

作为一个终极懒人，平常刷pwn题的各种模式切换显示十分繁琐，于是就诞生了这个小小的python库。现在增加了宏定义支持，让写PWN脚本更加高效！
