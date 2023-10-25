#!/usr/bin/env python3

import traceback
import subprocess
import zipfile
import platform
import shutil
import os
import re
import sys


class Setup:
    python_variable = sys.executable
    hide_output = '>nul 2>&1'
    nmap_link_pattern = r"Latest <u>stable<\/u> release self-installer: <a href=\"(https:\/\/nmap.org\/dist\/nmap-[0-9]+\.[0-9]+[a-z]*-setup\.exe)\" onClick=\""
    ngrok_link_pattern = r'<a\s+id="windows-dl-link"\s+.*?\s+href="(.*?)"\s*>'

    nodejs_modules = [
        'mineflayer',
        'minecraft-colors',
        'proxy-agent',
        'readline',
        'socks',
        'telebit'
    ]

    if os.name == 'nt':
        bits = platform.architecture()[0][:2]
    
    @staticmethod
    def ask(text):
        """
        Ask the user and expect their answer to be y or n.

        Args:
            text (str): Text to be displayed to the user.
        """

        while True:
            answer = input(text).lower()

            if answer == 'y':
                return True
                
            if answer == 'n':
                return False
            
    @staticmethod
    def download(url, file_name):
        """
        Downloads the specified file from the provided URL and saves it with the given file name.

        Args:
            url (str): URL of the file to be downloaded.
            file_name (str): File name to save the downloaded file as.
        """
        import requests

        with open(file_name, 'wb') as f:
            file = requests.get(url)
            f.write(file.content)

    @staticmethod
    def extracting(file, location):
        """
        Extracts the specified .zip file.

        Args:
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
    
    @staticmethod
    def check_by_command(command):
        """
        Check if the command is executed correctly.

        Args:
            command (str): Command to be executed.

        Returns:
            bool: True if the command is executed successfully, False otherwise.
        """

        if subprocess.call(command, shell=True) != 0:
            return False
        
        return True

    @staticmethod
    def check_pip():
        if not Setup.check_by_command(f'{Setup.python_variable} -m pip --version {Setup.hide_output}'):
            print('\n[-] PIP is not installed on the system. I recommend you to install python correctly.')
            sys.exit()


    @staticmethod
    def check_termux():
        """
        Check if MCPTool is running on Termux

        Returns:
            bool: True if "ANDROID_ROOT" is found in `os.environ`
        """

        return 'ANDROID_ROOT' in os.environ
    

    @staticmethod
    def install_nodejs():
        import requests

        if os.name == 'nt':
            response = requests.get('https://nodejs.org/es/download')

            # Extract the download link using regex
            link_match = re.search(r'<a href="([^"]+)">64-bit', response.text)
            if link_match:
                download_link = link_match.group(1)
                Setup.download(download_link, 'NodeJS.msi')
                subprocess.run('NodeJS.msi', shell=True)
                os.remove('NodeJS.msi')

            else:
                print('Failed to extract download link.')
            
        elif Setup.check_termux():
            subprocess.run(f'pkg install nodejs -y {Setup.hide_output}', shell=True)
            print('\n[+] NodeJS installed successfully.')
            
        else:
            subprocess.run('sudo apt install nodejs -y', shell=True)
            subprocess.run('sudo apt install npm -y', shell=True)
            print('\n[+] NodeJS installed successfully.')

    @staticmethod
    def install_java():
        if os.name == 'nt':
            download_link = 'https://download.oracle.com/java/19/archive/jdk-19.0.2_windows-x64_bin.exe'
            Setup.download(download_link, 'jdk-19.0.2_windows-x64_bin.exe')
            subprocess.run('jdk-19.0.2_windows-x64_bin.exe', shell=True)
            os.remove('jdk-19.0.2_windows-x64_bin.exe')
            print('\n[!] Close this terminal and start the script in a new terminal so it can access the Java variables.')
            return

        elif Setup.check_termux():
            subprocess.run(f'pkg install openjdk-17 -y {Setup.hide_output}', shell=True)

        else:
            subprocess.run('sudo apt install openjdk-17-jdk openjdk-17-jre', shell=True)

        print('\n[+] Java installed successfully.')
    
    @staticmethod
    def install_nmap():
        import requests

        if os.name == 'nt':
            response = requests.get('https://nmap.org/download.html')
            html = response.content.decode('utf-8')
            match = re.search(Setup.nmap_link_pattern, html)

            if match:
                download_link = match.group(1)
                Setup.download(download_link, 'Nmap.exe')
                subprocess.run('Nmap.exe', shell=True)
                os.remove('Nmap.exe')

        elif Setup.check_termux():
            subprocess.run(f'pkg install nmap -y {Setup.hide_output}', shell=True)

        else:
            subprocess.run('sudo apt-get install nmap', shell=True)

    @staticmethod
    def install_ngrok():
        import requests

        if os.name == 'nt':
            response = requests.get('https://ngrok.com/download')
            html = response.content.decode('utf-8')
            match = re.search(Setup.ngrok_link_pattern, html)

            if match:
                download_link = match.group(1)
                Setup.download(download_link, 'Ngrok.zip')
                Setup.extracting('Ngrok.zip', 'NgrokZip')
                shutil.copy('NgrokZip/ngrok.exe', 'ngrok.exe')
                shutil.rmtree('NgrokZip')
                os.remove('Ngrok.zip')

        elif Setup.check_termux():
            subprocess.run('pkg update && pkg upgrade -y && pkg install zip -y && pkg install wget -y && wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip && unzip ngrok-stable-linux-arm.zip && chmod +x ngrok', shell=True)
            
        else:
            subprocess.run('curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok', shell=True)

        print('\n[+] Ngrok installed successfully.')

    @staticmethod
    def install_sox():
        subprocess.run(f'pkg install sox -y {Setup.hide_output}', shell=True)
        print('\n[+] Sox installed successfully.')

    @staticmethod
    def start_setup():
        """ 
        Verify and install the dependencies needed to use MCPTool. 
        Also, prepare the configuration file for the user. 
        """

        if Setup.check_termux():
            print('\n[+] Updating APT packages..')
            subprocess.run('apt update && apt upgrade -y', shell=True)

        print('\n[+] Installing the necessary python modules..')
        subprocess.run(f'{Setup.python_variable} -m pip install -r requirements.txt {Setup.hide_output}', shell=True)

        # NodeJS Check
        if not Setup.check_by_command(f'npm --version {Setup.hide_output}'):
            answer = Setup.ask('\n[-] NodeJS is not installed on the system. Do you want to install it automatically? y/n > ')
        
            if answer:
                print('\n[+] Installing NodeJS..')
                Setup.install_nodejs()

            else:
                print('\n[-] Install NodeJS and start the script again.')
                return
        
        print('\n[+] Installing NodeJS modules..')
        for module in Setup.nodejs_modules:
            subprocess.run(f'npm install {module} {Setup.hide_output}', shell=True)

        # Java Check
        if not Setup.check_by_command(f'java -version {Setup.hide_output}'):
            answer = Setup.ask('\n[-] Java is not installed on your system. This dependency is optional. Do you want to install it to access all MCPTool options? y/n > ')

            if answer:
                print('\n[+] Installing Java..')
                Setup.install_java()

        # Nmap Check
        if not Setup.check_by_command(f'nmap --version {Setup.hide_output}'):
            answer = Setup.ask('\n[-] Nmap is not installed on your system. This dependency is optional. Do you want to install it to access all MCPTool options? y/n > ')
            
            if answer:
                print('\n[+] Installing Nmap..')
                Setup.install_nmap()                

        # Ngrok Check
        if not os.path.exists('ngrok') and not os.path.exists('ngrok.exe') and not Setup.check_by_command(f'ngrok version {Setup.hide_output}') and not Setup.check_by_command(f'./ngrok version {Setup.hide_output}'):
            answer = Setup.ask('\n[-] Ngrok is not installed on your system. This dependency is optional. Do you want to install it to access all MCPTool options? y/n > ')
            
            if answer:
                print('\n[+] Installing Ngrok..')
                Setup.install_ngrok()

        if Setup.check_termux():
            if not Setup.check_termux():
                answer = Setup.ask('\n[-] Sox is not installed on your system. This dependency is optional. Do you want to install it to access all MCPTool options? y/n > ')

                if answer:
                    print('\n[+] Installing Sox..')
                    Setup.install_sox()
        

        print(f'\n[+] Now you can start MCPTool! Use the python main.py command')


if __name__ == '__main__':
    try:
        if len(sys.argv) >= 2:
            if sys.argv[1] == '--debug':
                hide_output = ''

        Setup.start_setup()

    except KeyboardInterrupt:
        sys.exit()

    except:
        if len(sys.argv) >= 2:
            if sys.argv[1] == '--debug':
                print(traceback.format_exc())

        print('\n[!] There was an error during the installation. I recommend installing the dependencies manually. All information can be found at: https://www.mcptool.net/how-to-install')