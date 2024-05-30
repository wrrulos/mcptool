"""
Executable file for the MCPTool

This file is used to run the MCPTool from the command line
"""

import subprocess
import sys
import os

from mccolors import mcwrite
from mcptool import MCPTool

from mcptool.modules.utilities.update import update_utilities

FOLDER_NAME: str = 'MCPTool'


def update_tool() -> None:
    """
    Function to update the tool. It checks if there is an update available
    and updates the tool if there is one.
    """

    update_available: bool = update_utilities.UpdateUtilities.update_available()

    if not update_available:
        mcwrite('There are no updates available.')
        sys.exit(0)

    if os.name == 'nt':
        path: str = os.path.abspath(os.path.join(os.getenv('APPDATA'), FOLDER_NAME))

    else:
        #path = os.path.abspath(os.path.join(os.getenv('HOME'), '.config', FOLDER_NAME))
        print('Automatic update is not available for this OS. Please update manually.')
        sys.exit(0)

    subprocess.Popen(f'cd {path} && MCPToolUpdater.exe', shell=True)
    sys.exit(0)


def main() -> None:
    """
    Main function to run the MCPTool
    """

    help_message: str = """
&f&lUsage: &a&lmcptool [command]

&f&lCommands:

&f&l  help &8- &f&lShow the help message
&f&l  version &8- &f&lShow the version of the tool
&f&l  update &8- &f&lUpdate the tool
"""

    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            mcwrite(help_message)

        if sys.argv[1] == 'version':
            mcwrite(MCPTool.__version__)

        if sys.argv[1] == 'update':
            update_tool()

        sys.exit(0)

    MCPTool().run()


if __name__ == '__main__':
    update_tool()
    main()