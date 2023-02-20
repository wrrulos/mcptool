#!/usr/bin/python3

import requests

from utils.gets.Language import language
from utils.color.TextColor import paint


def dnslookup_command(domain):
    """ 
    Get the dns records of the domain. 
    
    :param domain: Domain
    """

    try:
        dns_records = ['A', 'AAAA', 'CAA', 'CNAME', 'MX', 'SRV', 'TXT', 'NS', 'SOA']
        r = requests.get(f'https://api.hackertarget.com/dnslookup/?q={domain}')
        content = r.text

        if 'error input invalid - enter IP or Hostname' in content or 'try reverse dns tool for ipaddress' in content:
            paint(f'\n    {language["commands"]["ERROR"]}{language["commands"]["dnslookup"]["INVALID_DOMAIN"]}')
            return

        output = r.text.split('\n')
        print('')
        
        for line in output:
            for record in dns_records:
                if 'AAAA : ' in line:
                    line = line.replace('AAAA : ', '[red][[lred]AAAA[red]] [lwhite]')

                elif 'SOA : ' in line:
                    line = line.replace('SOA : ', '[red][[lred]SOA[red]] [lwhite]')

                else:
                    line = line.replace(f'{record} : ', f'[red][[lred]{record}[red]] [lwhite]')

            paint(f'    {line}')

    except KeyboardInterrupt:
        return
    