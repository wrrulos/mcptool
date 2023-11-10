import os
import requests
import json


class LocalFileUtilities:
    url_and_paths = [
        ['./config/bruteforce_config.json', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/config/bruteforce_config.json'],
        ['./config/sendcmd_config.json', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/config/sendcmd_config.json'],
        ['./config/lang/cat.json', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/config/lang/cat.json'],
        ['./config/lang/de.json', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/config/lang/de.json'],
        ['./config/lang/en.json', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/config/lang/en.json'],
        ['./config/lang/es.json', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/config/lang/es.json'],
        ['./config/lang/fr.json', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/config/lang/fr.json'],
        ['./config/lang/pt.json', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/config/lang/pt.json'],
        ['./config/lang/sk.json', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/config/lang/sk.json'],
        ['./config/lang/tr.json', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/config/lang/tr.json'],
        ['./mcptool_files/banners/discord.txt', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/banners/discord.txt'],
        ['./mcptool_files/banners/help.txt', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/banners/help.txt'],
        ['./mcptool_files/banners/help_termux.txt', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/banners/help_termux.txt'],
        ['./mcptool_files/banners/menu.txt', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/banners/menu.txt'],
        ['./mcptool_files/banners/menu_termux.txt', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/banners/menu_termux.txt'],
        ['./mcptool_files/banners/pickaxe.txt', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/banners/pickaxe.txt'],
        ['./mcptool_files/banners/pickaxe_termux.txt', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/banners/pickaxe_termux.txt'],
        ['./mcptool_files/banners/presentation.txt', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/banners/presentation.txt'],
        ['./mcptool_files/banners/presentation_termux.txt', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/banners/presentation_termux.txt'],
        ['./mcptool_files/banners/proxy_update.txt', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/banners/proxy_update.txt'],
        ['./mcptool_files/banners/proxy_update_termux.txt', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/banners/proxy_update_termux.txt'],
        ['./mcptool_files/banners/starting_api.txt', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/banners/starting_api.txt'],
        ['./mcptool_files/banners/starting_api_termux.txt', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/banners/starting_api_termux.txt'],
        ['./mcptool_files/banners/update.txt', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/banners/update.txt'],
        ['./mcptool_files/banners/update_termux.txt', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/banners/update_termux.txt'],
        ['./mcptool_files/proxy/server-icon.png', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/server-icon.png'],
        ['./mcptool_files/proxy/settings/fakeproxy.config', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/settings/fakeproxy.config'],
        ['./mcptool_files/proxy/settings/variables.txt', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/settings/variables.txt'],
        ['./mcptool_files/proxy/settings/velocity.config', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/settings/velocity.config'],
        ['./mcptool_files/proxy/settings/waterfall.config', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/settings/waterfall.config'],
        ['./mcptool_files/proxy/jar/fakeproxy/Velocity.jar', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/jar/fakeproxy/Velocity.jar'],
        ['./mcptool_files/proxy/jar/fakeproxy/forwarding.secret', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/jar/fakeproxy/forwarding.secret'],
        ['./mcptool_files/proxy/jar/fakeproxy/velocity.toml', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/jar/fakeproxy/velocity.toml'],
        ['./mcptool_files/proxy/jar/fakeproxy/server-icon.png', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/jar/fakeproxy/server-icon.png'],
        ['./mcptool_files/proxy/jar/fakeproxy/plugins/RPoisoner-1.1-SNAPSHOT.jar', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/jar/fakeproxy/plugins/RPoisoner-1.1-SNAPSHOT.jar'],
        ['./mcptool_files/proxy/jar/velocity/Velocity.jar', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/jar/velocity/Velocity.jar'],
        ['./mcptool_files/proxy/jar/velocity/forwarding.secret', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/jar/velocity/forwarding.secret'],
        ['./mcptool_files/proxy/jar/velocity/velocity.toml', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/jar/velocity/velocity.toml'],
        ['./mcptool_files/proxy/jar/velocity/server-icon.png', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/jar/velocity/server-icon.png'],
        ['./mcptool_files/proxy/jar/velocity/plugins/MCPTool-1.1-SNAPSHOT.jar', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/jar/velocity/plugins/MCPTool-1.1-SNAPSHOT.jar'],
        ['./mcptool_files/proxy/jar/waterfall/waterfall.jar', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/jar/waterfall/waterfall.jar'],
        ['./mcptool_files/proxy/jar/waterfall/config.yml', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/jar/waterfall/config.yml'],
        ['./mcptool_files/proxy/jar/waterfall/server-icon.png', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/jar/waterfall/server-icon.png'],
        ['./mcptool_files/proxy/jar/waterfall/plugins/RBungeeExploit-1.0.jar', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/proxy/jar/waterfall/plugins/RBungeeExploit-1.0.jar'],
        ['./mcptool_files/scanner/old_qubo.jar', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/scan/old_qubo.jar'],
        ['./mcptool_files/scripts/checker.js', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/scripts/checker.js'],
        ['./mcptool_files/scripts/connect.js', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/scripts/connect.js'],
        ['./mcptool_files/scripts/kick.js', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/scripts/kick.js'],
        ['./mcptool_files/scripts/login.js', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/scripts/login.js'],
        ['./mcptool_files/scripts/pinlogin.js', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/scripts/pinlogin.js'],
        ['./mcptool_files/scripts/sendcmd.js', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/scripts/sendcmd.js'],
        ['./mcptool_files/scripts/utils.js', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/scripts/utils.js'],
        ['./mcptool_files/usernames.txt', 'https://raw.githubusercontent.com/wrrulos/MCPTool/main/mcptool_files/usernames.txt'],
    ]

    @staticmethod
    def check_local_files():
        """
        Checks if all local files are on the system.
        """

        directories_to_create = [
            './mcptool_files/',
            './config/',
            './config/lang/',
            './mcptool_files/banners/',
            './mcptool_files/presence/',
            './mcptool_files/proxy/',
            './mcptool_files/proxy/settings/',
            './mcptool_files/proxy/jar/fakeproxy/plugins/',
            './mcptool_files/proxy/jar/velocity/plugins/',
            './mcptool_files/proxy/jar/waterfall/plugins/',
            './mcptool_files/scanner/',
            './mcptool_files/scripts/',
        ]

        for directory in directories_to_create:
            if not os.path.exists(directory):
                os.makedirs(directory)

        if not os.path.exists(f'./config/config.json'):
            data = {
                "lang": "en",
                "api": "mcsrvstat.us",
                "discordPresence": True,
                "local_api_port": 55455,
                "shodanApiKey": "",
                "virusTotalApiKey": "0a1f92cc877fb00875cf0fa6e856db8009fb322fce4b507a9ef40e22d63b7fa4",
                "minecraftServerOptions": {
                    "checkServerLoginWithABot": True,
                    "proxy": False,
                    "proxyFileForTheBot": "./proxy.txt",
                    "nodeCommand": "node"
                },
                "scannerOptions": {
                    "nmapCommand": "nmap -p [PORTS] -n -T5 -Pn -vvv -sS [TARGET]",
                    "quboscannerCommand": "cd ./mcptool_files/scan && java -Dfile.encoding=UTF-8 -jar old_qubo.jar -range [TARGET] -ports [PORTS] -th 500 -ti 2000",
                    "masscanCommand": "masscan -p [PORTS] [TARGET]",
                    "showScanOutput": False
                },
                "proxyConfig": {
                    "convertDomainToIP": True,
                    "updateProxy": True,
                    "ngrokCommand": "ngrok",
                    "waterfallPort": "25570",
                    "waterfallCommand": "java -Xms512M -Xmx512M -jar WaterFall.jar >nul 2>&1",
                    "velocityPort": "25580",
                    "velocityCommand": "java -Xms512M -Xmx512M -jar Velocity.jar >nul 2>&1",
                    "fakeProxyPort": "33330",
                    "fakeProxyUpdateDelay": "2",
                    "fakeProxyCommandPrefix": ".",
                    "waterfallVersion": "https://api.papermc.io/v2/projects/waterfall/versions/1.20/builds/549/downloads/waterfall-1.20-549.jar",
                    "velocityVersion": "https://api.papermc.io/v2/projects/velocity/versions/3.2.0-SNAPSHOT/builds/294/downloads/velocity-3.2.0-SNAPSHOT-294.jar"
                },
                "logs": True,
                "currentVersion": "4.1.0"
            }

            with open(f'./config/config.json', 'w') as f:
                json.dump(data, f, indent=4)

        if not os.path.exists(f'./mcptool_files/presence/richPresence.command'):
            with open(f'./mcptool_files/presence/richPresence.command', 'w') as f:
                f.write('Help')

        if not os.path.exists(f'./mcptool_files/presence/richPresence.status'):
            with open(f'./mcptool_files/presence/richPresence.status', 'w') as f:
                f.write('True')

        for path, url in LocalFileUtilities.url_and_paths:
            if not os.path.exists(path):
                response = requests.get(url)

                if response.status_code == 200:
                    with open(path, 'wb') as f:
                        f.write(response.content)
