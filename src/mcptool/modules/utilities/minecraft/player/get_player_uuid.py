import requests
import hashlib
import uuid

from typing import Union
from json import JSONDecodeError


class PlayerUUIDFormat:
    def __init__(self, online_uuid: Union[str, None], offline_uuid: Union[str, None]) -> None:
        self.online_uuid: Union[str, None] = online_uuid
        self.offline_uuid: Union[str, None] = offline_uuid


class PlayerUUID:
    def __init__(self, username: str):
        self.username = username

    def get_uuid(self) -> PlayerUUIDFormat:
        """
        Method to get the online and offline UUID of the player

        Returns:
            PlayerUUIDFormat: The online and offline UUID of the player
        """

        try:
            response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{self.username}")
            response.raise_for_status()
            return PlayerUUIDFormat(response.json()['id'], self._get_offline_uuid())
        
        except (JSONDecodeError, KeyError, requests.exceptions.HTTPError):
            return PlayerUUIDFormat(None, self._get_offline_uuid())

        except requests.exceptions.RequestException:
            return PlayerUUIDFormat(None, self._get_offline_uuid())
        
    def _get_offline_uuid(self) -> str:
        """
        Method to get the offline UUID of the player

        Returns:
            str: The offline UUID of the player
        """

        return str(uuid.UUID(bytes=hashlib.md5(bytes(f'OfflinePlayer:{self.username}', 'utf-8')).digest()[:16], version=3))
