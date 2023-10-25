from src.decoration.paint import paint
from src.utilities.get_utilities import GetUtilities
from src.managers.log_manager import LogManager


def dnslookup(domain, *args):
    """
    Perform DNS lookups for various types of DNS records for a given domain.

    Args:
        domain (str): The domain name or IP address for which DNS records are to be retrieved.
        *args: Additional arguments.
    """

    try:
        # List of DNS record types to look up
        dns_records = [
            'A', 'AAAA', 'CNAME', 'MX', 'NS', 'PTR', 'SOA', 'SRV', 'TXT',
            'CAA', 'SPF', 'NAPTR'
        ]

        # Initialize variables for logging
        log_file = LogManager.create_log_file('dnslookup')
        log_data = f'Domain: {domain}\n'
        founds = False

        for dns_record in dns_records:
            # Retrieve DNS records for the specified domain and record type
            output = GetUtilities.get_dns_records(domain, dns_record)

            if output is not None and len(output) >= 1:
                for i in output:
                    if not founds:
                        paint('')

                    # Display each DNS record
                    paint(f'{GetUtilities.get_spaces()}&4[&c{dns_record}&4] &f&l{i}')
                    log_data += f'[{dns_record}] {i}\n'
                    founds = True

                log_data += '\n'
                LogManager.write_log(log_file, 'dnslookup', log_data)

        if not founds:
            # Display a message if no DNS records were found for the domain
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "dnslookup", "withoutResults"])}')

    except KeyboardInterrupt:
        # Handle Ctrl+C interruption gracefully
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')