import requests
import json
import time
import sys

from src.decoration.print_banner import print_banner
from src.managers.json_manager import JsonManager
from src.utilities.get_utilities import GetUtilities
from src.utilities.check_utilities import CheckUtilities


class MCPToolUpdater:
    @staticmethod
    def show_banner_update():
        """
        This method displays an update banner and checks for updates.

        It first determines the appropriate update banner to show based on the environment.
        Then, it displays the banner, checks for updates, and takes appropriate action based on the result.
        """
        
        try:
            # Get the update banner.
            update_banner_name = 'update' if not CheckUtilities.check_termux() else 'update_termux'

            # Show the banner.
            print_banner(
                update_banner_name,
                GetUtilities.get_translated_text(['banners', 'update', 'title']),
                GetUtilities.get_translated_text(['banners', 'update', 'checkingUpdates']),
                '', '', '', '', ''
            )

            time.sleep(1)

            # Check for updates.
            if MCPToolUpdater.check_update():
                # Show the banner with information about a new version.
                print_banner(
                    update_banner_name,
                    GetUtilities.get_translated_text(['banners', 'update', 'title']),
                    GetUtilities.get_translated_text(['banners', 'update', 'checkingUpdates']),
                    GetUtilities.get_translated_text(['banners', 'update', 'newVersion']),
                    '', '', '', ''
                )

                time.sleep(1)

                # Show the banner with a link to the new version.
                print_banner(
                    update_banner_name,
                    GetUtilities.get_translated_text(['banners', 'update', 'title']),
                    GetUtilities.get_translated_text(['banners', 'update', 'checkingUpdates']),
                    GetUtilities.get_translated_text(['banners', 'update', 'newVersion']),
                    GetUtilities.get_translated_text(['banners', 'update', 'url']),
                    '&a&lhttps://github.com/wrrulos/MCPTool', ''
                )

                time.sleep(10)
                sys.exit()

            else:
                # Show the banner indicating no updates were found.
                print_banner(
                    update_banner_name,
                    GetUtilities.get_translated_text(['banners', 'update', 'title']),
                    GetUtilities.get_translated_text(['banners', 'update', 'checkingUpdates']),
                    GetUtilities.get_translated_text(['banners', 'update', 'notFound']),
                    '', '', ''
                )

                time.sleep(2)

        except KeyboardInterrupt:
            return

    @staticmethod
    def check_update():
        """
        Check for updates by comparing the current and latest version numbers.

        This method retrieves the current version from JsonManager and the latest version
        from the MCPToolUpdater.get_latest_version() method. If these versions are different,
        it returns True, indicating that an update is available. Otherwise, it returns False.

        Returns:
            bool: True if an update is available, False otherwise.
        """
    
        # Get the current version from JsonManager.
        current_version = JsonManager.get('currentVersion')

        # Get the latest version from an external source (MCPToolUpdater.get_latest_version()).
        latest_version = MCPToolUpdater.get_latest_version()
        
        # Compare the current and latest versions.
        if current_version != latest_version:
            return True
        
        # No update available.
        return False

    @staticmethod
    def get_latest_version():
        """
        Retrieve the latest version of MCPTool from a remote configuration file.

        This method sends an HTTP GET request to a specific URL, which contains a JSON
        configuration file with version information. It then parses the JSON response
        and extracts the 'currentVersion' field, which represents the latest version.
        
        Returns:
            str: The latest version number as a string.
        """

        # Send an HTTP GET request to the remote configuration file URL.
        response = requests.get('https://raw.githubusercontent.com/wrrulos/MCPTool/main/config/config.json')

        # Parse the JSON response.
        js = json.loads(response.text)

        # Extract and return the 'currentVersion' field from the JSON.
        return js['currentVersion']