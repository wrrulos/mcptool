import json
import os

from src.decoration.paint import paint
from src.managers.json_manager import JsonManager
from src.utilities.check_utilities import CheckUtilities
from src.utilities.get_utilities import GetUtilities


def language_command(language, *args):
    """
    Change the language of the application.

    Args:
        language (str): The desired language code.
        *args: Additional arguments (not used in this function).
    """

    language = language.lower()
    valid_languages = GetUtilities.get_valid_languages()

    if not CheckUtilities.check_language(language):
        # Check if the provided language is valid, display an error if not.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidLanguage"])}')
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "language", "languageList"]).replace("[0]", valid_languages)}')
        return

    if JsonManager.get('lang') == language:
        # Check if the selected language is already in use.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "language", "languageInUse"])}')
        return

    with open(f'./config/lang/{language}.json', 'r', encoding='utf8') as f:
        new_language = json.loads(f.read())

    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "language", "changeOfLanguage"]).replace("[0]", new_language["languageName"])}')

    settings = JsonManager.load_json('./config/config.json')
    settings['lang'] = language
    JsonManager.save_json(settings, './config/config.json')
