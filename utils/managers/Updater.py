#!/usr/bin/python3

import requests
import zipfile
import shutil
import socket
import json
import os

from utils.managers.Settings import SettingsManager

sm = SettingsManager()
settings = sm.read('settings')


class Updater:
    def __init__(self) -> None:
        pass

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
            r = requests.get('https://raw.githubusercontent.com/wrrulos/MCPTool/main/settings/settings.json')  # Get the latest version
            js = json.loads(r.text)
            current_version = settings['CURRENT_VERSION']
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