"""
Executable file for the MCPTool

This file is used to run the MCPTool from the command line
"""

import sys

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
&f&l  update &8- &f&lUpdate the tool
"""

    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            mcwrite(help_message)

        if sys.argv[1] == 'version':
            mcwrite(MCPTool.__version__)

        if sys.argv[1] == 'update':
            mcwrite('Updating the tool...')
            mcwrite('The tool is already updated!')

        sys.exit(0)

    MCPTool().run()


if __name__ == '__main__':
    main()