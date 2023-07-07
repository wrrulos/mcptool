import json

from utils.color.text_color import paint
from utils.managers.language_manager import language_manager
from utils.managers.config_manager import config_manager
from utils.gets.get_spaces import get_spaces


def language_command(lang):
    """ 
    Change the language of the tool
    
    Args:
        lang (str): Language name.
    """

    lang = lang.lower()

    if config_manager.config['lang'] == lang:
        paint(f'\n{get_spaces()}{language_manager.language["commands"]["language"]["languageInUse"]}')
        return
    
    with open(f'config/lang/{lang}.json', 'r', encoding='utf8') as f:
        new_language = json.loads(f.read())

    paint(f'\n{get_spaces()}{language_manager.language["commands"]["language"]["changeOfLanguage"].replace("[0]", new_language["languageName"])}')
    config_manager.config['lang'] = lang
    config_manager.update_settings(config_manager.config)
