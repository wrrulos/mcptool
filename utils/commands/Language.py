#!/usr/bin/python3

from utils.managers.Settings import SettingsManager
from utils.gets.Language import language
from utils.color.TextColor import paint

sm = SettingsManager()
settings = sm.read('settings')


def language_command(lang):
    """ 
    Change the language of the tool
    
    :param language: Language
    """

    if settings['LANGUAGE'] == lang:
        paint(f'\n    {language["commands"]["language"]["LANGUAGE_IN_USE"]}')
        return
        
    paint(f'\n    {language["commands"]["language"]["CHANGE_OF_LANGUAGE"].replace("[0]", str(lang).capitalize())}')
    sm.write('settings', 'LANGUAGE', lang)
