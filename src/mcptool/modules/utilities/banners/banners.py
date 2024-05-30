from ..managers.settings_manager import SettingsManager as SM
from ..managers.language_manager import LanguageManager as LM

from ..constants import SPACES, OS_NAME, DISCORD_LINK, VERSION
from ..constants.update_available import UPDATE_AVAILABLE


class MCPToolBanners:
    BANNER_1: str = f'''
&f&l        dMMMMMMMMb  .aMMMb  dMMMMb&c&l dMMMMMMP .aMMMb  .aMMMb  dMP
&f&l       dMP"dMP"dMP dMP"VMP dMP.dMP&c&l   dMP   dMP"dMP dMP"dMP dMP
&f&l      dMP dMP dMP dMP     dMMMMP"&c&l   dMP   dMP dMP dMP dMP dMP
&f&l     dMP dMP dMP dMP.aMP dMP&c&l       dMP   dMP.aMP dMP.aMP dMP
&f&l    dMP dMP dMP  VMMMP" dMP&c&l       dMP    VMMMP"  VMMMP" dMMMMMP

{LM().get(['app', 'description']).replace('%version%', VERSION)}{LM().get(['app', 'newVersion']) if UPDATE_AVAILABLE  else ''}'''

    BANNER_2: str = f'''
&f&l    ███╗   ███╗ ██████╗██████╗ &c&l████████╗ ██████╗  ██████╗ ██╗
&f&l    ████╗ ████║██╔════╝██╔══██╗&c&l╚══██╔══╝██╔═══██╗██╔═══██╗██║
&f&l    ██╔████╔██║██║     ██████╔╝&c&l   ██║   ██║   ██║██║   ██║██║
&f&l    ██║╚██╔╝██║██║     ██╔═══╝ &c&l   ██║   ██║   ██║██║   ██║██║
&f&l    ██║ ╚═╝ ██║╚██████╗██║     &c&l   ██║   ╚██████╔╝╚██████╔╝███████╗
&f&l    ╚═╝     ╚═╝ ╚═════╝╚═╝     &c&l   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝

{LM().get(['app', 'description']).replace('%version%', VERSION)}{LM().get(['app', 'newVersion']) if UPDATE_AVAILABLE else ''}'''

    BANNER_3: str = f'''
&f&l    8888ba.88ba   a88888b.  888888ba  &c&ld888888P                   dP
&f&l    88  `8b  `8b d8'   `88  88    `8b &c&l   88                      88
&f&l    88   88   88 88        a88aaaa8P' &c&l   88    .d8888b. .d8888b. 88
&f&l    88   88   88 88         88        &c&l   88    88'  `88 88'  `88 88
&f&l    88   88   88 Y8.   .88  88        &c&l   88    88.  .88 88.  .88 88
&f&l    dP   dP   dP  Y88888P'  dP        &c&l   dP    `88888P' `88888P' dP

{LM().get(['app', 'description']).replace('%version%', VERSION)}{LM().get(['app', 'newVersion']) if UPDATE_AVAILABLE else ''}'''

    BANNER_4: str = f'''
&f&l    `7MMM.     ,MMF' .g8"""bgd `7MM"""Mq. &c&lMMP""MM""YMM              `7MM
&f&l      MMMb    dPMM .dP'     `M   MM   `MM.&c&lP'   MM   `7                MM
&f&l      M YM   ,M MM dM'       `   MM   ,M9 &c&l     MM  ,pW"Wq.   ,pW"Wq.  MM
&f&l      M  Mb  M' MM MM            MMmmdM9  &c&l     MM 6W'   `Wb 6W'   `Wb MM
&f&l      M  YM.P'  MM MM.           MM       &c&l     MM 8M     M8 8M     M8 MM
&f&l      M  `YM'   MM `Mb.     ,'   MM       &c&l     MM YA.   ,A9 YA.   ,A9 MM
&f&l    .JML. `'  .JMML. `"bmmmd'  .JMML.     &c&l   .JMML.`Ybmd9'   `Ybmd9'.JMML.

{LM().get(['app', 'description']).replace('%version%', VERSION)}{LM().get(['app', 'newVersion']) if UPDATE_AVAILABLE else ''}'''

    BANNERS: list = [BANNER_1, BANNER_2, BANNER_3, BANNER_4]


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
      &d► &f&luuid [username/UUID]                                             &d    ⣸⠁⢰⠃   ⠈⢣⡀              ⠈⣇
      &d► &f&lipinfo [ip]                                                      &d    ⡇ ⡾⡀    ⣀⣹⣆⡀             ⢹
      &d► &f&ldnslookup [domain]                                               &d   ⢸⠃⢀⣇⡈      &d⢀⡑⢄⡀⢀⡀         ⢸⡇
      &d► &f&lchecker [file]                                                   &d   ⢸ &f&l⢻⡟⡻⢶⡆   ⡼⠟⡳⢿⣦&d⡑⢄         ⢸⡇
      &d► &f&lresolver [domain]                                                &d   ⣸ &f&l⢸⠃⡇⢀⠇     ⡼  ⠈⣿&d⡗⠂       ⢸⠁
      &d► &f&lseeker [token/servers]                                           &d   ⡏ &f&l⣼ ⢳⠊      ⠱⣀⣀⠔&d⣸⠁       ⢠⡟
      &d► &f&lsubdomains [domain] [wordlist]                                   &d   ⡇&f&l⢀⡇           ⠠ &d⡇        ⢸⠃
      &d► &f&lscan [ip_address/ip_range] [port/port_range] [method             &d  ⢸⠃&f&l⠘⡇            &d⢸⠁  ⢀     ⣾
      &d► &f&llistening [ip:port]                                              &d  ⣸  &f&l⠹⡄  ⠈⠁       &d⡞   ⠸     ⡇
      &d► &f&lproxy [ip:port] [proxy_type]                                     &d  ⡏   &f&l⠙⣆       ⢀⣠⢶&d⡇  ⢰⡀     ⡇
      &d► &f&lfakeproxy [ip:port] [velocity_forwading_mode]                    &d ⢰⠇⡄    &f&l⢣⣀⣀⣀⡤⠴⡞⠉ &d⢸   ⣿⡇     ⣧
      &d► &f&lconnect [ip:port] [version] [username]                           &d ⣸ ⡇       &f&l   ⢹  &d⢸  ⢀⣿⠇   ⠁ ⢸
      &d► &f&lsendcmd [ip:port] [version] [username] [commands_file]           &d ⣿ ⡇    &f&l ⢀⡤⠤⠶⠶⠾⠤⠄&d⢸ ⡀⠸⣿⣀     ⠈⣇
      &d► &f&lrcon [ip:port] [password]                                        &d ⡇ ⡇    &f&l⡴⠋       &d⠸⡌⣵⡀⢳⡇      ⢹⡀
      &d► &f&lbrutercon [ip:port] [passwords_file]                             &d ⡇ ⠇   &f&l⡸⠁         &d⠙⠮⢧⣀⣻⢂      ⢧
      &d► &f&lbruteauth [ip:port] [version] [username] [passwords_file]        &d ⣇ ⢠   &f&l⠇            &d  ⠈⡎⣆     ⠘
      &d► &f&lkick [ip:port] [version] [username] [loop]                       &d ⢻ ⠈⠰ &f&l⢸             &d  ⠰⠘⢮⣧⡀
      &d► &f&lkickall [ip:port] [version] [loop]                               &d ⠸⡆  ⠇&f&l⣾             &d     ⠙⠳⣄⡀⡀
      &d► &f&llanguage [language]  (not available in beta)                     &d ⠸⡆  ⠇&f&l⣾             &d       ⠙⠳⢢
      &d► &f&lclear                                                            &d ⠸⡆  ⠇&f&l⣾             &d         ⠙⡀⢢'''

    BANNERS: list = [HELP_BANNER_2, HELP_BANNER_2]

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