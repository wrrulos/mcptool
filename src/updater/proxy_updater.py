import requests
import socket
import json
import time
import sys

from src.updater.update_velocity import update_velocity
from src.updater.update_waterfall import update_waterfall
from src.decoration.print_banner import print_banner
from src.managers.json_manager import JsonManager
from src.utilities.get_utilities import GetUtilities
from src.utilities.check_utilities import CheckUtilities
from src.decoration.paint import paint


class ProxyUpdater:
    @staticmethod
    def update_proxies():
        """
        Check for updates for WaterFall and Velocity proxies and update them if necessary.

        This function checks for updates for the WaterFall and Velocity proxies, and if updates are available, it updates them.
        """

        proxy_update_name = 'proxy_update' if not CheckUtilities.check_termux() else 'proxy_update_termux'
        print_banner(proxy_update_name)
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "updateCheck"]).replace("[0]", "WaterFall")}')

        try:
            url = ProxyUpdater.check_waterfall_update()

            if url is not None:
                paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "updateAvailable"]).replace("[0]", "WaterFall")}')
                update_waterfall(url)
            
            else:
                paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "noUpdatesFound"])}')

            time.sleep(1)
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "updateCheck"]).replace("[0]", "Velocity")}')
            url = ProxyUpdater.check_velocity_update()

            if url is not None:
                paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "updateAvailable"]).replace("[0]", "Velocity")}')
                update_velocity(url)

            else:
                paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "noUpdatesFound"])}')

            time.sleep(1)

        except KeyError:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "updateFailed"])}')
            time.sleep(1)

        except KeyboardInterrupt:
            return
    
    @staticmethod
    def check_waterfall_update():
        """
        Check if a new version of waterfall is available.

        Returns:
            str or None: The URL of the latest Velocity version download if an update is available,
            None otherwise.
        """

        try:
            last_version = requests.get('https://api.papermc.io/v2/projects/waterfall').json()['versions'][-1]
            latest_build = requests.get(f'https://api.papermc.io/v2/projects/waterfall/versions/{last_version}/builds/').json()['builds'][-1]
            build, name = latest_build['build'], latest_build['downloads']['application']['name']
            url = f'https://api.papermc.io/v2/projects/waterfall/versions/{last_version}/builds/{build}/downloads/{name}'

            if JsonManager.get(["proxyConfig", "waterfallVersion"]) != url:
                settings = JsonManager.load_json('./config/config.json')
                settings['proxyConfig']['waterfallVersion'] = url
                JsonManager.save_json(settings, './config/config.json')
                return url
    
        except (socket.gaierror, socket.timeout, requests.ConnectionError, requests.ConnectTimeout, KeyboardInterrupt):
            return None
        
    @staticmethod
    def check_velocity_update():
        """
        Check if a new version of Velocity is available.

        Returns:
            str or None: The URL of the latest Velocity version download if an update is available,
            None otherwise.
        """

        try:
            last_version = requests.get('https://api.papermc.io/v2/projects/velocity').json()['versions'][-1]
            latest_build = requests.get(f'https://api.papermc.io/v2/projects/velocity/versions/{last_version}/builds/').json()['builds'][-1]
            build, name = latest_build['build'], latest_build['downloads']['application']['name']
            url = f'https://api.papermc.io/v2/projects/velocity/versions/{last_version}/builds/{build}/downloads/{name}'

            if JsonManager.get(["proxyConfig", "velocityVersion"]) != url:
                settings = JsonManager.load_json('./config/config.json')
                settings['proxyConfig']['velocityVersion'] = url
                JsonManager.save_json(settings, './config/config.json')
                return url
    
        except (socket.gaierror, socket.timeout, requests.ConnectionError, requests.ConnectTimeout, KeyboardInterrupt):
            return None