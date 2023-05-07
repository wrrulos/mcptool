import json

from utils.color.TextColor import paint
from utils.gets.Language import language
from utils.managers.Settings import SettingsManager


def language_command(lang):
    """ 
    Change the language of the tool
    
    Parameters:
        language (str): Language
    """

    sm = SettingsManager()
    settings = sm.read('settings')
    lang = lang.lower()

    if settings['LANGUAGE'] == lang:
        paint(f'\n    {language["commands"]["language"]["LANGUAGE_IN_USE"]}')
        return
    
    with open(f'settings/lang/{lang}.json', 'r', encoding='utf8') as f:
        new_language = json.loads(f.read())
        

    paint(f'\n    {language["commands"]["language"]["CHANGE_OF_LANGUAGE"].replace("[0]", new_language["language"])}')
    sm.write('settings', 'LANGUAGE', lang)
