def minimessage_colors(text):
    """ 
    Replace the minecraft colored characters with 
    those of the MiniMessage library.
    
    Args:
        text (str): Text.

    Returns:
        str: New text.
    """

    codes = {
        '0': '<reset><black>',
        '1': '<reset><dark_blue>',
        '2': '<reset><dark_green>',
        '3': '<reset><dark_aqua>',
        '4': '<reset><dark_red>',
        '5': '<reset><dark_purple>',
        '6': '<reset><gold>',
        '7': '<reset><gray>',
        '8': '<reset><dark_gray>',
        '9': '<reset><blue>',
        'a': '<reset><green>',
        'b': '<reset><aqua>',
        'c': '<reset><red>',
        'd': '<reset><light_purple>',
        'e': '<reset><yellow>',
        'f': '<reset><white>',
        'k': '<obfuscated>',
        'l': '<bold>',
        'm': '<strikethrough>',
        'n': '<underlined>',
        'o': '<italic>',
        'r': '<reset>',
        'x': ''
    }

    for code in codes.items():
        text = text.replace(f'&{code[0]}', code[1]).replace(f'§{code[0]}', code[1])
        text = text.replace(f'&{code[0].upper()}', code[1]).replace(f'§{code[0].upper()}', code[1])
    
    text = text.replace('\n', '<newline>')
    return text


def minecraft_colors(text):
    """
    Replace MiniMessage colored characters with Minecraft color codes.

    Args:
        text (str): Text.

    Returns:
        str: New text.
    """

    codes = {
        '<reset><black>': '0',
        '<reset><dark_blue>': '1',
        '<reset><dark_green>': '2',
        '<reset><dark_aqua>': '3',
        '<reset><dark_red>': '4',
        '<reset><dark_purple>': '5',
        '<reset><gold>': '6',
        '<reset><gray>': '7',
        '<reset><dark_gray>': '8',
        '<reset><blue>': '9',
        '<reset><green>': 'a',
        '<reset><aqua>': 'b',
        '<reset><red>': 'c',
        '<reset><light_purple>': 'd',
        '<reset><yellow>': 'e',
        '<reset><white>': 'f',
        '<obfuscated>': 'k',
        '<bold>': 'l',
        '<strikethrough>': 'm',
        '<underlined>': 'n',
        '<italic>': 'o',
        '<reset>': 'r',
    }

    for code in codes.items():
        text = text.replace(code[0], f'&{code[1]}').replace(code[0], f'&{code[1]}')

    text = text.replace('<newline>', '\n')
    return text