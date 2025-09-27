"""
Macro definitions for common pwntools functions
提供常用pwntools函数的快捷宏定义
"""

# 全局连接对象
_current_connection = None

def set_current_connection(conn):
    """设置当前连接对象"""
    global _current_connection
    _current_connection = conn

def get_current_connection():
    """获取当前连接对象"""
    return _current_connection

# 发送数据宏
def s(data):
    """p.send()的宏定义"""
    if _current_connection:
        return _current_connection.send(data)
    else:
        raise RuntimeError("No active connection. Use pr() to establish connection first.")

def sl(data):
    """p.sendline()的宏定义"""
    if _current_connection:
        return _current_connection.sendline(data)
    else:
        raise RuntimeError("No active connection. Use pr() to establish connection first.")

def sa(delim, data):
    """p.sendafter()的宏定义"""
    if _current_connection:
        return _current_connection.sendafter(delim, data)
    else:
        raise RuntimeError("No active connection. Use pr() to establish connection first.")

def sla(delim, data):
    """p.sendlineafter()的宏定义"""
    if _current_connection:
        return _current_connection.sendlineafter(delim, data)
    else:
        raise RuntimeError("No active connection. Use pr() to establish connection first.")

# 接收数据宏
def r(numb=4096):
    """p.recv()的宏定义"""
    if _current_connection:
        return _current_connection.recv(numb)
    else:
        raise RuntimeError("No active connection. Use pr() to establish connection first.")

def rl():
    """p.recvline()的宏定义"""
    if _current_connection:
        return _current_connection.recvline()
    else:
        raise RuntimeError("No active connection. Use pr() to establish connection first.")

def ra(delim):
    """p.recvafter()的宏定义"""
    if _current_connection:
        return _current_connection.recvafter(delim)
    else:
        raise RuntimeError("No active connection. Use pr() to establish connection first.")

def ru(delim):
    """p.recvuntil()的宏定义"""
    if _current_connection:
        return _current_connection.recvuntil(delim)
    else:
        raise RuntimeError("No active connection. Use pr() to establish connection first.")

def rla():
    """p.recvlineafter()的宏定义"""
    if _current_connection:
        return _current_connection.recvlineafter()
    else:
        raise RuntimeError("No active connection. Use pr() to establish connection first.")

def rt(timeout=1):
    """p.recvtimeout()的宏定义"""
    if _current_connection:
        return _current_connection.recvtimeout(timeout)
    else:
        raise RuntimeError("No active connection. Use pr() to establish connection first.")

# 交互宏
def ia():
    """p.interactive()的宏定义"""
    if _current_connection:
        return _current_connection.interactive()
    else:
        raise RuntimeError("No active connection. Use pr() to establish connection first.")

def cl():
    """p.close()的宏定义"""
    if _current_connection:
        result = _current_connection.close()
        set_current_connection(None)
        return result
    else:
        raise RuntimeError("No active connection. Use pr() to establish connection first.")



# 创建连接包装器类
class ConnectionWrapper:
    """连接包装器，自动设置为当前连接"""
    
    def __init__(self, connection):
        self._conn = connection
        set_current_connection(connection)
    
    def __getattr__(self, name):
        return getattr(self._conn, name)
    
    def __enter__(self):
        set_current_connection(self._conn)
        return self._conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        set_current_connection(None)