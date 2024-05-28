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
                                                              &f&l⢰⣶⣾⣿⣿⣿⡏⠉       &b  ⠈⠉⠁⠀
                                                            &f&l⢰⣶⡎⠉⢹⣿⡏⠉⠁
                                                            &f&l⢸⣿⣷⣶⡎⠉⠁
                                                             &f&l⠉⠉⠉⠁'''


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