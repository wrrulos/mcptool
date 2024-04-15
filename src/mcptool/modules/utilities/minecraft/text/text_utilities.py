import json

from typing import Union


class TextUtilities:
    @staticmethod
    def get_text_from_json(json_str) -> Union[str, None]:
        """
        Get text from json string

        Args:
            json_str (str): Json string

        Returns:
            Union[str, None]: Text or None
        """

        try:
            obj = json.loads(json_str)

        except:
            return None

        text: str = ''

        def process_extra(extra):
            nonlocal text
            
            if isinstance(extra, list):
                for item in extra:
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

        if isinstance(obj.get('extra'), list):
            process_extra(obj['extra'])

        elif 'text' in obj:
            text = obj['text']

        elif 'translate' in obj:
            text = obj['translate']

        return text.strip()
