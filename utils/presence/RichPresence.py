#!/usr/bin/python3

import pypresence
import struct
import time

from pypresence import Presence


def rich_presence():
    """ 
    Show MCPTool status on Discord 
    """
    
    try:
        RPC = Presence('802529947368292404')
        start_time=time.time()
        RPC.connect()

        while True:
            RPC.update(large_image='logo',
                    large_text='The Best Pentesting Tool for Minecraft',
                    details='The Best Pentesting Tool for Minecraft',
                    start=start_time,
                    buttons=[{'label': 'Website', 'url': 'https://github.com/wrrulos/MCPTool'}, {'label': 'Discord', 'url': 'https://discord.gg/ewPyW4Ghzj'}]) 
            time.sleep(10)

    except (pypresence.exceptions.DiscordNotFound, struct.error):
        return

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    rich_presence()