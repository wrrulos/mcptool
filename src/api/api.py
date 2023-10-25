import asyncio

from flask import Flask, request, jsonify
from waitress import serve

from src.managers.json_manager import JsonManager
from src.utilities.get_utilities import GetUtilities
from src.api.minecraft_server_data import MinecraftServerData

app = Flask(__name__)


def convert_server_data(server_data):
    """
    Converts server data from a custom data structure to a dictionary format.

    Args:
        server_data (JavaServerData or BedrockServerData or None): The server data to be converted.

    Returns:
        dict or None: A dictionary containing server information or None if server_data is None.
    """

    if server_data is None:
        # Return None if server_data is None.
        return None

    if server_data.platform_type == 'Java':
        # Convert Java server data to a dictionary.
        response = {
            'platform_type': server_data.platform_type,
            'ip_port': server_data.ip_port,
            'motd': server_data.motd,
            'version': server_data.version,
            'protocol': server_data.protocol,
            'connected_players': server_data.connected_players,
            'max_player_limit': server_data.max_player_limit,
            'player_list': server_data.player_list,
            'default_player_list': server_data.default_player_list,
            'favicon': server_data.favicon,
            'mod_type': server_data.mod_type,
            'mod_list': server_data.mod_list,
            'latency': server_data.latency,
            'bot_response': server_data.bot_response
        }
            
    elif server_data.platform_type == 'Bedrock':
        # Convert Bedrock server data to a dictionary.
        response = {
            'platform_type': server_data.platform_type,
            'ip_port': server_data.ip_port,
            'motd': server_data.motd,
            'version': server_data.version,
            'protocol': server_data.protocol,
            'brand': server_data.brand,
            'connected_players': server_data.connected_players,
            'max_player_limit': server_data.max_player_limit,
            'map': server_data.map,
            'gamemode': server_data.gamemode,
            'latency': server_data.latency,
            'bot_response': server_data.bot_response
        }

    else:
        # Return None if the platform type is unknown.
        response = None

    return response


@app.route('/api/minecraft_server_data', methods=['GET'])
def get_minecraft_server_data():
    """
    Retrieve and return Minecraft server data based on the provided server address.

    This function uses the Flask `request` object to get the server address as a query parameter.
    It then asynchronously fetches Minecraft server data using `asyncio.run` and the `MinecraftServerData.get_server_data`
    method. The retrieved data is then formatted based on the platform type (Java or Bedrock) and returned as JSON.

    Returns:
        JSON response: A JSON object containing Minecraft server data or an error message.
    """
    
    server_address = request.args.get('server_address')
    bot = request.args.get('bot') == 'True'
    clean_data = request.args.get('clean_data') == 'True'
    
    if server_address:
        # Asynchronously retrieve Minecraft server data.
        minecraft_server_data = asyncio.run(MinecraftServerData.get_server_data(server_address, bot, clean_data))

        if minecraft_server_data is not None:
            # Format and return the server data as JSON.
            response = convert_server_data(minecraft_server_data)
            return jsonify(response)

        else:        
            # Return an error response for invalid server address.
            return jsonify({'Error': f'{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidServer"])}'}), 400

    else:
        # Return an error response for missing server address argument.
        return jsonify({'Error': f'{GetUtilities.get_translated_text(["commands", "server", "missingArgument1"])}'}), 400


def run_flask_app():
    """
    Run a Flask web application to serve the API.

    This function runs the Flask web application, serving the API on the specified host and port 
    as configured in the `JsonManager`. It uses the `serve` function from the `waitress` library 
    to serve the app.
    """

    serve(app, host='0.0.0.0', port=JsonManager.get('local_api_port'))

   