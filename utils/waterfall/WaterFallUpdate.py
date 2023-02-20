#!/usr/bin/python3

import requests
import json

from utils.waterfall.UpdateWaterFall import update_waterfall
from utils.managers.Settings import SettingsManager
from utils.gets.Language import language
from utils.color.TextColor import paint

sm = SettingsManager()
settings = sm.read('settings')


def search_for_waterfall_updates():
    """
    Check for waterfall updates
    """

    paint(f'\n    {language["script"]["PREFIX"]}{language["waterfall_messages"]["UPDATE_CHECK"]}')
    r = requests.get('https://raw.githubusercontent.com/wrrulos/MCPTool/main/settings/settings.json')
    github_settings = json.loads(r.text)

    if github_settings['WATERFALL_VERSION'] != settings['WATERFALL_VERSION']:
        paint(f'\n    {language["script"]["PREFIX"]}{language["waterfall_messages"]["UPDATE_AVAILABLE"]}')
        sm.write('settings', 'WATERFALL_VERSION', github_settings['WATERFALL_VERSION'])
        update_waterfall(github_settings['WATERFALL_VERSION'])
        return

    paint(f'\n    {language["script"]["PREFIX"]}{language["waterfall_messages"]["NO_UPDATES_FOUND"]}')




    


