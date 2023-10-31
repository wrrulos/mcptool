from src.commands.clear import clear_command
from src.commands.discord import discord_command
from src.commands.language import language_command
from src.commands.help import help_command
from src.commands.server import server_command
from src.commands.uuid import uuid_command
from src.commands.ipinfo import ipinfo_command
from src.commands.dnsloookup import dnslookup
from src.commands.shodan import shodan_command
from src.commands.websearch import websearch_command
from src.commands.subdomains import subdomains_command
from src.commands.scan import scan_command
from src.commands.listening import listening_command
from src.commands.playerlogs import playerlogs_command
from src.commands.resolver import resolver_command
from src.commands.fakeproxy import fakeproxy_command
from src.commands.login import login_command
from src.commands.pinlogin import pinlogin_command
from src.commands.sendcmd import sendcmd_command
from src.commands.kick import kick_command
from src.commands.kickall import kickall_command
from src.commands.rconbrute import rconbrute
from src.commands.checker import checker_command
from src.commands.waterfall import waterfall_command
from src.commands.velocity import velocity_command
from src.commands.connect import connect_command
from src.commands.rcon import rcon_command

commands = {
    **dict.fromkeys(['cls', 'clear'], clear_command),
    **dict.fromkeys(['dc', 'discord'], discord_command),
    **dict.fromkeys(['lang', 'language'], language_command),
    **dict.fromkeys(['00', 'help'], help_command),
    **dict.fromkeys(['01', 'server'], server_command),
    **dict.fromkeys(['02', 'uuid'], uuid_command),
    **dict.fromkeys(['03', 'ipinfo'], ipinfo_command),
    **dict.fromkeys(['04', 'dnslookup'], dnslookup),
    **dict.fromkeys(['05', 'shodan'], shodan_command),
    **dict.fromkeys(['06', 'websearch'], websearch_command),
    **dict.fromkeys(['07', 'subdomains'], subdomains_command),
    **dict.fromkeys(['08', 'scan'], scan_command),
    **dict.fromkeys({'09', 'listening'}, listening_command),
    **dict.fromkeys(['10', 'playerlogs'], playerlogs_command),
    **dict.fromkeys(['10', 'resolver'], resolver_command),
    **dict.fromkeys(['12', 'fakeproxy'], fakeproxy_command),
    **dict.fromkeys(['13', 'login'], login_command),
    **dict.fromkeys(['14', 'pinlogin'], pinlogin_command),
    **dict.fromkeys(['15', 'sendcmd'], sendcmd_command),
    **dict.fromkeys(['16', 'kick'], kick_command),
    **dict.fromkeys(['17', 'kickall'], kickall_command),
    **dict.fromkeys(['18', 'rconbrute'], rconbrute),
    **dict.fromkeys(['19', 'checker'], checker_command),
    **dict.fromkeys(['20', 'waterfall'], waterfall_command),
    **dict.fromkeys(['21', 'velocity'], velocity_command),
    **dict.fromkeys(['22', 'connect'], connect_command),
    **dict.fromkeys(['23', 'rcon'], rcon_command),
}
