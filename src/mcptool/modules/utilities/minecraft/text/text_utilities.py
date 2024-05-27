import json

from loguru import logger


class TextUtilities:
    @logger.catch
    @staticmethod
    def get_text_from_json(json_str) -> str:
        """
        Get text from json string

        Args:
            json_str (str): Json string

        Returns:
            str: The text from the json string
        """

        try:
            obj = json.loads(json_str)

        except json.JSONDecodeError:
            return json_str

        text: str = ''

        def process_extra(extra):
            nonlocal text

            if isinstance(extra, list):
                for item in extra:
                    if isinstance(item, str):
                        text += item

                    elif isinstance(item, dict):
                        if 'text' in item:
                            text += item['text']

                        if 'translate' in item:
                            text += item['translate']

                        if 'extra' in item:
                            process_extra(item['extra'])

                        if 'with' in item:
                            text += TextUtilities.get_text_from_json(json.dumps(item['with']))

            elif 'text' in extra:
                text = extra['text']

            elif 'translate' in extra:
                text = extra['translate']

        try:
            if isinstance(obj.get('extra'), list):
                process_extra(obj['extra'])

            elif 'text' in obj:
                text = obj['text']

            elif 'translate' in obj:
                text = obj['translate']

            return text.strip()

        except AttributeError:
            return json_str

    @logger.catch
    @staticmethod
    def minimessage_colors(text: str):
        """
        Replace Minecraft color codes with MiniMessage colored characters.

        Args:
            text (str): Text.

        Returns:
            _type_: New text.
        """

        codes = {
            '0': '<reset><black>',
            '1': '<reset><dark_blue>',
            '2': '<reset><dark_green>',
            '3': '<reset><dark_aqua>',
            '4': '<reset><dark_red>',
            '5': '<reset><dark_purple>',
            '6': '<reset><gold>',
            '7': '<reset><gray>',
            '8': '<reset><dark_gray>',
            '9': '<reset><blue>',
            'a': '<reset><green>',
            'b': '<reset><aqua>',
            'c': '<reset><red>',
            'd': '<reset><light_purple>',
            'e': '<reset><yellow>',
            'f': '<reset><white>',
            'k': '<obfuscated>',
            'l': '<bold>',
            'm': '<strikethrough>',
            'n': '<underlined>',
            'o': '<italic>',
            'r': '<reset>',
            'x': ''
        }

        for code in codes.items():
            text = text.replace(f'&{code[0]}', code[1]).replace(f'§{code[0]}', code[1])
            text = text.replace(f'&{code[0].upper()}', code[1]).replace(f'§{code[0].upper()}', code[1])

        text = text.replace('\n', '<newline>')
        return text

    @logger.catch
    @staticmethod
    def minecraft_colors(text: str):
        """
        Replace MiniMessage colored characters with Minecraft color codes.

        Args:
            text (str): Text.

        Returns:
            _type_: New text.
        """

        codes = {
            '<reset><black>': '0',
            '<reset><dark_blue>': '1',
            '<reset><dark_green>': '2',
            '<reset><dark_aqua>': '3',
            '<reset><dark_red>': '4',
            '<reset><dark_purple>': '5',
            '<reset><gold>': '6',
            '<reset><gray>': '7',
            '<reset><dark_gray>': '8',
            '<reset><blue>': '9',
            '<reset><green>': 'a',
            '<reset><aqua>': 'b',
            '<reset><red>': 'c',
            '<reset><light_purple>': 'd',
            '<reset><yellow>': 'e',
            '<reset><white>': 'f',
            '<obfuscated>': 'k',
            '<bold>': 'l',
            '<strikethrough>': 'm',
            '<underlined>': 'n',
            '<italic>': 'o',
            '<reset>': 'r',
        }

        for code in codes.items():
            text = text.replace(code[0], f'&{code[1]}').replace(code[0], f'&{code[1]}')

        text = text.replace('<newline>', '\n')
        return text