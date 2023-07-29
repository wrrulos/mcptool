#!/usr/bin/env python3

import traceback
import subprocess
import zipfile
import platform
import shutil
import time
import os
import re
import sys

python_variable = sys.executable
hide_output = '>nul 2>&1'


def check(command):
    """
    Check if the command is executed correctly.

    Parameters:
        command (str): Command to be executed.

    Returns:
         bool: True if the command is executed successfully, False otherwise.
    """

    if subprocess.call(command, shell=True) != 0:
        return False
    
    return True


if not check(f'{python_variable} -m pip --version {hide_output}'):
    print('\n[-] PIP is not installed on the system. I recommend you to install python correctly.')
    sys.exit()

try:
    import requests

except ImportError:
    print('Requests module it is not installed. Installing..')
    subprocess.run(f'{python_variable} -m pip install requests {hide_output}', shell=True)
    import requests


python_modules = [
    'colorama',
    'requests',
    'dnspython',
    'mcstatus',
    'mcrcon',
    'shodan'
]

nodejs_modules = [
    'mineflayer',
    'minecraft-colors',
    'proxy-agent',
    'readline',
    'socks'
]

nmap_link_pattern = r"Latest <u>stable<\/u> release self-installer: <a href=\"(https:\/\/nmap.org\/dist\/nmap-[0-9]+\.[0-9]+[a-z]*-setup\.exe)\" onClick=\""
ngrok_link_pattern = r'<a\s+id="windows-dl-link"\s+.*?\s+href="(.*?)"\s*>'

if os.name == 'nt':
    bits = platform.architecture()[0][:2]


def check_termux():
    """
    Check if MCPTool is running on Termux

    Returns:
        bool: True if "ANDROID_ROOT" is found in `os.environ`
    """

    return 'ANDROID_ROOT' in os.environ


def ask(text):
    """
    Ask the user and expect their answer to be y or n.

    Parameters:
        text (str): Text to be displayed to the user.
    """

    while True:
        answer = input(text).lower()

        if answer == 'y':
            return True
            
        if answer == 'n':
            return False


def download(url, file_name):
    """
    Downloads the specified file from the provided URL and saves it with the given file name.

    Parameters:
        url (str): URL of the file to be downloaded.
        file_name (str): File name to save the downloaded file as.
    """

    with open(file_name, 'wb') as f:
        file = requests.get(url)
        f.write(file.content)


def extracting(file, location):
    """
    Extracts the specified .zip file.

    Parameters:
        file (str): Path to the .zip file to be extracted.
        location (str): Path to the directory where the contents of the .zip file will be extracted.

    Returns:
        bool: True if the extraction is successful, False otherwise.
    """

    try:
        with zipfile.ZipFile(file, mode="r") as archive:
            archive.extractall(location)
            return True

    except (zipfile.BadZipFile, zipfile.LargeZipFile):
        return False


def setup():
    """ Check and install the dependencies needed to use MCPTool. """
    
    if check_termux():
        subprocess.run('apt update && apt upgrade -y', shell=True)

    print('\n[+] Installing the necessary python modules..')
    time.sleep(1)

    subprocess.run(f'{python_variable} -m pip install --upgrade pip {hide_output}', shell=True)

    for module in python_modules:
        subprocess.run(f'{python_variable} -m pip install {module} {hide_output}', shell=True)

    if not check_termux():
        subprocess.run(f'{python_variable} -m pip install pygame {hide_output}', shell=True)
        subprocess.run(f'{python_variable} -m pip install pypresence {hide_output}', shell=True)
        subprocess.run(f'{python_variable} -m pip install psutil {hide_output}', shell=True)

    # NodejS
    if not check(f'npm --version {hide_output}'):
        answer = ask('\n[-] NodeJS is not installed on the system. Do you want to install it automatically? y/n > ')
        
        if answer:
            if os.name == 'nt':
                response = requests.get('https://nodejs.org/es/download')

                # Extract the download link using regex
                link_match = re.search(r'<a href="([^"]+)">64-bit', response.text)
                if link_match:
                    download_link = link_match.group(1)
                    download(download_link, 'NodeJS.msi')
                    subprocess.run('NodeJS.msi', shell=True)
                    os.remove('NodeJS.msi')

                else:
                    print('Failed to extract download link.')
            
            elif check_termux():
                subprocess.run(f'pkg install nodejs -y {hide_output}', shell=True)
                print('\n[+] NodeJS installed successfully.')
            
            else:
                subprocess.run('sudo apt install nodejs -y', shell=True)
                subprocess.run('sudo apt install npm -y', shell=True)
                print('\n[+] NodeJS installed successfully.')

        else:
            print('\n[-] Install NodeJS and start the script again.')
            return

    print('\n[+] Installing NodeJS modules..')

    for module in nodejs_modules:
        subprocess.run(f'npm install {module} {hide_output}', shell=True)

    # Java
    if not check(f'java -version {hide_output}'):
        answer = ask('\n[-] Java is not installed on your system. This dependency is optional. Do you want to install it to access all MCPTool options? y/n > ')

        if answer:
            print('\n[+] Installing Java..')

            if os.name == 'nt':
                download_link = 'https://download.oracle.com/java/19/archive/jdk-19.0.2_windows-x64_bin.exe'
                download(download_link, 'jdk-19.0.2_windows-x64_bin.exe')
                subprocess.run('jdk-19.0.2_windows-x64_bin.exe', shell=True)
                os.remove('jdk-19.0.2_windows-x64_bin.exe')
                print('\n[!] Close this terminal and start the script in a new terminal so it can access the Java variables.')
                return

            elif check_termux():
                subprocess.run(f'pkg install openjdk-17 -y {hide_output}', shell=True)

            else:
                subprocess.run('sudo apt install openjdk-17-jdk openjdk-17-jre', shell=True)

            print('\n[+] Java installed successfully.')

    # Nmap
    if not check(f'nmap --version {hide_output}'):
        answer = ask('\n[-] Nmap is not installed on your system. This dependency is optional. Do you want to install it to access all MCPTool options? y/n > ')
        
        if answer:
            print('\n[+] Installing Nmap..')

            if os.name == 'nt':
                response = requests.get('https://nmap.org/download.html')
                html = response.content.decode('utf-8')
                match = re.search(nmap_link_pattern, html)

                if match:
                    download_link = match.group(1)
                    download(download_link, 'Nmap.exe')
                    subprocess.run('Nmap.exe', shell=True)
                    os.remove('Nmap.exe')

            elif check_termux():
                subprocess.run(f'pkg install nmap -y {hide_output}', shell=True)

            else:
                subprocess.run('sudo apt-get install nmap', shell=True)

            print('\n[+] Nmap installed successfully.')

    # Ngrok
    if not os.path.exists('ngrok') and not os.path.exists('ngrok.exe') and not check(f'ngrok version {hide_output}'):
        answer = ask('\n[-] Ngrok is not installed on your system. This dependency is optional. Do you want to install it to access all MCPTool options? y/n > ')
        
        if answer:
            print('\n[+] Installing Ngrok..')

            if os.name == 'nt':
                response = requests.get('https://ngrok.com/download')
                html = response.content.decode('utf-8')
                match = re.search(ngrok_link_pattern, html)

                if match:
                    download_link = match.group(1)
                    download(download_link, 'Ngrok.zip')
                    extracting('Ngrok.zip', 'NgrokZip')
                    shutil.copy('NgrokZip/ngrok.exe', 'ngrok.exe')
                    shutil.rmtree('NgrokZip')
                    os.remove('Ngrok.zip')

            elif check_termux():
                subprocess.run('pkg update && pkg upgrade -y && pkg install zip -y && pkg install wget -y && wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip && unzip ngrok-stable-linux-arm.zip && chmod +x ngrok', shell=True)
            
            else:
                subprocess.run('curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok', shell=True)

            print('\n[+] Ngrok installed successfully.')

    # Sox (Termux)
    if check_termux():
        if not check('play --version'):
            answer = ask('\n[-] Sox is not installed on your system. This dependency is optional. Do you want to install it to access all MCPTool options? y/n > ')

            if answer:
                print('\n[+] Installing Sox..')
                subprocess.run(f'pkg install sox -y {hide_output}', shell=True)
                print('\n[+] Sox installed successfully.')

    print(f'\n[+] Now you can start MCPTool! Use the python main.py command')


if __name__ == '__main__':
    try:
        if len(sys.argv) >= 2:
            if sys.argv[1] == '--debug':
                hide_output = ''

        setup()

    except KeyboardInterrupt:
        sys.exit()

    except:
        if len(sys.argv) >= 2:
            if sys.argv[1] == '--debug':
                print(traceback.format_exc())

        print('\n[!] There was an error during the installation. I recommend installing the dependencies manually. All information can be found at: https://www.mcptool.net/how-to-install')
