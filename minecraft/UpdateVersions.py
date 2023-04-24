import json
import requests

from utils.color.TextColor import paint
from utils.gets.Language import language


def update_versions():
    """ Update Versions.json and Protocols.json """

    files = ['Versions.json', 'InvalidProtocols.json']

    for file in files:
        with open(f'utils/minecraft/{file}', 'w+') as f:
            new_content = requests.get(f'https://raw.githubusercontent.com/wrrulos/MCPTool/main/utils/minecraft/{file}').text
            json_data = json.loads(new_content)
            f.truncate(0)
            json.dump(json_data, f, indent=4)

    paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["UPDATE_COMPLETED"].replace("[0]", "WaterFall")}')
