from ..managers.settings_manager import SettingsManager as SM
from ..managers.language_manager import LanguageManager as LM
from ..update.update_utilities import UpdateUtilities as UU
from ..constants import SPACES, OS_NAME, DISCORD_LINK


class MCPToolBanners:
    BANNER_1 = f'''
&f&l        dMMMMMMMMb  .aMMMb  dMMMMb&c&l dMMMMMMP .aMMMb  .aMMMb  dMP
&f&l       dMP"dMP"dMP dMP"VMP dMP.dMP&c&l   dMP   dMP"dMP dMP"dMP dMP
&f&l      dMP dMP dMP dMP     dMMMMP"&c&l   dMP   dMP dMP dMP dMP dMP
&f&l     dMP dMP dMP dMP.aMP dMP&c&l       dMP   dMP.aMP dMP.aMP dMP
&f&l    dMP dMP dMP  VMMMP" dMP&c&l       dMP    VMMMP"  VMMMP" dMMMMMP

{LM().get(['app', 'description']).replace('%version%', SM().get('version'))}{LM().get(['app', 'newVersion']) if UU.update_available() else ''}'''


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