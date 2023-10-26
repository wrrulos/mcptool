import sys


def fix(filepath):
    try:
        old_text = '/etc/resolv.conf'
        new_text = '/data/data/com.termux/files/usr/etc/resolv.conf'

        # Check if the file has already been modified
        with open(filepath, 'r') as f:
            if f'/data/data/com.termux/files/usr/etc/resolv.conf' in f.read():
                return

        # Read the file and replace the old text with the new text
        with open(filepath, 'r') as file:
            lines = file.readlines()

        updated_lines = [line.replace(old_text, new_text) for line in lines]

        # Write the updated content back to the file
        with open(filepath, 'w') as file:
            file.writelines(updated_lines)

        return True

    except FileNotFoundError:
        return False


def fix_dnspython():
    """
    This function fixes a specific issue related to 
    the 'resolver.py' file in the 'dnspython' package.

    It first checks if the target file has already been 
    modified by searching for a specific path in its content. 
    If the path is found, the function returns without making 
    any changes.

    If the path is not found, the function reads the content 
    of the file, replaces the old text with the new text, and 
    then writes the updated content back to the file.
    """

    filepath = f'/data/data/com.termux/files/usr/lib/python{sys.version_info.major}.{sys.version_info.minor}/dns/resolver.py'

    if not fix(filepath):
        filepath = f'/data/data/com.termux/files/usr/lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages/dns/resolver.py'
        fix(filepath)
