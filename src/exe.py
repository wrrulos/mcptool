"""
Executable file for the MCPTool

This file is used to run the MCPTool from the command line
"""

import subprocess
import shutil
import sys
import os

from mccolors import mcwrite

from mcptool.modules.utilities.constants import MCPTOOL_WEBSITE
from mcptool.modules.utilities.constants.update_available import UPDATE_AVAILABLE
from mcptool.modules.utilities.notificactions.send import SendNotification


FOLDER_NAME: str = 'MCPTool'


def update_tool() -> None:
    """
    Function to update the tool. It checks if there is an update available
    and updates the tool if there is one.
    """

    if not UPDATE_AVAILABLE:
        mcwrite('There are no updates available.')
        sys.exit(0)

    SendNotification(
        title='MCPTool Update Available',
        message=f'An update is available for MCPTool. Starting the update process. Visit {MCPTOOL_WEBSITE} for more information.'
    ).send()

    if os.name == 'nt':
        # Paths
        appdata_path: str = os.getenv('APPDATA')  #* %appdata%
        lib_folder_path: str = os.path.abspath(os.path.join(appdata_path, 'lib'))  #* %appdata%/lib
        mcptool_folder_path: str = os.path.abspath(os.path.join(appdata_path, FOLDER_NAME))  #* %appdata%/MCPTool
        mcptool_lib_folder_path: str = os.path.abspath(os.path.join(mcptool_folder_path, 'lib'))  #* %appdata%/MCPTool/lib
        original_updater_path = os.path.join(mcptool_folder_path, 'MCPToolUpdater.exe')  #* %appdata%/MCPTool/MCPToolUpdater.exe
        updater_executable = os.path.join(appdata_path, 'MCPToolUpdater.exe')  #* %appdata%/MCPToolUpdater.exe
        # Command to run the updater with elevated privileges
        command = f'powershell -Command "Start-Process \'{updater_executable}\' -Verb runAs"'

        # Copy ./lib and *.dll python files to the %APPDATA% folder
        if os.path.exists(lib_folder_path):
            shutil.rmtree(lib_folder_path)

        shutil.copytree(mcptool_lib_folder_path, lib_folder_path)

        for file in os.listdir(appdata_path):
            if file.endswith('.dll'):
                if 'python' in file:
                    os.remove(os.path.join(appdata_path, file))
                    shutil.copyfile(os.path.join(appdata_path, file), os.path.join(mcptool_folder_path, file))

        # Copy the updater to the %APPDATA% folder
        if os.path.exists(updater_executable):
            os.remove(updater_executable)

        shutil.copyfile(original_updater_path, updater_executable)

        # Run the updater
        subprocess.run(command, shell=True)
        sys.exit(0)

    else:
        print('Automatic update is not available for this OS. Please update manually.')
        sys.exit(0)


def main() -> None:
    """
    Main function to run the MCPTool
    """

    from mcptool import MCPTool

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
            sys.exit(0)

        if sys.argv[1] == 'version':
            mcwrite(MCPTool.__version__)
            sys.exit(0)

        if sys.argv[1] == 'update':
            update_tool()

    MCPTool().run()


if __name__ == '__main__':
    update_tool()
    main()
