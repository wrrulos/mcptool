from utils.color.text_color import paint
from utils.managers.language_manager import language_manager
from utils.minecraft.server_data import GetDataFromMinecraftServer
from utils.minecraft.show_server import show_server
from utils.gets.get_spaces import get_spaces


def server_command(server, *args):
    """ 
    Gets information about the specified Minecraft 
    server and displays it on the screen.

    Args:
        server (str): The IP address or domain of the server.
    """

    try:
        server_data = GetDataFromMinecraftServer(server)
        data = server_data.get_information()

        if data is not None:
            show_server(data, False)
            return

        paint(f'\n{get_spaces()}{language_manager.language["commands"]["error"]}{language_manager.language["commands"]["invalidArguments"]["invalidServer"]}')

    except KeyboardInterrupt:
        paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
        return
