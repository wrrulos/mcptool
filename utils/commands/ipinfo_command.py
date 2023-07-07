import requests

from utils.color.text_color import paint
from utils.managers.language_manager import language_manager
from utils.gets.get_spaces import get_spaces


def ipinfo_command(ip_address):
    """ 
    Get data from the specified IP address 
    using the ip-api API.
    
    Args:
        ip_address (str): IP Address.
    """

    try:
        r = requests.get(f'http://ip-api.com/json/{ip_address}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,timezone,isp,org,as,asname,reverse,query')
        r_json = r.json()

        # If the request is valid.
        if r_json['status'] == 'success':
            continent = r_json['continent']
            continent_code = r_json['continentCode']
            country = r_json['country']
            country_code = r_json['countryCode']
            region = r_json['region']
            region_name = r_json['regionName']
            city = r_json['city']
            timezone = r_json['timezone']
            isp = r_json['isp']
            org = r_json['org']
            as_ = r_json['as']
            asname = r_json['asname']
            reverse = r_json['reverse']

            paint(f'\n{get_spaces()}&4[{language_manager.language["commands"]["ipinfo"]["result1"]}&4] &f&l{continent} (&c{continent_code}&f&l)')
            paint(f'{get_spaces()}&4[{language_manager.language["commands"]["ipinfo"]["result2"]}&4] &f&l{country} (&c{country_code}&f&l)')
            paint(f'{get_spaces()}&4[{language_manager.language["commands"]["ipinfo"]["result3"]}&4] &f&l{region_name} (&c{region}&f&l)')
            paint(f'{get_spaces()}&4[{language_manager.language["commands"]["ipinfo"]["result4"]}&4] &f&l{city} (&c{timezone}&f&l)')
            paint(f'{get_spaces()}&4[{language_manager.language["commands"]["ipinfo"]["result5"]}&4] &f&l{isp} (&c{org}&f&l)')

            if asname != '':
                paint(f'{get_spaces()}&4[{language_manager.language["commands"]["ipinfo"]["result6"]}&4] &f&l{asname} (&c{as_}&f&l) &f&lhttps://ipinfo.io/{as_.split(" ")[0]}')

            if reverse != '':
                paint(f'{get_spaces()}&4[{language_manager.language["commands"]["ipinfo"]["result7"]}&4] &f&l{reverse}')

        else:
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["error"]}{language_manager.language["commands"]["invalidArguments"]["invalidIP"]}')
        
    except requests.exceptions.ConnectionError:
        paint(f'\n{get_spaces()}{language_manager.language["apiConnectionError"]}')

    except KeyboardInterrupt:
        paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
        return
