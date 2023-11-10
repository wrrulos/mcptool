from src.decoration.paint import paint
from src.utilities.get_utilities import GetUtilities


def show_server(server_data):
    if server_data is None:
        return
    
    paint(f'\n{GetUtilities.get_spaces()}&4[&cPlat&f&lform&4] &f&l{server_data["platform_type"]}')
    paint(f'{GetUtilities.get_spaces()}&4[&cI&f&lP&4] &f&l{server_data["ip_port"]}')
    paint(f'{GetUtilities.get_spaces()}&4[&cMo&f&ltd&4] &f&l{server_data["motd"]}')
    paint(f'{GetUtilities.get_spaces()}&4[&cVer&f&lsion&4] &f&l{server_data["version"]}')
    paint(f'{GetUtilities.get_spaces()}&4[&cProto&f&lcol&4] &f&l{server_data["protocol"]}')
    paint(f'{GetUtilities.get_spaces()}&4[&cPlay&f&lers&4] &f&l{server_data["connected_players"]}&8&r/&f&l{server_data["max_player_limit"]}')
    
    if server_data['platform_type'] == 'Java':
        _show_java_server(server_data)

    else:
        _show_bedrock_server(server_data)
    
    if server_data['latency'] is not None:
        paint(f'{GetUtilities.get_spaces()}&4[&cPi&f&lng&4] &f&l{GetUtilities.get_ms_color(server_data["latency"])}ms')
    
    if server_data['bot_response'] is not None:
        paint(f'{GetUtilities.get_spaces()}&4[&cBO&f&lT&4] {server_data["bot_response"]}')

    else:
        paint(f'{GetUtilities.get_spaces()}&4[&cBO&f&lT&4] ❌')

def _show_java_server(server_data):
    if server_data['player_list'] is not None:
        paint(f'{GetUtilities.get_spaces()}&4[&cNa&f&lmes&4] &f&l{server_data["player_list"]}')
    
    if server_data["mod_type"] is not None:
        paint(f'{GetUtilities.get_spaces()}&4[&cMods&f&l Type&4] &f&l{server_data["mod_type"]}')
        paint(f'{GetUtilities.get_spaces()}&4[&cMo&f&lds&4] &f&l{len(server_data["mod_list"])}')

    else:
        paint(f'{GetUtilities.get_spaces()}&4[&cMo&f&lds&4] &f&l❌')

def _show_bedrock_server(server_data):
    if server_data['brand'] is not None:
        paint(f'{GetUtilities.get_spaces()}&4[&cBra&f&lnd&4] &f&l{server_data["brand"]}')

    else:
        paint(f'{GetUtilities.get_spaces()}&4[&cBra&f&lnd&4] &f&l❌')
    
    if server_data['map'] is not None:
        paint(f'{GetUtilities.get_spaces()}&4[&cMa&f&lp&4] &f&l{server_data["map"]}')

    else:
        paint(f'{GetUtilities.get_spaces()}&4[&cMa&f&lp&4] &f&l❌')
    
    if server_data['gamemode'] is not None:
        paint(f'{GetUtilities.get_spaces()}&4[&cGame&f&lmode&4] &f&l{server_data["gamemode"]}')

    else:
        paint(f'{GetUtilities.get_spaces()}&4[&cGame&f&lmode&4] &f&l❌')