import requests

from utils.color.TextColor import paint
from utils.gets.Language import language
from utils.managers.Settings import SettingsManager

sm = SettingsManager()
settings = sm.read('settings')


def reverseip_command(ip_address):
    """ 
    Use the hackertarget API to get the hostnames 
    that have DNS (A) records associated with the 
    specified IP address.
    
    Parameters:
        ip_address (str): IP Address.
    """

    try:
        # Check if the user entered a hackertarget key in the settings.
        if settings['HACKERTARGET_API_KEY'] != '':
            r = requests.get(f'https://api.hackertarget.com/reverseiplookup/?q={ip_address}&apikey={settings["HACKERTARGET_API_KEY"]}')

        else:
            r = requests.get(f'https://api.hackertarget.com/reverseiplookup/?q={ip_address}')

        content = r.text

        if 'error check your search parameter' in content:
            paint(f'\n    {language["commands"]["ERROR"]}{language["commands"]["INVALID_ARGUMENTS"]["INVALID_IP"]}')
            return

        if 'Error invalid key' in content:
            paint(f'\n    {language["commands"]["ERROR"]}{language["other_messages"]["HACKERTARGET_INVALID_API_KEY"]}')
            return

        if 'API count exceeded - Increase Quota with Membership' in content:
            paint(f'\n    {language["commands"]["ERROR"]}{language["other_messages"]["HACKERTARGET_API_LIMIT_EXCEEDED"]}')
            return

        output = r.text.split('\n')
        print('')
        
        for line in output:
            paint(f'    {language["commands"]["reverseip"]["RESULT"]} &f&l{line}')

    except KeyboardInterrupt:
        return
