import sys
import re
from pwn import *
from .macro_utils import ConnectionWrapper, set_current_connection

def pr(url=None, filename=None, gdbscript=None, ssl_mode=False, **kwargs):
    """
    增强的进程/远程连接函数 
    
    Args:
        url: 远程连接地址 (format: host:port)
        filename: 本地二进制文件路径
        gdbscript: GDB调试脚本
        ssl_mode: 是否使用SSL连接
        **kwargs: 其他参数
    
    Returns:
        ConnectionWrapper: 包装后的连接对象
    """
    p = None

    remote_mode = len(sys.argv) > 1 and sys.argv[1] == 're'
    debug_mode = len(sys.argv) > 1 and sys.argv[1] == 'de'
    ssl_remote_mode = len(sys.argv) > 1 and sys.argv[1] == 'ssl'

    if remote_mode or ssl_remote_mode:
        if not url:
            log.error("Remote mode requires a URL (format: host:port)")
            return None
        
        # 解析URL
        match = re.match(r'([^:\s]+)(?::(\d+)|\s+(\d+))?', url)
        if not match:
            log.error(f"Invalid URL format: {url}")
            return None
        
        host = match.group(1)
        port = int(match.group(2) or match.group(3) or 9999)
        
        try:
            if ssl_remote_mode or ssl_mode:
                # SSL连接模式
                log.info(f"Connecting to {host}:{port} with SSL")
                timeout = kwargs.get('timeout', 10)
                p = remote(host, port, ssl=True, timeout=timeout)
                log.success(f"SSL connection established to {host}:{port}")
            else:
                # 普通TCP连接
                log.info(f"Connecting to {host}:{port}")
                timeout = kwargs.get('timeout', 10)
                p = remote(host, port, timeout=timeout)
                log.success(f"Connection established to {host}:{port}")
        except Exception as e:
            log.error(f"Connection failed: {e}")
            return None
    else:
        # 本地模式
        if not filename:
            log.error("Local mode requires a filename")
            return None
        
        try:
            log.info(f"Starting local process: {filename}")
            env = kwargs.get('env', {})
            p = process(filename, env=env)
            
            if debug_mode and gdbscript:
                log.info("Attaching GDB...")
                gdb.attach(p, gdbscript=gdbscript)
                log.success("GDB attached successfully")
        except Exception as e:
            log.error(f"Failed to start process: {e}")
            return None
    
    if p:
        # 包装连接对象并设置为当前连接
        wrapped_conn = ConnectionWrapper(p)
        return wrapped_conn
    
    return None
