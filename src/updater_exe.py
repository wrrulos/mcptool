import subprocess
import requests
import shutil
import os

from mccolors import mcwrite


class Updater:
    def __init__(self) -> None:
        self.download_url: str = 'https://github.com/wrrulos/MCPTool/releases/download/TEST/MCPTool-0.1.3-win64.msi'

    def windows_update(self) -> None:
        """
        Update the MCPTool
        """

        appdata_path: str = os.getenv('APPDATA')
        msi_file_name: str = 'MCPTool-win64.msi'
        msi_file_path: str = os.path.join(appdata_path, msi_file_name)

        if os.path.exists(f'{appdata_path}/{msi_file_name}'):
            mcwrite('&8&l[&a&lINFO&8&l] &f&lOld installer found. Removing it...')
            os.remove(f'{appdata_path}/{msi_file_name}')
            mcwrite('&8&l[&a&lINFO&8&l] &f&lOld installer removed successfully!')

        # Download the new version
        mcwrite(f'&8&l[&a&lINFO&8&l] &f&lDownloading the new version from &a&l{self.download_url}&f&l...')

        try:
            r: requests.Response = requests.get(self.download_url)

            with open(f'{appdata_path}/{msi_file_name}', 'wb') as f:
                f.write(r.content)

            mcwrite('&8&l[&a&lINFO&8&l] &f&lThe new version has been downloaded successfully!')

        except Exception as e:
            mcwrite(f'&8&l[&c&lERROR&8&l] &f&lError downloading the new version: &c&l{e}')
            return

        # Remove the data from the old version if it exists
        if os.path.exists(f'{appdata_path}/MCPToolData'):
            mcwrite('&8&l[&a&lINFO&8&l] &f&lRemoving the data from the old version...')
            shutil.rmtree(f'{appdata_path}/MCPToolData')
            mcwrite('&8&l[&a&lINFO&8&l] &f&lThe data from the old version has been removed successfully!')

        # Remove the old version if it exists
        if os.path.exists(f'{appdata_path}/MCPTool'):
            mcwrite('&8&l[&a&lINFO&8&l] &f&lRemoving the old version...')
            subprocess.run("""wmic product where "name='MCPTool'" call uninstall /nointeractive >nul 2>&1""", shell=True)
            mcwrite('&8&l[&a&lINFO&8&l] &f&lThe old version has been removed successfully!')

        # Install the new version
        mcwrite('&8&l[&a&lINFO&8&l] &f&lInstalling the new version...')

        if not os.path.exists(msi_file_path):
            mcwrite('&8&l[&c&lERROR&8&l] &f&lThe installer does not exist. Please try again.')
            input()
            return

        subprocess.run(f'start msiexec /i {msi_file_path}', shell=True)
        mcwrite('&8&l[&a&lINFO&8&l] &f&lMCPTool has been updated successfully!')
        input()
        subprocess.run(f'cd "{appdata_path}/MCPTool" && MCPTool.exe', shell=True)


if __name__ == '__main__':
    mcwrite('&8&l[&a&lINFO&8&l] &f&lUpdating the MCPTool...')

    if os.name == 'nt':
        Updater().windows_update()
