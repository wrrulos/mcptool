import threading
import time

from mccolors import mcwrite
from loguru import logger

from ..utilities.managers.language_utils import LanguageUtils as LM
from ..utilities.scrapers.minecraftservers import MinecraftServerScrapper
from ..utilities.input.get import GetInput


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'websearch'
        self.arguments: list = [i for i in LM.get(f'commands.{self.name}.arguments')]

    @logger.catch
    def execute(self, arguments: list, scrapper: MinecraftServerScrapper) -> None:
        """
        Method to execute the command

        Args:
            arguments (list): The arguments to execute the command
        """

        filter: tuple = GetInput(LM.get('commands.websearch.filterByData'), 'boolean').get_input()

        if filter[0]:
            filter_only_bot_join: tuple = GetInput(LM.get('commands.websearch.filterByOnlyBotCanJoin'), 'boolean').get_input()

            if filter_only_bot_join[0]:
                scrapper.filters['onlyBotCanJoin'] = True

            filter_description: tuple = GetInput(LM.get('commands.websearch.filterByDescription'), 'boolean').get_input()

            if filter_description[0]:
                scrapper.filters['filterByDescription'] = True
                scrapper.filters['description'] = GetInput(LM.get('commands.websearch.filterByDescriptionText'), 'string').get_input()[0]

            filter_online_players: tuple = GetInput(LM.get('commands.websearch.filterByOnlinePlayers'), 'boolean').get_input()

            if filter_online_players[0]:
                scrapper.filters['filterByOnlinePlayers'] = True
                scrapper.filters['onlinePlayers'] = GetInput(LM.get('commands.websearch.filterByOnlinePlayersText'), 'integer').get_input()[0]

            filter_protocol: tuple = GetInput(LM.get('commands.websearch.filterByProtocol'), 'boolean').get_input()

            if filter_protocol[0]:
                scrapper.filters['filterByProtocol'] = True
                scrapper.filters['protocol'] = GetInput(LM.get('commands.websearch.filterByProtocolText'), 'integer').get_input()[0]

        if filter[0]:
            mcwrite(LM.get('commands.websearch.filterDataShow')
                .replace('%onlyBotCanJoin%', '✔️' if scrapper.filters['onlyBotCanJoin'] else '❌')
                .replace('%description%', scrapper.filters['description'] if scrapper.filters['filterByDescription'] else '❌')
                .replace('%onlinePlayers%', str(scrapper.filters['onlinePlayers']) if scrapper.filters['filterByOnlinePlayers'] else '❌')
                .replace('%protocol%', str(scrapper.filters['protocol']) if scrapper.filters['filterByProtocol'] else '❌')
            )

        # It seems strange, but it's the only way I found to control thread closing the way I want.
        # If you're reading this and think you know better, let me know or make a pull request! :D
        scrapper_thread = threading.Thread(target=scrapper.get)
        scrapper_thread.start()

        try:
            while True:
                time.sleep(0.1)

        except KeyboardInterrupt:
            scrapper.stop()
            mcwrite(LM.get('commands.ctrlC'))
            scrapper_thread.join()
            scrapper.restore()
