"""
接收数据处理工具模块
提供常用的地址接收、canary接收等便捷函数
"""
# from asyncio.windows_events import NULL
from pwn import *
from .macro_utils import get_current_connection
def recv_libc_addr(p=None):
    """
    接收libc相关地址
    处理格式: u64(p.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00'))
    
    Args:
        p: 连接对象，如果为None则使用当前连接
    
    Returns:
        int: 泄露的libc地址
    """
    if p is None:
        p = get_current_connection()
        if p is None:
            raise RuntimeError("No active connection. Use pr() to establish connection first.")
    
    data = p.recvuntil(b'\x7f')
    addr = u64(data[-6:].ljust(8, b'\x00'))
    return addr

def recv_str_addr(p=None, hex_len = 0):
    """
    接收十六进制地址
    处理格式: p.recvuntil(b'0x') + int(p.recv(hex_len), 16)
    
    Args:
        p: 连接对象，如果为None则使用当前连接
    
    Returns:
        int: 解析的地址
    """
    if p is None:
        p = get_current_connection()
        if p is None:
            raise RuntimeError("No active connection. Use pr() to establish connection first.")
    
    p.recvuntil(b'0x')
    hex_data = p.recv(hex_len)
    addr = int(hex_data, 16)
    return addr



def recv_addr_32(p=None):
    """
    接收32位地址
    
    Args:
        p: 连接对象，如果为None则使用当前连接
    
    Returns:
        int: 32位地址
    """
    if p is None:
        p = get_current_connection()
        if p is None:
            raise RuntimeError("No active connection. Use pr() to establish connection first.")
    data = p.recv(4)
    addr = u32(data)
    return addr

def recv_addr_64(p=None):
    """
    接收64位地址
    
    Args:
        p: 连接对象，如果为None则使用当前连接
    
    Returns:
        int: 64位地址
    """
    if p is None:
        p = get_current_connection()
        if p is None:
            raise RuntimeError("No active connection. Use pr() to establish connection first.")
    data = p.recv(6)
    addr = u64(data)
    return addr

# 便捷的别名函数
def leak_libc(p=None):
    """recv_libc_addr的别名"""
    return recv_libc_addr(p)


def leak_hex( p=None):
    """
    根据框架泄露地址

    Args:
        p: 连接对象
    
    Returns:
        int: 泄露的地址
    """
    arch = context.arch
    if arch == 'amd64':
        return recv_addr_64(p)
    elif arch == 'i386':
        return recv_addr_32(p)
        

def leak_str(p=None):
    arch = context.arch
    """recv_str_addr的别名"""
    if arch == 'amd64':
        hex_len = 12
        return recv_str_addr(p , hex_len)
    elif arch == 'i386':
        hex_len = 8
        return recv_str_addr(p , hex_len)

def leak_canary(p=None):
    arch = context.arch
    """recv_str_addr的别名"""
    if arch == 'amd64':
        hex_len = 16
        return recv_str_addr(p , hex_len)
    elif arch == 'i386':
        hex_len = 8
        print("32位系统")
        return recv_str_addr(p , hex_len)

# 高级功能函数
def leak_base(known_func_offset = 0, p=None):
    """
    泄露libc基址
    
    Args:
        known_func_offset: 已知函数在libc中的偏移
        p: 连接对象
    
    Returns:
        int: libc基址
    """
    arch = context.arch
    if arch == 'amd64':
        leaked_addr = recv_libc_addr(p)
        libc_base = leaked_addr - known_func_offset
        return libc_base
    elif arch == 'i386':
        leaked_addr = recv_addr_32(p)
        libc_base = leaked_addr - known_func_offset
        return libc_base

   