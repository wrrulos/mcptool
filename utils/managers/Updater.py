import json
import os
import requests
import shutil
import socket
import zipfile

from utils.managers.Settings import SettingsManager


class Updater:
    def __init__(self) -> None:
        self.sm = SettingsManager()
        self.settings = self.sm.read('settings')

    def download(self, file, url, location):
        """ Download the specified file """

        try:
            if os.path.exists(location):
                shutil.rmtree(location)

            os.mkdir(location)

            with open(f'{location}/{file}', 'wb') as f:
                file = requests.get(url)
                f.write(file.content)
                return True

        except KeyboardInterrupt:
            return False

    def extracting(self, file, location):
        """ Extracts the specified .zip file """

        with zipfile.ZipFile(file, mode="r") as archive:
            archive.extractall(location)
            return True

    def check_mcptool_updates(self):
        """ Check if there is a new version of MCPTool """

        try:
            js = json.loads(requests.get('https://raw.githubusercontent.com/wrrulos/MCPTool/main/settings/settings.json').text)
            current_version = self.settings['CURRENT_VERSION']
            last_version = js['CURRENT_VERSION']
            versions = last_version.split('///')
            current_versions = current_version.split('///')
            last_version = versions[0]
            current_version = current_versions[0]

            if int(last_version) != int(current_version):
                return True

            return False

        except TypeError:
            return True

        except (socket.gaierror, socket.timeout, requests.ConnectionError, requests.ConnectTimeout, KeyboardInterrupt):
            return False
        
    def check_files_update(self):
        """ Check if a new version is available from the Release Files. """

        try:
            with open('utils/minecraft/Versions.json', 'r') as f:
                js = json.loads(f.read())

            current_version = js['LAST_VERSION']

            js = json.loads(requests.get('https://raw.githubusercontent.com/wrrulos/MCPTool/main/utils/minecraft/Versions.json').text)
            last_version = js['LAST_VERSION']

            if current_version != last_version:
                return True
            
            return False
        
        except (socket.gaierror, socket.timeout, requests.ConnectionError, requests.ConnectTimeout, KeyboardInterrupt):
            return False

    def check_waterfall_update(self):
        """ Check for a new version of Waterfall is available."""

        try:
            last_version = requests.get('https://api.papermc.io/v2/projects/waterfall').json()['versions'][-1]
            latest_build = requests.get(f'https://api.papermc.io/v2/projects/waterfall/versions/{last_version}/builds/').json()['builds'][-1]
            build, name = latest_build['build'], latest_build['downloads']['application']['name']
            url = f'https://api.papermc.io/v2/projects/waterfall/versions/{last_version}/builds/{build}/downloads/{name}'

            if self.settings['WATERFALL_VERSION'] != url:
                self.sm.write('settings', 'WATERFALL_VERSION', url)
                return url
    
        except (socket.gaierror, socket.timeout, requests.ConnectionError, requests.ConnectTimeout, KeyboardInterrupt):
            return
        
    def check_velocity_update(self):
        """ Check for a new version of Velocity is available."""

        try:
            last_version = requests.get('https://api.papermc.io/v2/projects/velocity').json()['versions'][-1]
            latest_build = requests.get(f'https://api.papermc.io/v2/projects/velocity/versions/{last_version}/builds/').json()['builds'][-1]
            build, name = latest_build['build'], latest_build['downloads']['application']['name']
            url = f'https://api.papermc.io/v2/projects/velocity/versions/{last_version}/builds/{build}/downloads/{name}'

            if self.settings['VELOCITY_VERSION'] != url:
                self.sm.write('settings', 'VELOCITY_VERSION', url)
                return url
    
        except (socket.gaierror, socket.timeout, requests.ConnectionError, requests.ConnectTimeout, KeyboardInterrupt):
            return