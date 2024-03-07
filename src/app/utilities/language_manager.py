import os

from app.utilities.json_manager import JsonManager as JM


class LanguageManager:
    def __init__(self):
        self.language = "en"

    def get(self, key):
        """
        Method to get the text in the current language
        """

        language_file = self.get_language()

        if not os.path.exists(language_file):
            return 'None'
        
        return JM(language_file).get(key)

    def set_language(self, language):
        self.language = language

    def get_language(self):
        return f'./languages/s{self.language}.json'