from ..managers.settings_manager import SettingsManager as SM
from ..managers.language_manager import LanguageManager as LM
from ..constants import SPACES, OS_NAME

class MCPToolBanners:
    BANNER_1 = f'''
&f&l        dMMMMMMMMb  .aMMMb  dMMMMb&c&l dMMMMMMP .aMMMb  .aMMMb  dMP 
&f&l       dMP"dMP"dMP dMP"VMP dMP.dMP&c&l   dMP   dMP"dMP dMP"dMP dMP  
&f&l      dMP dMP dMP dMP     dMMMMP"&c&l   dMP   dMP dMP dMP dMP dMP   
&f&l     dMP dMP dMP dMP.aMP dMP&c&l       dMP   dMP.aMP dMP.aMP dMP    
&f&l    dMP dMP dMP  VMMMP" dMP&c&l       dMP    VMMMP"  VMMMP" dMMMMMP

{LM().get(['app', 'description'])}{LM().get(['app', 'version']) if True else ''}
'''


class InputBanners:
    INPUT_1 = f'\n{" " * SPACES}&8&l{OS_NAME}@mcptool ~\n{" " * SPACES}&c&l↪ &f&l'
