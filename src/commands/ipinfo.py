from src.decoration.paint import paint
from src.decoration.mccolor.mc_remove import mcremove
from src.managers.json_manager import JsonManager
from src.utilities.get_utilities import GetUtilities
from src.utilities.check_utilities import CheckUtilities
from src.managers.log_manager import LogManager


def ipinfo_command(ip_address, *args):
    """
    Get information about an IP address including its geolocation and reverse DNS.

    Args:
        ip_address (str): IP Address or filename containing IP addresses.
        *args: Additional arguments.
    """

    try:
        # Check if the provided IP address is valid.
        if not CheckUtilities.check_ip_address(ip_address):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidIP"]).replace("[0]", ip_address)}')
            return

        # Get information about the IP address.
        ip_address_information = GetUtilities.get_ip_info(ip_address)
        
        if ip_address_information is None:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidIP"]).replace("[0]", ip_address)}')
            return
        
        if JsonManager.get('logs'):
            log_file = LogManager.create_log_file('ipinfo')
            LogManager.write_log(log_file, 'ipinfo', f'IP: {ip_address}\n')

        if ip_address_information[0] is not None:
            # Display geolocation information.
            paint(f'\n{GetUtilities.get_spaces()}&4[{GetUtilities.get_translated_text(["commands", "ipinfo", "result1"])}&4] &f&l{ip_address_information[0]["continent"]} (&c{ip_address_information[0]["continentCode"]}&f&l)')
            paint(f'{GetUtilities.get_spaces()}&4[{GetUtilities.get_translated_text(["commands", "ipinfo", "result2"])}&4] &f&l{ip_address_information[0]["country"]} (&c{ip_address_information[0]["countryCode"]}&f&l)')
            paint(f'{GetUtilities.get_spaces()}&4[{GetUtilities.get_translated_text(["commands", "ipinfo", "result3"])}&4] &f&l{ip_address_information[0]["regionName"]} (&c{ip_address_information[0]["region"]}&f&l)')
            paint(f'{GetUtilities.get_spaces()}&4[{GetUtilities.get_translated_text(["commands", "ipinfo", "result4"])}&4] &f&l{ip_address_information[0]["city"]} (&c{ip_address_information[0]["timezone"]}&f&l)')
            paint(f'{GetUtilities.get_spaces()}&4[{GetUtilities.get_translated_text(["commands", "ipinfo", "result5"])}&4] &f&l{ip_address_information[0]["isp"]} (&c{ip_address_information[0]["org"]}&f&l)')
            
            log_data = f'''
[{GetUtilities.get_translated_text(["commands", "ipinfo", "result1"])} {ip_address_information[0]["continent"]} ({ip_address_information[0]["continentCode"]})
[{GetUtilities.get_translated_text(["commands", "ipinfo", "result2"])}] {ip_address_information[0]["country"]} ({ip_address_information[0]["countryCode"]})
[{GetUtilities.get_translated_text(["commands", "ipinfo", "result3"])}] {ip_address_information[0]["regionName"]} ({ip_address_information[0]["region"]})
[{GetUtilities.get_translated_text(["commands", "ipinfo", "result4"])}] {ip_address_information[0]["city"]} ({ip_address_information[0]["timezone"]})
[{GetUtilities.get_translated_text(["commands", "ipinfo", "result5"])}] {ip_address_information[0]["isp"]} ({ip_address_information[0]["org"]})
            '''

            if ip_address_information[0]['asname'] != '':
                paint(f'{GetUtilities.get_spaces()}&4[{GetUtilities.get_translated_text(["commands", "ipinfo", "result6"])}&4] &f&l{ip_address_information[0]["asname"]} (&c{ip_address_information[0]["as"]}&f&l)')

        if ip_address_information[1] is not None:
            if type(ip_address_information[1]) == list:
                # Display reverse DNS information for multiple domains.
                for domain in ip_address_information[1]:
                    paint(f'{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ipinfo", "reverse"])} &f&l{domain}')
                    log_data += f'{GetUtilities.get_translated_text(["commands", "ipinfo", "reverse"])} {domain}'
            else:
                # Display reverse DNS information for a single domain.
                paint(f'{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ipinfo", "reverse"])} &f&l{ip_address_information[1]}')
                log_data += f'{GetUtilities.get_translated_text(["commands", "ipinfo", "reverse"])} {ip_address_information[1]}'

        if JsonManager.get('logs'):
            LogManager.write_log(log_file, 'ipinfo', mcremove(log_data))

    except KeyboardInterrupt:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
