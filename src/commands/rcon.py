from mcrcon_mcpt.mcrcon import MCRcon, MCRconException

from src.decoration.paint import paint
from src.decoration.mccolor import mcreplace
from src.utilities.get_utilities import GetUtilities
from src.utilities.check_utilities import CheckUtilities


def rcon_command(server, password, *args):
    """
    Connects to the specified Minecraft server using RCON and interacts with the server.

    Args:
        server (str): The IP address or domain of the server, along with the RCON port (e.g., "127.0.0.1:25575").
        password (str): The RCON password for authentication.
        *args: Additional arguments (not used in this function).
    """

    try:
        if not CheckUtilities.check_ip_port(server):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "InvalidRconFormat"])}')
            return
        
        # Display a message indicating that an RCON connection is being established
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rcon", "connecting"])}')
        
        # Split the server address and port
        server = server.split(':')
        mcr = None

        with MCRcon(server[0], password, int(server[1]), timeout=35) as mcr:
            # Display a message indicating that the RCON connection has been established
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rcon", "establishedConnection"])}\n')
            
            while True:
                # Prompt the user for an RCON command
                paint(f'{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rcon", "command"])}', '')
                command = input()

                if command == '.exit':
                    # If the user enters '.exit', stop the RCON connection
                    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rcon", "stopping"])}')
                    mcr.disconnect()
                    return

                resp = mcr.command(command)
                resp = mcreplace(resp)
                # Display the RCON command response
                paint(f'\n{GetUtilities.get_spaces()}{resp}')

    except TimeoutError:
        # Handle a timeout error gracefully
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rcon", "timeout"])}')

    except ConnectionRefusedError:
        # Handle a connection refused error gracefully
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rcon", "connectionRefused"])}')

    except MCRconException:
        # Handle an exception indicating an invalid RCON password gracefully
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidRconPassword"])}')
    
    except KeyboardInterrupt:
        if mcr is not None:
            mcr.disconnect()

        # Handle keyboard interruption gracefully.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

    except Exception as e:
        # Handle other exceptions and display the error message
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rcon", "error"]).replace("[0]", str(e))}')
