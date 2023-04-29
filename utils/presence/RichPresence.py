#!/usr/bin/env python3

import pypresence
import struct
import sys
import time

from pypresence import Presence


def get_rp_status():
    """
    Returns the RichPresence status.

    Returns:
        bool: RichPresence Status.
    """

    with open('utils/presence/RichPresence.status', 'r') as f:
        if f.read() == 'True':
            return True
        
        return False
    

def get_last_command():
    """
    Returns the last command used by 
    the user.

    Returns:
        str: Command
    """

    with open('utils/presence/RichPresence.command', 'r') as f:
        return f.read()
    

def change_rp_status(status):
    """
    Change the state of RichPresence.

    Parameters:
        status (str): RichPresence Status.
    """

    with open('utils/presence/RichPresence.status', 'w+') as f:
        f.truncate(0)
        f.write(status)


def rich_presence(mcptool_version):
    """ 
    Shows the status of MCPTool in discord.

    This is updated each time a command is executed.

    It also prevents it from running twice. 
    Create a temporary file so that its execution can be detected.
    """

    try:
        logo = 'logo'
        small_image = 'small_logo'
        change_rp_status('False')

        time.sleep(3)
        RPC = Presence('802529947368292404')
        start_time=time.time()
        RPC.connect()
        change_rp_status('True')

        while True:
            try:
                if not get_rp_status():
                    return

                last_command = get_last_command()
                state = f'Using the {last_command} command' if last_command != 'In the main menu' else 'In the main menu'

                RPC.update(
                    state=state,
                    details='Pentesting Tool for Minecraft',
                    start=start_time,
                    large_image=logo,
                    large_text='Pentesting Tool for Minecraft',
                    small_image=small_image,
                    small_text=f'Version: {mcptool_version}',
                    buttons=[{'label': 'Website', 'url': 'https://www.mcptool.net'}, {'label': 'Discord', 'url': 'https://discord.gg/44YkUxEEqV'}]
                )
                
                time.sleep(1)

            except KeyboardInterrupt:
                pass

    except (pypresence.exceptions.DiscordNotFound, struct.error, pypresence.exceptions.ServerError):
        return

    except (KeyboardInterrupt, ValueError):
        pass


if __name__ == "__main__":
    rich_presence(sys.argv[1])
