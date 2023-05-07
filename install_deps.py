import os
import platform
import subprocess
import importlib

deps = ['pypresence', 'colorama', 'requests', 'mcstatus', 'shodan', 'pygame', 'mcrcon', 'psutil', 'dnspython']
ignore_if_termux = ['pypresence', 'pygame', 'psutil']

def pip_install(name):
    # run command and pipe all output stderr
    subprocess.run(['python3', '-m', 'pip', 'install', name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# try to import all dependencies, if ImportError occurs then install the dependency
for dep in deps:
    if dep in ignore_if_termux and platform.system() == 'Linux' and 'ANDROID_ROOT' in os.environ:
        print(f'[{dep}] Detected Termux environment, not installing...')
        continue
    try:
        if dep == 'dnspython':
            importlib.import_module('dns')
        else:
            importlib.import_module(dep)
        print(f'[{dep}] Already present!')
    except ImportError:
        print(f'[{dep}] not installed, installing...')
        pip_install(dep)