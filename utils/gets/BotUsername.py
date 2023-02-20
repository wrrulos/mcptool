#!/usr/bin/python3

import random

from utils.checks.Encoding import check_encoding


def get_bot_username(file='utils/otherfiles/usernames.txt'):
    """
    This function opens the usernames.txt file to select a 
    random name for the mineflayer bot

    :return: Bot Username
    """

    with open(file, 'r', encoding=check_encoding(file)) as f:
        usernames = f.readlines()

    username = random.choice(usernames)
    username = username.replace('\n', '')
    return username