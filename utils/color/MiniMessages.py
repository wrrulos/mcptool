def minimessage_colors(text):
    """ 
    Replace the minecraft colored characters with 
    those of the MiniMessage library.
    
    Parameters:
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
        text = text.replace(f'&{code[0]}', code[1]
                  ).replace(f'§{code[0]}', code[1])
    
    text = text.replace('\n', '<newline>')
    return text
