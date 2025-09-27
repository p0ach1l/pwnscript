# pwnscript - CTF PWN 工具包
# 为CTF PWN题目提供便捷的工具函数和宏定义

# 基础工具
from .context_utils import set_context
from .connection_utils import pr
from .log_utils import ls, lss, lsl

# 宏定义 - 常用pwntools函数的快捷方式
from .macro_utils import (
    # 发送数据宏
    s, sl, sa, sla,
    # 接收数据宏  
    r, rl, ra, ru, rla, rt,
    # 交互宏
    ia, cl,
    # 连接管理
    set_current_connection, get_current_connection,
    ConnectionWrapper
)

# 接收数据处理工具
from .recv_utils import (
    # 基础接收函数
    recv_libc_addr, recv_str_addr, 
    recv_addr_32, recv_addr_64,
    
    # 便捷别名
    leak_libc, leak_str, leak_hex, leak_canary,
    
    # 高级功能
    leak_base,
)

# ELF和LIBC快速查找工具
from .elf_utils import (
    # 设置函数
    set_binary, set_elf, set_libc, set_elf_base, set_libc_base,
    
    # ELF查找函数
    plt, got, elf_sym, elf_str,
    
    # LIBC查找函数
    libc_sym, libc_str, 
    
    # 常用函数快捷方式
    system, binsh, sh,
    
    # 显示和批量操作
    show_plt, show_got, show_symbols,
    
)

# 版本信息
__version__ = "2.1.0"
__author__ = "p0ach1l"
__description__ = "A powerful CTF PWN utility toolkit with macro support"

def version():
    """显示版本信息"""
    print(f"pwnscript v{__version__} by {__author__}")
    print(__description__)

def help_usage():
    """显示使用帮助"""
    print("""
=== pwnscript 使用指南 ===

基础功能:
  set_context()     - 设置pwntools环境
  pr()             - 连接进程/远程服务
  ls(), lss(), lsl()      - 高亮日志输出

宏定义 (需要先使用pr()建立连接):
  s(data)          - p.send(data)
  sl(data)         - p.sendline(data)
  sa(delim, data)  - p.sendafter(delim, data)
  sla(delim, data) - p.sendlineafter(delim, data)
  
  r(numb)          - p.recv(numb)
  rl()             - p.recvline()
  ra(delim)        - p.recvafter(delim)
  ru(delim)        - p.recvuntil(delim)
  rt(timeout)      - p.recvtimeout(timeout)
  
  ia()             - p.interactive()
  cl()             - p.close()
  

ELF和LIBC工具:
  set_elf(elf)     - 设置ELF对象
  set_libc(libc)   - 设置LIBC对象
  plt(func)        - 获取PLT地址
  got(func)        - 获取GOT地址
  sym(symbol)      - 获取符号地址
  
  libc_func(func)  - 获取LIBC函数地址
  binsh()          - 获取/bin/sh地址
  system()         - 获取system函数地址
  
  pop_rdi()        - 查找pop rdi gadget
  find_gadgets(pattern) - 查承ROP gadgets

接收数据工具:
  leak_libc()      - 接收libc地址 (自动处理\x7f结尾)
  leak_hex()       - 接收十六进制地址 (0x开头)
  leak_addr(size)  - 接收指定大小的地址
  
  recv_addr_32()   - 接收32位地址
  recv_addr_64()   - 接收64位地址
  leak_base(offset) - 智能计算libc基址

运行模式:
  python exp.py    - 本地模式
  python exp.py de - 调试模式
  python exp.py re - 远程模式
  python exp.py ssl- SSL远程模式

示例:
  from pwnscript import *
  
  set_context()
  p = pr(filename='./binary')  # 自动设置为当前连接
  
  sl(b'Hello')      # 等同于 p.sendline(b'Hello')
  data = rl()       # 等同于 data = p.recvline()
  
  payload = flat(b'A'*64, p64(0x400123))
  sl(payload)
  
  ia()              # 等同于 p.interactive()
""")

# 导出所有公共接口
__all__ = [
    # 基础工具
    'set_context', 'pr', 'ls', 'lss', 'lsl',
    
    # 发送数据宏
    's', 'sl', 'sa', 'sla',
    
    # 接收数据宏
    'r', 'rl', 'ra', 'ru', 'rla', 'rt',
    
    # 交互宏
    'ia', 'cl',
    
    # 连接管理
    'set_current_connection', 'get_current_connection', 'ConnectionWrapper',
    
    # 接收数据工具
    'recv_libc_addr', 'recv_str_addr',
    'recv_addr_32', 'recv_addr_64', 
    
    # 便捷别名
    'leak_libc', 'leak_str', 'leak_hex', 'leak_canary',
    
    # 高级功能
    'leak_base', 
    
    # ELF和LIBC工具
    'set_binary', 'set_elf', 'set_libc', 'set_elf_base', 'set_libc_base',
    'plt', 'got', 'elf_sym', 'elf_str',
    'libc_sym', 'libc_str', 
    'system', 'binsh', 'sh',
    'show_plt', 'show_got', 'show_symbols',
    
    # 辅助函数
    'version', 'help_usage'
]
