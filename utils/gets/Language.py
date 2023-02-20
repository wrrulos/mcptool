#!/usr/bin/python3

import json
import os

from utils.managers.Settings import SettingsManager

sm = SettingsManager()
settings = sm.read('settings')

if not os.path.exists(f'settings/lang/{settings["LANGUAGE"]}.json'):
    language = None

with open(f'settings/lang/{settings["LANGUAGE"]}.json', 'r', encoding='utf8') as f:
    language = json.loads(f.read())