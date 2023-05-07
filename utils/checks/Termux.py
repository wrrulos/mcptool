import os
def is_termux():
    """
    Check if running on Termux
    
    Returns:
        bool: True if "ANDROID_ROOT" is found in `os.environ`
    """
    return "ANDROID_ROOT" in os.environ