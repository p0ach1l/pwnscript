"""
ELF和LIBC快速查找工具模块
提供便捷的函数偏移、字符串查找等功能
"""
from pwn import *
import os

# 全局ELF和LIBC对象
_current_elf = None
_current_libc = None
_elf_base = 0
_libc_base = 0

def set_binary(elf_obj=None, libc_obj=None, elf_base=0, libc_base=0):
    """
    统一设置ELF和LIBC对象
    ELF优先级高于LIBC，可以同时设置或单独设置
    
    Args:
        elf_obj: ELF对象或文件路径，优先级高
        libc_obj: LIBC对象或文件路径
        elf_base: ELF基址，默认为0
        libc_base: LIBC基址，默认为0
    """
    global _current_elf, _current_libc, _elf_base, _libc_base
    
    # 设置ELF（优先级高）
    if elf_obj is not None:
        if isinstance(elf_obj, str):
            _current_elf = ELF(elf_obj)
        else:
            _current_elf = elf_obj
        _elf_base = elf_base
    
    # 设置LIBC
    if libc_obj is not None:
        if isinstance(libc_obj, str):
            _current_libc = ELF(libc_obj)
        else:
            _current_libc = libc_obj
        _libc_base = libc_base

def set_elf(elf_obj, base=0):
    """
    设置当前ELF对象（保持向后兼容）
    
    Args:
        elf_obj: ELF对象或文件路径
        base: ELF基址，默认为0
    """
    set_binary(elf_obj=elf_obj, elf_base=base)

def set_libc(libc_obj, base=0):
    """
    设置当前LIBC对象（保持向后兼容）
    
    Args:
        libc_obj: ELF对象或文件路径
        base: LIBC基址，默认为0
    """
    set_binary(libc_obj=libc_obj, libc_base=base)

def set_elf_base(base):
    """设置ELF基址"""
    global _elf_base
    _elf_base = base

def set_libc_base(base):
    """设置LIBC基址"""
    global _libc_base
    _libc_base = base

def plt(func_name, elf_base=None):
    """
    获取PLT表中函数地址
    
    Args:
        func_name: 函数名
        elf_base: ELF基址，如果为None则使用全局设置
    
    Returns:
        int: PLT地址
    """
    if _current_elf is None:
        raise RuntimeError("No ELF set. Use set_elf() first.")
    
    base = elf_base if elf_base is not None else _elf_base
    plt_addr = _current_elf.plt.get(func_name)
    
    if plt_addr is None:
        raise ValueError(f"Function '{func_name}' not found in PLT")
    
    return plt_addr + base

def got(func_name, elf_base=None):
    """
    获取GOT表中函数地址
    
    Args:
        func_name: 函数名
        elf_base: ELF基址，如果为None则使用全局设置
    
    Returns:
        int: GOT地址
    """
    if _current_elf is None:
        raise RuntimeError("No ELF set. Use set_elf() first.")
    
    base = elf_base if elf_base is not None else _elf_base
    got_addr = _current_elf.got.get(func_name)
    
    if got_addr is None:
        raise ValueError(f"Function '{func_name}' not found in GOT")
    
    return got_addr + base

def elf_sym(symbol_name, elf_base=None):
    """
    获取符号地址
    
    Args:
        symbol_name: 符号名
        elf_base: ELF基址，如果为None则使用全局设置
    
    Returns:
        int: 符号地址
    """
    if _current_elf is None:
        raise RuntimeError("No ELF set. Use set_elf() first.")
    
    base = elf_base if elf_base is not None else _elf_base
    sym_addr = _current_elf.symbols.get(symbol_name)
    
    if sym_addr is None:
        raise ValueError(f"Symbol '{symbol_name}' not found")
    
    return sym_addr + base

def libc_sym(func_name, libc_base=None):
    """
    获取LIBC中函数地址
    
    Args:
        func_name: 函数名
        libc_base: LIBC基址，如果为None则使用全局设置
    
    Returns:
        int: 函数地址
    """
    if _current_libc is None:
        raise RuntimeError("No LIBC set. Use set_libc() first.")
    
    base = libc_base if libc_base is not None else _libc_base
    func_addr = _current_libc.symbols.get(func_name)
    
    if func_addr is None:
        raise ValueError(f"Function '{func_name}' not found in LIBC")
    
    return func_addr + base

def libc_str(string, libc_base=None):
    """
    查找LIBC中的字符串
    
    Args:
        string: 要查找的字符串
        libc_base: LIBC基址，如果为None则使用全局设置
    
    Returns:
        int: 字符串地址
    """
    if _current_libc is None:
        raise RuntimeError("No LIBC set. Use set_libc() first.")
    
    base = libc_base if libc_base is not None else _libc_base
    
    # 查找字符串
    str_addr = next(_current_libc.search(string.encode() if isinstance(string, str) else string), None)
    
    if str_addr is None:
        raise ValueError(f"String '{string}' not found in LIBC")
    
    return str_addr + base


def elf_str(string, elf_base=None):
    """
    查找ELF中的字符串
    
    Args:
        string: 要查找的字符串
        elf_base: ELF基址，如果为None则使用全局设置
    
    Returns:
        int: 字符串地址
    """
    if _current_elf is None:
        raise RuntimeError("No ELF set. Use set_elf() first.")
    
    base = elf_base if elf_base is not None else _elf_base
    
    # 查找字符串
    str_addr = next(_current_elf.search(string.encode() if isinstance(string, str) else string), None)
    
    if str_addr is None:
        raise ValueError(f"String '{string}' not found in ELF")
    
    return str_addr + base

# 便捷函数组合
def system(libc_base=None):
    """快速获取system函数地址"""
    return libc_sym("system", libc_base)

def binsh(libc_base=None):
    """快速获取/bin/sh字符串地址"""
    return libc_str("/bin/sh", libc_base)

def sh(libc_base=None):
    """快速获取sh字符串地址"""
    return libc_str("sh", libc_base)


def show_plt():
    """显示PLT表中的所有函数"""
    if _current_elf is None:
        raise RuntimeError("No ELF set. Use set_elf() first.")
    
    from .log_utils import ls
    ls("PLT functions:")
    for func_name, addr in _current_elf.plt.items():
        ls(f"  {func_name}: 0x{addr + _elf_base:x}")

def show_got():
    """显示GOT表中的所有函数"""
    if _current_elf is None:
        raise RuntimeError("No ELF set. Use set_elf() first.")
    
    from .log_utils import ls
    ls("GOT functions:")
    for func_name, addr in _current_elf.got.items():
        ls(f"  {func_name}: 0x{addr + _elf_base:x}")

def show_symbols():
    """显示符号表中的所有符号"""
    if _current_elf is None:
        raise RuntimeError("No ELF set. Use set_elf() first.")
    
    from .log_utils import ls
    ls("Symbols:")
    for sym_name, addr in _current_elf.symbols.items():
        ls(f"  {sym_name}: 0x{addr + _elf_base:x}")

