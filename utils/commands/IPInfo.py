#!/usr/bin/python3

import requests

from utils.gets.Language import language
from utils.color.TextColor import paint


def ipinfo_command(ip_address):
    """ 
    Get information about an IP address 
    
    :param ip_address: IP Address
    """

    try:
        r = requests.get(f'http://ip-api.com/json/{ip_address}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,timezone,isp,org,as,asname,reverse,query')
        r_json = r.json()

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

            paint(f'\n    [red][{language["commands"]["ipinfo"]["RESULT_1"]}[red]] [lwhite]{continent} ([lred]{continentCode}[lwhite])')
            paint(f'    [red][{language["commands"]["ipinfo"]["RESULT_2"]}[red]] [lwhite]{country} ([lred]{countryCode}[lwhite])')
            paint(f'    [red][{language["commands"]["ipinfo"]["RESULT_3"]}[red]] [lwhite]{regionName} ([lred]{region}[lwhite])')
            paint(f'    [red][{language["commands"]["ipinfo"]["RESULT_4"]}[red]] [lwhite]{city} ([lred]{timezone}[lwhite])')
            paint(f'    [red][[lred]IS[lwhite]P[red]] [lwhite]{isp} ([lred]{org}[lwhite])')
            
            if asname != '':
                paint(f'    [red][[lred]A[lwhite]S[red]] [lwhite]{asname} ([lred]{as_}[lwhite])')

            if reverse != '':
                paint(f'    [red][[lred]Reve[lwhite]rse[red]] [lwhite]{reverse}')

        else:
            paint(f'{language["commands"]["ERROR"]}{language["commands"]["ipinfo"]["INVALID_IP"]}')
                        
    except requests.exceptions.ConnectionError:
        paint(f'{language["commands"]["API_CONNECTION_ERROR"]}')

    except KeyboardInterrupt:
        return
