#!/usr/bin/env python3

import sys
import subprocess

from mcptool import MCPTool
from mccolors import mcwrite


def main():
    """
    Main function to run the MCPTool
    """

    HELP_MESSAGE: str = """
&f&lUsage: &a&lmcptool [command]

&f&lCommands:

&f&l  help &8- &f&lShow the help message
&f&l  version &8- &f&lShow the version of the tool
&f&l  update &8- &f&lUpdate the tool
"""

    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            mcwrite(HELP_MESSAGE)
    
        if sys.argv[1] == 'version':
            mcwrite(MCPTool.__version__)

        if sys.argv[1] == 'update':
            subprocess.run('pip install -e . --upgrade', shell=True)
        
        sys.exit(0)

    MCPTool().run()
