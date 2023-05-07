import os
import platform
import subprocess
import importlib

def pip_install(name):
    # run command and pipe all output stderr
    subprocess.run(['python3', '-m', 'pip', 'install', name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# try to import all dependencies, if ImportError occurs then install the dependency
for dep in ['pypresence', 'colorama', 'requests', 'mcstatus', 'shodan', 'pygame', 'mcrcon', 'psutil', 'dnspython']:
    if dep == 'pygame':
        if platform.system() == 'Linux' and 'ANDROID_ROOT' in os.environ:
            print('Detected Termux environment, ignoring pygame')
            continue
    try:
        if dep == 'dnspython':
            importlib.import_module('dns')
        else:
            importlib.import_module(dep)
        print(f'{dep} is installed!')
    except ImportError:
        print(f'{dep} not installed, installing...')
        pip_install(dep)