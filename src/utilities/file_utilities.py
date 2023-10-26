from src.utilities.check_utilities import CheckUtilities


class FileUtilities:
    @staticmethod
    def write_file(file, text, mode='w', clean_file=False):
        """
        Write text to a file with the specified mode and optionally clean the file.

        Args:
            file (str): File name or path.
            text (str): Text to be written to the file.
            mode (str): File open mode (default is 'w' for write, use 'a' for append).
            clean_file (bool): If True, the file's contents will be cleared before writing.
        """

        try:
            with open(file, mode, encoding='utf8') as f:
                if clean_file:
                    f.truncate(0)  # Truncate (clear) the file contents before writing.

                f.write(text)  # Write the provided text to the file.

        except FileNotFoundError:
            pass

    @staticmethod
    def read_file(file, mode='read'):
        """
        Read the content of a file and return it as a string or list of lines.

        Args:
            file (str): The path to the file to be read.
            mode (str): The read mode, either 'read' (default) to read the file as a string, or 'readlines' to read as a list of lines.

        Returns:
            str or list: The content of the file in the specified format, or None if the file is not found.
        """
            
        try:
            with open(file, 'r+', encoding=CheckUtilities.check_file_encoding(file)) as f:
                if mode == 'read':
                    return f.read()
                
                elif mode == 'readlines':
                    return f.readlines()
            
        except FileNotFoundError:
            return None