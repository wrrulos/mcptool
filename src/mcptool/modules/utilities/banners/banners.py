from ..managers.settings_manager import SettingsManager as SM
from ..managers.language_manager import LanguageManager as LM
from ..update.update_utilities import UpdateUtilities as UU
from ..constants import SPACES, OS_NAME, DISCORD_LINK


class MCPToolBanners:
    BANNER_1: str = f'''
&f&l        dMMMMMMMMb  .aMMMb  dMMMMb&c&l dMMMMMMP .aMMMb  .aMMMb  dMP
&f&l       dMP"dMP"dMP dMP"VMP dMP.dMP&c&l   dMP   dMP"dMP dMP"dMP dMP
&f&l      dMP dMP dMP dMP     dMMMMP"&c&l   dMP   dMP dMP dMP dMP dMP
&f&l     dMP dMP dMP dMP.aMP dMP&c&l       dMP   dMP.aMP dMP.aMP dMP
&f&l    dMP dMP dMP  VMMMP" dMP&c&l       dMP    VMMMP"  VMMMP" dMMMMMP

{LM().get(['app', 'description']).replace('%version%', SM().get('version'))}{LM().get(['app', 'newVersion']) if UU.update_available() else ''}'''

    BANNER_2: str = f'''
&f&l    ███╗   ███╗ ██████╗██████╗ &c&l████████╗ ██████╗  ██████╗ ██╗
&f&l    ████╗ ████║██╔════╝██╔══██╗&c&l╚══██╔══╝██╔═══██╗██╔═══██╗██║
&f&l    ██╔████╔██║██║     ██████╔╝&c&l   ██║   ██║   ██║██║   ██║██║
&f&l    ██║╚██╔╝██║██║     ██╔═══╝ &c&l   ██║   ██║   ██║██║   ██║██║
&f&l    ██║ ╚═╝ ██║╚██████╗██║     &c&l   ██║   ╚██████╔╝╚██████╔╝███████╗
&f&l    ╚═╝     ╚═╝ ╚═════╝╚═╝     &c&l   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝

{LM().get(['app', 'description']).replace('%version%', SM().get('version'))}{LM().get(['app', 'newVersion']) if UU.update_available() else ''}'''

    BANNER_3: str = f'''
&f&l    8888ba.88ba   a88888b.  888888ba  &c&ld888888P                   dP
&f&l    88  `8b  `8b d8'   `88  88    `8b &c&l   88                      88
&f&l    88   88   88 88        a88aaaa8P' &c&l   88    .d8888b. .d8888b. 88
&f&l    88   88   88 88         88        &c&l   88    88'  `88 88'  `88 88
&f&l    88   88   88 Y8.   .88  88        &c&l   88    88.  .88 88.  .88 88
&f&l    dP   dP   dP  Y88888P'  dP        &c&l   dP    `88888P' `88888P' dP

{LM().get(['app', 'description']).replace('%version%', SM().get('version'))}{LM().get(['app', 'newVersion']) if UU.update_available() else ''}'''

    BANNER_4: str = f'''
&f&l    `7MMM.     ,MMF' .g8"""bgd `7MM"""Mq. &c&lMMP""MM""YMM              `7MM
&f&l      MMMb    dPMM .dP'     `M   MM   `MM.&c&lP'   MM   `7                MM
&f&l      M YM   ,M MM dM'       `   MM   ,M9 &c&l     MM  ,pW"Wq.   ,pW"Wq.  MM
&f&l      M  Mb  M' MM MM            MMmmdM9  &c&l     MM 6W'   `Wb 6W'   `Wb MM
&f&l      M  YM.P'  MM MM.           MM       &c&l     MM 8M     M8 8M     M8 MM
&f&l      M  `YM'   MM `Mb.     ,'   MM       &c&l     MM YA.   ,A9 YA.   ,A9 MM
&f&l    .JML. `'  .JMML. `"bmmmd'  .JMML.     &c&l   .JMML.`Ybmd9'   `Ybmd9'.JMML.

{LM().get(['app', 'description']).replace('%version%', SM().get('version'))}{LM().get(['app', 'newVersion']) if UU.update_available() else ''}'''

    BANNER_5: str = rf'''
&c&l                         __
&c&l           ---_ ...... _/_ -
&c&l          /  .      ./ .'*\ \
&c&l          : '         /__-'   \.
&c&l         /                      )     &c&l___  ________ ______ _____ _____  _____ _
&c&l       _/                  >   .'     &c&l|  \/  /  __ \| ___ \_   _|  _  ||  _  | |
&c&l     /   '   .       _.-" /  .'       &c&l| |\/| | |    |  __/  | | | | | || | | | |
&f&l     \           __/"     /.'         &f&l| |  | | \__/\| |     | | \ \_/ /\ \_/ / |____
&f&l       \ '--  .-" /     //'           &f&l\_|  |_/\____/\_|     \_/  \___/  \___/\_____/
&f&l        \|  \ | /     //
&f&l             \:     //
&f&l          `\/     //              {LM().get(['app', 'description']).replace('%version%', SM().get('version'))}{LM().get(['app', 'newVersion']) if UU.update_available() else ''}
&f&l           \__`\/ /
&f&l               \_|
'''

    BANNERS: list = [BANNER_1, BANNER_2, BANNER_3, BANNER_4, BANNER_5]


class InputBanners:
    INPUT_1 = f'\n{SPACES}&8&l{OS_NAME}@mcptool ~\n{SPACES} &c&l↪ &f&l'


class HelpBanners:
    HELP_BANNER_1 = f'''
                                                                     &b⢀⣀⣀⣀⣀⣀⣀
    &f&l• &b&lInformation commands                                         &b⢀⣀⡿⠿⠿⠿⠿⠿⠿⢿⣀⣀⣀&f&l⣀⣀⡀
     &c&l↪ &f&lserver uuid ipinfo                                          &b⠸⠿⣇⣀⣀⣀⣀⣀⣀⣸⠿⢿⣿&f&l⣿⣿⡇
                                                                     &b⠻⠿⠿⠿⠿⠿⣿⣿⣀⡸⠿⢿⣿⡇
                                                                     &f&l    ⣤⣤⣿⣿⣿&b⣧⣤⡼⠿⢧⣤⡀
                                                                      &f&l⣤⣤⣿⣿⣿⣿⠛&b⢻⣿⡇ ⢸⣿⡇
                                                                    &f&l⣤⣤⣿⣿⣿⣿⠛⠛ &b⢸⣿⡇ ⢸⣿⡇
                                                                  &f&l⢠⣤⣿⣿⣿⣿⠛⠛   &b⢸⣿⡇ ⢸⣿⡇
                                                                &f&l⢰⣶⣾⣿⣿⣿⠛⠛     &b⠈⠛⢳⣶⡞⠛⠁
                                                              &f&l⢰⣶⣾⣿⣿⣿⡏⠉       &b  ⠈⠉⠁
                                                            &f&l⢰⣶⡎⠉⢹⣿⡏⠉⠁
                                                            &f&l⢸⣿⣷⣶⡎⠉⠁
                                                             &f&l⠉⠉⠉⠁'''

    HELP_BANNER_2 = f'''
                                                                             &d      ⣠⠤⠖⠚⢉⣩⣭⡭⠛⠓⠲⠦⣄⡀
    &c• &f&lCommands:                                                          &d       ⢀⡴⠋⠁  ⠊         ⠉⠳⢦⡀
                                                                         &d     ⢀⡴⠃⢀⡴⢳               ⠙⣆
      &d► &f&lserver [ip:port/domain]                                          &d     ⡾⠁⣠⠋ ⠈⢧               ⠈⢧
      &d► &f&lplayer [username]                                                &d    ⣸⠁⢰⠃   ⠈⢣⡀              ⠈⣇
      &d► &f&lipinfo [ip]                                                      &d    ⡇ ⡾⡀    ⣀⣹⣆⡀             ⢹
      &d► &f&lreverseip [ip]                                                   &d   ⢸⠃⢀⣇⡈      &d⢀⡑⢄⡀⢀⡀         ⢸⡇
      &d► &f&ldnslookup [domain]                                               &d   ⢸ &f&l⢻⡟⡻⢶⡆   ⡼⠟⡳⢿⣦&d⡑⢄         ⢸⡇
      &d► &f&lsearch [data]                                                    &d   ⣸ &f&l⢸⠃⡇⢀⠇     ⡼  ⠈⣿&d⡗⠂       ⢸⠁
      &d► &f&lwebsearch [tag] [bot] <proxy>                                    &d   ⡏ &f&l⣼ ⢳⠊      ⠱⣀⣀⠔&d⣸⠁       ⢠⡟
      &d► &f&laternos [pages] [bot] <proxy>                                    &d   ⡇&f&l⢀⡇           ⠠ &d⡇        ⢸⠃
      &d► &f&lscan [ip] [ports] [method] [bot] <proxy>                         &d  ⢸⠃&f&l⠘⡇            &d⢸⠁  ⢀     ⣾
      &d► &f&lchecker [file] [bot] <proxy>                                     &d  ⣸  &f&l⠹⡄  ⠈⠁       &d⡞   ⠸     ⡇
      &d► &f&llistening [ip:port/domain]                                       &d  ⡏   &f&l⠙⣆       ⢀⣠⢶&d⡇  ⢰⡀     ⡇
      &d► &f&lplayerlogs [ip:port/domain]                                      &d ⢰⠇⡄    &f&l⢣⣀⣀⣀⡤⠴⡞⠉ &d⢸   ⣿⡇     ⣧
      &d► &f&lbungee [ip:port/domain]                                          &d ⣸ ⡇       &f&l   ⢹  &d⢸  ⢀⣿⠇   ⠁ ⢸
      &d► &f&lvelocity [ip:port/domain] [forwarding-mode]                      &d ⣿ ⡇    &f&l ⢀⡤⠤⠶⠶⠾⠤⠄&d⢸ ⡀⠸⣿⣀     ⠈⣇
      &d► &f&lfakeproxy [ip:port/domain] [forwarding-mode]                     &d ⡇ ⡇    &f&l⡴⠋       &d⠸⡌⣵⡀⢳⡇      ⢹⡀
      &d► &f&lconnect [ip:port] [username] [version] <proxy>                   &d ⡇ ⠇   &f&l⡸⠁         &d⠙⠮⢧⣀⣻⢂      ⢧
      &d► &f&lrconnect [ip:rconPort] [passwordFile]                            &d ⣇ ⢠   &f&l⠇            &d  ⠈⡎⣆     ⠘
      &d► &f&lrcon [ip:rconPort] [passwordFile] <delay>                        &d ⢻ ⠈⠰ &f&l⢸             &d  ⠰⠘⢮⣧⡀
      &d► &f&lauthme [ip:port] [username] [version] [passwordFile] <proxy>     &d ⠸⡆  ⠇&f&l⣾             &d     ⠙⠳⣄⡀⡀
      &d► &f&lkick [ip:port] [username] [version] [loop] <proxy>               &d ⠸⡆  ⠇&f&l⣾             &d       ⠙⠳⢢
      &d► &f&lkickall [ip:port] [version] [loop] <proxy>                       &d ⠸⡆  ⠇&f&l⣾             &d        ⠙⣄⢢
      &d► &f&lsendcmd [ip:port] [username] [version] [file] [loop] <proxy>     &d ⠸⡆  ⠇&f&l⣾             &d         ⠙⡀⢢
      &d► &f&llanguage [language]                                              &d ⠸⡆  ⠇&f&l⣾             &d         ⠙⡀⢢'''

    BANNERS: list = [HELP_BANNER_1, HELP_BANNER_2]

class DiscordBanners:
    DISCORD_BANNER_1 = f'''
    &b                       &f&l• &5wRRulos Server
    &b                       &b&l{DISCORD_LINK}
    &b       ⢠⣴⣾⣵⣶⣶⣾⣿⣦⡄
    &b      ⢀⣾⣿⣿⢿⣿⣿⣿⣿⣿⣿⡄        &f&l- Enter my discord server
    &b      ⢸⣿⣿⣧⣀⣼⣿⣄⣠⣿⣿⣿        &f&l- to stay up to date with my projects
    &b      ⠘⠻⢷⡯⠛⠛⠛⠛⢫⣿⠟⠛        &f&l- and you can also talk to me!
    &b
    &b                       &c➥ &f&lWeb: &bwww.mcptool.net'''