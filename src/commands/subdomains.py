import socket
import os

from src.decoration.paint import paint
from src.utilities.get_utilities import GetUtilities
from src.managers.log_manager import LogManager


def subdomains_command(domain, wordlist, *args):
    """
    Find subdomains for a given domain using a wordlist.

    Args:
        domain (str): The target domain to check for subdomains.
        wordlist (str): The path to a text file containing a list of subdomains.
        *args: Additional arguments (not used in this function).
    """
    
    # Create a log file to record the results.
    log_file = LogManager.create_log_file('subdomains')
    
    # Initialize log data with information about the target domain.
    log_data = f'Domain: {domain}\n'

    try:
        # Check if the specified wordlist file exists.
        if not os.path.exists(wordlist):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidFile"]).replace("[0]", wordlist)}')
            return
        
        # Initialize a counter for subdomains found.
        subdomains = 0

        # Read the subdomain list from the provided wordlist file.
        with open(wordlist, 'r', encoding='utf8') as f:
            subdomain_list = f.readlines()

        # Strip newline characters and spaces from subdomains in the list.
        subdomain_list = [subdomain.strip() for subdomain in subdomain_list]
        
        # Display a message indicating the start of the subdomain search.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "subdomains", "lookingForSubdomains"]).replace("[0]", domain)}')

        # Check if there are subdomains in the list to search for.
        if len(subdomain_list) >= 1:
            paint('')

        # Iterate through the subdomain list and attempt to resolve them.
        for subdomain in subdomain_list:
            try:
                host = f'{subdomain}.{domain}'
                ip = socket.gethostbyname(host)
                
                # Display information about the resolved subdomain.
                paint(f'{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "subdomains", "found"]).replace("[0]", host).replace("[1]", ip)}')
                
                # Add the subdomain information to the log data.
                log_data += f'{host} ({ip})\n'
                
                # Increment the subdomains counter.
                subdomains += 1

            except socket.gaierror:
                continue

        # Check if any subdomains were found and report the count.
        if subdomains >= 1:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "subdomains", "subdomainsFound"]).replace("[0]", str(subdomains))}')
            log_data += '\n'
            
            # Write the log data to the log file.
            LogManager.write_log(log_file, 'subdomains', log_data)

        else:
            # Report that no subdomains were found.
            paint(f'{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "subdomains", "subdomainsNotFound"])}')

    except KeyboardInterrupt:
        # Handle a KeyboardInterrupt (Ctrl+C) gracefully.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

    except (UnicodeError, PermissionError):
        # Handle potential Unicode or permission errors when reading the wordlist file.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidFile"]).replace("[0]", wordlist)}')
