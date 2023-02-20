#!/usr/bin/python3

import json


def check_minecraft_version(version):
    """
    Check if the version entered by the user is 
    compatible with Mineflayer.

    :param version: Minecraft Version
    :return: True if the version is compatible, False if it is not.
    """

    with open('utils/minecraftserver/Versions.json', 'r') as f:
        js = json.loads(f.read())

    if version in js['VERSIONS']:
        return True

    return False