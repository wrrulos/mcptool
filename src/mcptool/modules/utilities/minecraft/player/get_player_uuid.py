import requests
import hashlib
import uuid

from typing import Union
from json import JSONDecodeError
from loguru import logger


class PlayerUUIDFormat:
    def __init__(self, online_uuid: Union[str, None], offline_uuid: Union[str, None]) -> None:
        self.online_uuid: Union[str, None] = online_uuid
        self.offline_uuid: Union[str, None] = offline_uuid


class PlayerUUID:
    def __init__(self, username: str):
        self.username = username

    @logger.catch
    def get_uuid(self) -> PlayerUUIDFormat:
        """
        Method to get the online and offline UUID of the player

        Returns:
            PlayerUUIDFormat: The online and offline UUID of the player
        """

        try:
            response: requests.Response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{self.username}")
            response.raise_for_status()
            return PlayerUUIDFormat(response.json()['id'], self._get_offline_uuid())

        except (JSONDecodeError, KeyError, requests.exceptions.HTTPError):
            return PlayerUUIDFormat(None, self._get_offline_uuid())

        except requests.exceptions.RequestException:
            return PlayerUUIDFormat(None, self._get_offline_uuid())

    @logger.catch
    def get_uuid_color(self, original_uuid: str) -> str:
        """
        Method to get the online and offline UUID of the player in color format

        Returns:
            str: The online and offline UUID of the player in color format
        """

        player_uuid: PlayerUUIDFormat = self.get_uuid()

        if player_uuid.online_uuid is not None:
            if original_uuid == player_uuid.online_uuid:
                return f'&a&l'

        if original_uuid == player_uuid.offline_uuid:
            return f'&c&l'

        # If neither the online nor offline UUIDs match, consider it modified.
        return f'&5&l'

    @logger.catch
    def _get_offline_uuid(self) -> str:
        """
        Method to get the offline UUID of the player

        Returns:
            str: The offline UUID of the player
        """

        return str(uuid.UUID(bytes=hashlib.md5(bytes(f'OfflinePlayer:{self.username}', 'utf-8')).digest()[:16], version=3)).replace('-', '')
