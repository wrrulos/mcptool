# Module created for my tool MCPTool @wrrulos

import os
import socket
import time
import requests

from colorama import Fore, init
from mcstatus import MinecraftServer

script_verison = 14
version_link = "https://raw.githubusercontent.com/wrrulos/MCPTool/main/config/data/version"

init()

# MOTDS CONFIG

motd_1 = """
# This is the list of message shown when hovering over the player count.
# Only works on Bukkit (Requires ProtocolLib)
sample:
  enabled: false

  # Placeholders: %onlineplayers% %maxplayers%
  samples:
    - |-
      &b&lCleanMOTD &f&lDefault &b&lSample
      &7Online: &a%onlineplayers%&8/&a%maxplayers%
    - |-
      &aCleanMOTD Default Sample &c[Optimized]
      &d&lNew Sample feature!

# This is shown as the server version name.
# Requires ProtocolLib on Bukkit to work.
protocol:
  enabled: false

  # Protocol name
  name: "FlameCord 1.7-1.16.5"

maxplayers:
  enabled: true

  # Changes the max players value.
"""

motd_2 = """

  # Changes the max player value depending on your onlineplayers.
  # Example: 12/13 players online.
  justonemore: false

# Requires ProtocolLib on Bukkit to work.
fakeplayers:
  enabled: true

  # Sets the amount of fakeplayers.
"""

motd_3 = """

  # "STATIC": Adds the value of fakeplayers to the amount of players online.
  # "RANDOM": Adds a random amount of players between 1 and the fakeplayers value.
  # "DIVISION": Adds the amount of players online divided by the fakeplayers value.
  mode: "STATIC"

# Using ProtocolLib will use packets instead of events.
motd:
  enabled: true

  # Placeholders: %onlineplayers% %maxplayers%
  motds:
    - |-
"""

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


def check_nmap():
    """ Check if nmap is installed """

    if os.system("nmap --version >nul 2>&1") == 0:
        return True

    print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}You need to install Nmap!")
    return False


def check_java():
    """ Check if java is installed """

    if os.system("java -version >nul 2>&1") == 0:
        return True

    print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}You need to install Java!")
    return False


def check_node():
    """ Check if nodejs is installed """

    if os.system("npm --version >nul 2>&1") == 0:
        os.system("title MCPTool")
        return True

    print(f"\n     {lblack}[{lred}ERR{white}OR{lblack}] {white}You need to install NodeJS!")
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


def check_encoding(file):
    try:
        f_ = open(file, "r+", encoding="utf8")
        f_.read()
        f_.close()
        return "utf8"

    except:
        f_ = open(file, "r+", encoding="unicode_escape")
        f_.read()
        f_.close()
        return "unicode_escape"

