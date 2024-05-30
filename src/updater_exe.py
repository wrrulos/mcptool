import subprocess
import requests
import shutil
import os


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
            print('Old installer found. Removing it...')
            os.remove(f'{appdata_path}/{msi_file_name}')
            print('Old installer removed successfully!')

        # Download the new version
        print(f'Downloading the new version from {self.download_url}...')

        try:
            r = requests.get(self.download_url)

            with open(f'{appdata_path}/{msi_file_name}', 'wb') as f:
                f.write(r.content)

            print('The new version has been downloaded successfully!')

        except Exception as e:
            print(f'Error downloading the new version: {e}')
            return

        # Remove the data from the old version if it exists
        if os.path.exists(f'{appdata_path}/MCPToolData'):
            print('Removing the data from the old version...')
            shutil.rmtree(f'{appdata_path}/MCPToolData')
            print('The data from the old version has been removed successfully!')

        # Remove the old version if it exists
        if os.path.exists(f'{appdata_path}/MCPTool'):
            print('Removing the old version...')
            subprocess.run("""wmic product where "name='MCPTool'" call uninstall /nointeractive""", shell=True)
            print('The old version has been removed successfully!')

        # Install the new version
        print('Installing the new version...')

        if not os.path.exists(msi_file_path):
            print('The installer does not exist. Please try again.')
            input()
            return

        print(f'start msiexec /i {msi_file_path}')
        subprocess.run(f'start msiexec /i {msi_file_path}', shell=True)
        print('The new version has been installed successfully! Press any key to start the MCPTool...')
        input()
        subprocess.run(f'cd "{appdata_path}/MCPTool" && MCPTool.exe', shell=True)


if __name__ == '__main__':
    print('Updating MCPTool...')

    if os.name == 'nt':
        Updater().windows_update()

    print('MCPTool has been updated successfully!')
