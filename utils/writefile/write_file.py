from datetime import datetime

date = datetime.now()


def WriteFile(file, clean_file, mode, *text):
    """
    Write the file with the specified text.
    Also cleans it if necessary.

    Args:
    file (str): File name
    clean_file (bool): Boolean value that decides whether to delete the contents of the file
    mode (str): How to open the file
    *text (str): Text to be written to the file
    """

    with open(file, mode=mode, encoding='utf8') as f:
        if clean_file:
            f.truncate(0)

        for i in text:
            f.write(str(i))
