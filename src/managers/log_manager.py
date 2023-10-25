import datetime
import os
import re

from src.utilities.file_utilities import FileUtilities
from src.decoration.mccolor import mcremove

class LogManager:
    save_bedrock_server = '''
[IP] [1] ([0])
[MOTD] [2]
[Version] [3]
[Protocol] [4]
[Players] [6]/[7]
[Brand] [5]
[Map] [8]
[Gamemode] [9]
[Ping] [10]
[BOT] [11]
'''

    save_java_server = '''
[IP] [1] ([0])
[MOTD] [2]
[Version] [3]
[Protocol] [4]
[Players] [5]/[6]
[Names] [8]
[Mods Type] [10]
[Mods] [11]
[Ping] [12]
[Bot] [13]
'''

    @staticmethod
    def create_log_file(log_name):
        """
        Create a log file with a timestamp and return its path.

        Args:
            log_name (str): Name of the log file.

        Returns:
            str: Path to the created log file.
        """

        timestamp = LogManager.get_timestamp()
        start_message = 'MCPTool Logs\nwww.github.com/wrrulos/mcptool\n\n'

        if log_name in ['scan', 'shodan', 'websearch', 'listening', 'checker', 'fakeproxy']:
            log_folder = f'./logs/{log_name}/'
            log_file = f'{log_folder}{log_name}_{timestamp}.log'

        else:
            log_folder = f'./logs/'
            log_file = f'{log_folder}{log_name}.log'

        if not os.path.exists(log_file):
            os.makedirs(log_folder, exist_ok=True)
            FileUtilities.write_file(log_file, start_message, 'w', True)
            
        return log_file

    @staticmethod
    def write_log(log_file, log_name, data):
        """
        Write data to a log file.

        Args:
            log_file (str): Path to the log file.
            log_name (str): Name of the log file.
            data (str): Data to be written to the log.
        """

        new_data = LogManager.get_new_data(log_name, data)
        FileUtilities.write_file(log_file, new_data, 'a')

    @staticmethod
    def get_new_data(log_name, data):
        """
        Generate new log data based on log type and provided data.

        Args:
            log_name (str): Name of the log.
            data (str): Data to be processed.

        Returns:
            str: Processed log data.
        """

        if log_name in ['server', 'shodan', 'scan', 'websearch', 'checker']:
            if data[0] == 'Java':
                new_data = LogManager.replace_data_values(LogManager.save_java_server, data)
            else:
                new_data = LogManager.replace_data_values(LogManager.save_bedrock_server, data)

        else:
            new_data = data

        return new_data

    @staticmethod
    def replace_data_values(text, data):
        """
        Replace placeholders in a text template with actual data values.

        Args:
            text (str): Text template with placeholders.
            data (list): List of data values to replace placeholders.

        Returns:
            str: Text with placeholders replaced by data values.
        """

        for num, i in enumerate(data):
            if i is None:
                i = '❌'

            clean_data = LogManager._clean_data(i)
            text = text.replace(f'[{str(num)}]', str(clean_data))

        return text

    @staticmethod
    def _clean_data(data):
        """
        Clean and format data by removing unwanted characters.

        Args:
            data (str): Data to be cleaned.

        Returns:
            str: Cleaned and formatted data.
        """
        
        data = mcremove(str(data))
        data = data.replace('\n', '')
        data = re.sub(' +', ' ', data)
        return data 

    @staticmethod
    def get_timestamp():
        """
        Get the current timestamp in a specific format.

        Returns:
            str: Current timestamp in 'YYYY-MM-DD_HH-MM-SS' format.
        """
        return datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
