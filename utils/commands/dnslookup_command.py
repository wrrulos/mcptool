from utils.color.text_color import paint
from utils.checks.check_domain import check_domain
from utils.gets.get_dns_records import get_dns_records
from utils.managers.language_manager import language_manager
from utils.gets.get_spaces import get_spaces


def dnslookup_command(domain):
    """
    Retrieves DNS records of the specified domain using local DNS lookup.

    Args:
        domain (str): The domain for which DNS records will be retrieved.

    Raises:
        KeyboardInterrupt: If the user interrupts the function execution.
    """

    try:
        dns_records = [
            'A', 'AAAA', 'CNAME', 'MX', 'NS', 'PTR', 'SOA', 'SRV', 'TXT',
            'CAA', 'SPF', 'NAPTR'
        ]

        founds = False

        if not check_domain(domain):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["error"]}{language_manager.language["commands"]["invalidArguments"]["invalidDomain"]}')
            return

        for dns_record in dns_records:
            output = get_dns_records(domain, dns_record)

            if output is not None and len(output) >= 1:
                for i in output:
                    if not founds:
                        paint('')

                    paint(f'{get_spaces()}&4[&c{dns_record}&4] &f&l{i}')
                    founds = True

        if not founds:
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["dnslookup"]["withoutResults"]}')

    except KeyboardInterrupt:
        paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
        return
    
