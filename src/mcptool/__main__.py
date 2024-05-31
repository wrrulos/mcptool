"""
mcptool.__main__

This module contains the main entry point for running the MCPTool.
"""

import sys
import subprocess

from mccolors import mcwrite
from mcptool import MCPTool


def main():
    """
    Main function to run the MCPTool
    """

    help_message: str = """
&f&lUsage: &a&lmcptool [command]

&f&lCommands:

&f&l  help &8- &f&lShow the help message
&f&l  version &8- &f&lShow the version of the tool
"""

    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            mcwrite(help_message)

        if sys.argv[1] == 'version':
            mcwrite(MCPTool.__version__)

        return

    MCPTool().run()
