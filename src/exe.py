"""
Executable file for the MCPTool

This file is used to run the MCPTool from the command line
"""

import subprocess
import shutil
import time
import sys
import os

from mccolors import mcwrite

from mcptool.modules.utilities.constants import MCPTOOL_WEBSITE
from mcptool.modules.utilities.constants.update_available import UPDATE_AVAILABLE
from mcptool.modules.utilities.notificactions.send import SendNotification


class UpdateTool:
    def __init__(self) -> None:
        pass

    def check_for_update(self) -> None:
        """
        Check if there is an update available for the tool
        """

        if not UPDATE_AVAILABLE:
            mcwrite('&8&l[&a&lINFO&8&l] &f&lNo updates are available for MCPTool. Starting the tool...')
            time.sleep(0.5)
            return

        mcwrite('&8&l[&a&lINFO&8&l] &f&lAn update is available for MCPTool. Starting the update process...')
        SendNotification(
            title='MCPTool Update Available',
            message=f'An update is available for MCPTool. Starting the update process. Visit {MCPTOOL_WEBSITE} for more information.'
        ).send()

        if os.name != 'nt':
            mcwrite('&8&l[&c&lERROR&8&l] &f&lThe update process is only available for Windows. Please visit the MCPTool website to download the latest version.')
            sys.exit(0)

        self.windows_update()

    def windows_update(self) -> None:
        """
        Start the update process for Windows
        """

        # Paths
        appdata_path: str = os.getenv('APPDATA')  #* %appdata%
        lib_folder_path: str = os.path.abspath(os.path.join(appdata_path, 'lib'))  #* %appdata%/lib
        mcptool_folder_path: str = os.path.abspath(os.path.join(appdata_path, 'MCPTool'))  #* %appdata%/MCPTool
        mcptool_lib_folder_path: str = os.path.abspath(os.path.join(mcptool_folder_path, 'lib'))  #* %appdata%/MCPTool/lib
        original_updater_path = os.path.join(mcptool_folder_path, 'MCPToolUpdater.exe')  #* %appdata%/MCPTool/MCPToolUpdater.exe
        updater_executable = os.path.join(appdata_path, 'MCPToolUpdater.exe')  #* %appdata%/MCPToolUpdater.exe

        # Command to run the updater with elevated privileges
        command = f'powershell -Command "Start-Process \'{updater_executable}\' -Verb runAs"'

        # Copy ./lib and *.dll python files to the %APPDATA% folder
        mcwrite(r'&8&l[&a&lINFO&8&l] &f&lCopying the lib folder and .dll files to the %APPDATA% folder...')

        if os.path.exists(lib_folder_path):
            shutil.rmtree(lib_folder_path)

        shutil.copytree(mcptool_lib_folder_path, lib_folder_path)  #* Copy the lib folder to %appdata%

        for file in os.listdir(mcptool_folder_path):  #* Copy the .dll files to %appdata%
            if file.endswith('.dll'):
                if 'python' in file:
                    if os.path.exists(os.path.join(appdata_path, file)):
                        os.remove(os.path.join(appdata_path, file))

                    shutil.copyfile(os.path.join(mcptool_folder_path, file), os.path.join(appdata_path, file))

        # Copy the updater to the %APPDATA% folder
        if os.path.exists(updater_executable):
            os.remove(updater_executable)

        shutil.copyfile(original_updater_path, updater_executable)

        # Run the updater
        mcwrite(r'&8&l[&a&lINFO&8&l] &f&lThe updater has been copied to the %APPDATA% folder. Running the updater...')
        subprocess.run(command, shell=True)
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
"""

    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            mcwrite(help_message)
            sys.exit(0)

        if sys.argv[1] == 'version':
            mcwrite(MCPTool.__version__)
            sys.exit(0)

    MCPTool().run()


if __name__ == '__main__':
    mcwrite('&8&l[&a&lINFO&8&l] &f&lChecking for updates...')
    UpdateTool().check_for_update()
    main()
