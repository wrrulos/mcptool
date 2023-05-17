import os
def is_termux():
    """
    Check if MCPTool is running on Termux
    
    Returns:
        bool: True if "ANDROID_ROOT" is found in `os.environ`
    """
    return "ANDROID_ROOT" in os.environ
def _is_dnspython_fixed():
    """
    Check if resolver.py has been changed so that `mcstatus` (specifically its dependency, `dnspython`) works correctly on Termux.
    
    Returns:
        `True`: path to resolv.conf in dnspython is set to `/data/data/com.termux/files/usr/etc/resolv.conf` or not running on Termux\n
        `False`: Termux environment detected and path to resolv.conf is `/etc/resolv.conf`
    """
    if not is_termux(): return True
    import sys
    filepath = f'/data/data/com.termux/files/usr/lib/python{sys.version_info.major}.{sys.version_info.minor}/dns/resolver.py'
    with open(filepath, 'r') as f:
        text = f.read()
        if '/data/data/com.termux/files/usr/etc/resolv.conf' in text:
            return True
        else: return False
def _fix_dnspython():
    if _is_dnspython_fixed(): return
    import sys
    import fileinput
    filepath = f'/data/data/com.termux/files/usr/lib/python{sys.version_info.major}.{sys.version_info.minor}/dns/resolver.py'
    old_text = '/etc/resolv.conf'
    new_text = '/data/data/com.termux/files/usr/etc/resolv.conf'
    with fileinput.FileInput(filepath, inplace=True) as f:
        for line in f:
            line = line.replace(old_text, new_text)
