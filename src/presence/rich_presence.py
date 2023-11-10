#!/usr/bin/env python3

import pypresence
import struct
import sys
import time


class RichPresenceUpdater:
    @staticmethod
    def get_rp_status():
        """
        Returns the RichPresence status.

        Returns:
            bool: RichPresence Status.
        """

        with open('mcptool_files/presence/richPresence.status', 'r') as f:
            if f.read() == 'True':
                return True

        return False

    @staticmethod
    def get_last_command():
        """
        Returns the last command used by the user.

        Returns:
            str: Command
        """

        with open('mcptool_files/presence/richPresence.command', 'r') as f:
            return f.read()

    @staticmethod
    def change_rp_status(status):
        """
        Change the state of RichPresence.

        Args:
            status (str): RichPresence Status.
        """

        with open('mcptool_files/presence/richPresence.status', 'w+') as f:
            f.truncate(0)
            f.write(status)

    @staticmethod
    def change_last_command(command):
        """
        Change the last command of the RichPresence status.

        Args:
            command (str): Command.

        Returns:
            None
        """

        with open('mcptool_files/presence/richPresence.command', 'w+') as f:
            f.truncate(0)
            f.write(command.capitalize())


    @staticmethod
    def update_rich_presence(client_id, mcptool_version):
        """
        Shows the status of MCPTool in Discord.

        This is updated each time a command is executed.

        It also prevents it from running twice.
        Create a temporary file so that its execution can be detected.
        """

        try:
            logo = 'logo'
            small_image = 'small_logo'
            RichPresenceUpdater.change_rp_status('False')

            time.sleep(3)
            rpc = pypresence.Presence(client_id)
            start_time = time.time()
            rpc.connect()
            RichPresenceUpdater.change_rp_status('True')

            while True:
                try:
                    if not RichPresenceUpdater.get_rp_status():
                        return

                    last_command = RichPresenceUpdater.get_last_command()
                    state = f'Using the {last_command} command' if last_command != 'In the main menu' else 'In the main menu'

                    rpc.update(
                        state=state,
                        details='Pentesting Tool for Minecraft',
                        start=start_time,
                        large_image=logo,
                        large_text='Pentesting Tool for Minecraft',
                        small_image=small_image,
                        small_text=f'Version: {mcptool_version}',
                        buttons=[
                            {'label': 'Website', 'url': 'https://www.mcptool.net'},
                            {'label': 'Discord', 'url': 'https://discord.gg/TWKs6BWkR2'}
                        ]
                    )

                    time.sleep(1)

                except KeyboardInterrupt:
                    pass

                except RuntimeError:
                    print('RuntimeError! PyPresence')

        except (pypresence.exceptions.DiscordNotFound, struct.error, pypresence.exceptions.ServerError, pypresence.exceptions.ResponseTimeout):
            return

        except (KeyboardInterrupt, ValueError, RuntimeError, OSError):
            pass


if __name__ == "__main__":
    RichPresenceUpdater.update_rich_presence('1127920414383943801', sys.argv[1])
