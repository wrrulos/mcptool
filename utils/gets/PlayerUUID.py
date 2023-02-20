#!/usr/bin/python3

import requests
import hashlib
import uuid

from json import JSONDecodeError

api = 'https://api.mojang.com/users/profiles/minecraft/'  # Mojang api


def player_uuid(username):
    """
    Gets the following data from the minecraft username:
    > Online UUID
    > Offline UUID

    :param username: Username
    :return: UUID's
    """

    try:
        r = requests.get(f'{api}{username}')
        r_json = r.json()

        online_uuid = r_json['id']
        online_uuid = f'{online_uuid[0:8]}-{online_uuid[8:12]}-{online_uuid[12:16]}-{online_uuid[16:21]}-{online_uuid[21:32]}'
        offline_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f'OfflinePlayer:{username}', 'utf-8')).digest()[:16], version=3))
        return online_uuid, offline_uuid

    except (JSONDecodeError, KeyError):
        offline_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f'OfflinePlayer:{username}', 'utf-8')).digest()[:16], version=3))
        return None, offline_uuid
