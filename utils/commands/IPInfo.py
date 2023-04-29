import requests

from utils.color.TextColor import paint
from utils.gets.Language import language


def ipinfo_command(ip_address):
    """ 
    Get data from the specified IP address 
    using the ip-api API.
    
    Parameters:
        ip_address (str): IP Address.
    """

    try:
        r = requests.get(f'http://ip-api.com/json/{ip_address}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,timezone,isp,org,as,asname,reverse,query')
        r_json = r.json()

        # If the request is valid.
        if r_json['status'] == 'success':
            continent = r_json['continent']
            continentCode = r_json['continentCode']
            country = r_json['country']
            countryCode = r_json['countryCode']
            region = r_json['region']
            regionName = r_json['regionName']
            city = r_json['city']
            timezone = r_json['timezone']
            isp = r_json['isp']
            org = r_json['org']
            as_ = r_json['as']
            asname = r_json['asname']
            reverse = r_json['reverse']

            paint(f'\n    &4[{language["commands"]["ipinfo"]["RESULT_1"]}&4] &f&l{continent} (&c{continentCode}&f&l)')
            paint(f'    &4[{language["commands"]["ipinfo"]["RESULT_2"]}&4] &f&l{country} (&c{countryCode}&f&l)')
            paint(f'    &4[{language["commands"]["ipinfo"]["RESULT_3"]}&4] &f&l{regionName} (&c{region}&f&l)')
            paint(f'    &4[{language["commands"]["ipinfo"]["RESULT_4"]}&4] &f&l{city} (&c{timezone}&f&l)')
            paint(f'    &4[&cIS&f&lP&4] &f&l{isp} (&c{org}&f&l)')
            
            if asname != '':
                paint(f'    &4[&cA&f&lS&4] &f&l{asname} (&c{as_}&f&l)')

            if reverse != '':
                paint(f'    &4[&cReve&f&lrse&4] &f&l{reverse}')

        else:
            paint(f'\n    {language["commands"]["ERROR"]}{language["commands"]["INVALID_ARGUMENTS"]["INVALID_IP"]}')
                        
    except requests.exceptions.ConnectionError:
        paint(f'\n    {language["commands"]["other_messages"]["API_CONNECTION_ERROR"]}')

    except KeyboardInterrupt:
        return
