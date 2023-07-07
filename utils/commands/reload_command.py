from utils.color.text_color import paint
from utils.gets.get_spaces import get_spaces
from utils.managers.config_manager import config_manager
from utils.managers.language_manager import language_manager


def reload_command():
    config_manager.load_config()
    paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["reload"]["reloading"]}')