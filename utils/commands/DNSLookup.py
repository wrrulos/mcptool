import requests

from utils.color.TextColor import paint
from utils.gets.Language import language
from utils.managers.Settings import SettingsManager

sm = SettingsManager()
settings = sm.read('settings')


def dnslookup_command(domain):
    """ 
    Get the dns records of the specified domain 
    using the Hackertarget API.
    
    Parameters:
        domain (str): Domain.
    """

    try:
        dns_records = ['A', 'AAAA', 'CAA', 'CNAME', 'MX', 'SRV', 'TXT', 'NS', 'SOA']
        r = requests.get(f'https://api.hackertarget.com/dnslookup/?q={domain}')
        content = r.text

        if 'error input invalid - enter IP or Hostname' in content or 'try reverse dns tool for ipaddress' in content:
            paint(f'\n    {language["commands"]["ERROR"]}{language["commands"]["INVALID_ARGUMENTS"]["INVALID_DOMAIN"]}')
            return

        if 'Error invalid key' in content:
            paint(f'\n    {language["commands"]["ERROR"]}{language["HACKERTARGET_INVALID_API_KEY"]}')
            return

        if 'API count exceeded - Increase Quota with Membership' in content:
            paint(f'\n    {language["commands"]["ERROR"]}{language["HACKERTARGET_API_LIMIT_EXCEEDED"]}')
            return

        output = r.text.split('\n')
        print('')
        
        for line in output:
            for record in dns_records:
                if 'AAAA : ' in line:
                    line = line.replace('AAAA : ', '&4[&cAAAA&4] &f&l')

                elif 'SOA : ' in line:
                    line = line.replace('SOA : ', '&4[&cSOA&4] &f&l')

                else:
                    line = line.replace(f'{record} : ', f'&4[&c{record}&4] &f&l')

            paint(f'    {line}')

    except KeyboardInterrupt:
        return
    
