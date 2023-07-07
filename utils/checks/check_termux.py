import os


def check_termux():
    """
    Check if MCPTool is running on Termux

    Returns:
        bool: True if "ANDROID_ROOT" is found in `os.environ`
    """

    return 'ANDROID_ROOT' in os.environ
