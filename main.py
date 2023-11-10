import subprocess
import time
import os
import sys

from src.startup import Startup
from src.decoration.print_banner import print_banner
from src.utilities.check_utilities import CheckUtilities
from src.utilities.local_file_utilities import LocalFileUtilities


if __name__ == '__main__':
    try:
        # Check local files.
        print('Downloading files necessary to use MCPTool...')
        LocalFileUtilities.check_local_files()

        # Determine the banner name based on the configuration and environment.
        pickaxe_banner_name = f'pickaxe' if not CheckUtilities.check_termux() else 'pickaxe_termux'

        # If the operating system is Windows, set the console window title.
        if os.name == 'nt':
            subprocess.run('title MCPTool / By @wrrulos', shell=True)

        # Display the pickaxe banner.
        print_banner(pickaxe_banner_name)
        time.sleep(1)

        # Run the main startup routine, passing the API process.
        Startup.run()

    except KeyboardInterrupt:
        sys.exit()
