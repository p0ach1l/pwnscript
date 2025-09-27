import inspect
from pwn import log

def ls(data):
    log.success(data)

def lsl(data):
    """
    高亮打印bytes类型的长度
    显示十进制和十六进制格式
    自动获取变量名并显示为 "变量名 length"
    """
    if isinstance(data, bytes):
        length = len(data)
        
        # 获取调用者的栈帧
        frame = inspect.currentframe().f_back
        
        # 尝试找到传入参数的变量名
        var_name = "data"  # 默认名称
        for name, value in frame.f_locals.items():
            if value is data:
                var_name = name
                break
        
        # 如果在局部变量中没找到，尝试全局变量
        if var_name == "data":
            for name, value in frame.f_globals.items():
                if value is data:
                    var_name = name
                    break
        
        ls('\033[1;31;40m%s length ---> %d (0x%x) \033[0m' % (var_name, length, length))
    else:
        ls("Error: lsb() requires bytes type, got %s" % type(data).__name__)

def lss(s):
    """
    增强的变量显示函数
    支持两种用法:
    1. lss("variable_name") - 传入变量名字符串
    2. lss(variable_value) - 直接传入变量值
    """
    if isinstance(s, str):
        # 字符串模式：查找变量名对应的值
        frame = inspect.currentframe().f_back
        value = frame.f_locals.get(s)
        if value is None:
            # 尝试在全局作用域查找
            value = frame.f_globals.get(s)
        
        if value is None:
            ls("Variable '%s' not found." % s)
        else:
            # 根据数据类型选择显示格式
            if isinstance(value, int):
                if value >= 0:
                    ls('\033[1;31;40m%s ---> 0x%x \033[0m' % (s, value))
                else:
                    ls('\033[1;31;40m%s ---> -0x%x \033[0m' % (s, -value))
            elif isinstance(value, bytes):
                hex_repr = value.hex() if len(value) <= 8 else value[:8].hex() + "..."
                ls('\033[1;31;40m%s ---> %s (0x%s) \033[0m' % (s, value, hex_repr))
            else:
                ls('\033[1;31;40m%s ---> %s \033[0m' % (s, value))
    else:
        # 直接值模式：显示值本身，并尝试获取变量名
        frame = inspect.currentframe().f_back
        
        # 尝试找到传入参数的变量名
        var_name = "value"  # 默认名称
        for name, value in frame.f_locals.items():
            if value is s:
                var_name = name
                break
        
        # 如果在局部变量中没找到，尝试全局变量
        if var_name == "value":
            for name, value in frame.f_globals.items():
                if value is s:
                    var_name = name
                    break
        
        if isinstance(s, int):
            if s >= 0:
                ls('\033[1;31;40m%s ---> 0x%x \033[0m' % (var_name, s))
            else:
                ls('\033[1;31;40m%s ---> -0x%x \033[0m' % (var_name, -s))
        elif isinstance(s, bytes):
            hex_repr = s.hex() if len(s) <= 8 else s[:8].hex() + "..."
            ls('\033[1;31;40m%s ---> %s (0x%s) \033[0m' % (var_name, s, hex_repr))
        else:
            ls('\033[1;31;40m%s ---> %s \033[0m' % (var_name, s))
