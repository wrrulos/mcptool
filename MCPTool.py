#=============================================================================
#                      MCPTool v1.1 www.github.com/wrrulos
#                         Pentesting Tool for Minecraft
#                               Made by wRRulos
#                                  @wrrulos
#=============================================================================

# Any error report it to my discord please, thank you.
# Programmed in Python 3.9.7

z = 0

import os
import time

try:
    import colorama
    import requests

except:

    print("\n[-] Dependencies are missing...")

    time.sleep(2)

    print("[#] Verifying connection...")

    try:

        os.system("ping google.com >nul 2>&1")

        try:

            print("\n[#] Installing dependencies...\n\n")

            time.sleep(2)
        

            os.system("pip install requests & pip install colorama")

            import colorama
            import requests

        except:

            print("\n\nThere was an unexpected error.")
            print("Try to install the dependencies manually")

            print("\n - pip install colorama")
            print("\n - pip install requests\n\n")

            time.sleep(2)

            z = 1

            exit()

    except:

        if z == 1:

            exit()

        print("[-] You need to be connected to the internet")

        time.sleep(2)

        exit()
    
import platform
import json
import re
import socket

from random import randint
from datetime import datetime
from colorama import Fore, init

init ()

#=====================
#     VARIABLES
#=====================

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

urlmcsrv = "https://api.mcsrvstat.us/2/"
urlmojang = "https://api.mojang.com/users/profiles/minecraft/"
urlversion = "https://raw.githubusercontent.com/wrrulos/MCPTool/main/config/datos/version"
urlngrok = "http://localhost:4040/api/tunnels"
discord = "discord.gg/ewPyW4Ghzj"

animation = "|/-\\"
animation_two = "54321"

script_version = 2
script_version_two = "1.1"

host_list = ["minehost", "holyhosting"]
phishing_list = ["mc.universocraft.com"]

#######################################
#
# Check if the following folders exist
#
#######################################

def scans_folder():

    if os.path.isdir("scans"):
        pass

    else:
        os.mkdir("scans")

def ports_folder():

    if os.path.isdir("scans/ports"):
        pass

    else:
        os.mkdir("scans/ports")

def range_folder():

    if os.path.isdir("scans/range"):
        pass

    else:
        os.mkdir("scans/range")

def host_folder():

    if os.path.isdir("scans/host"):
        pass

    else:
        os.mkdir("scans/host")

def subd_folder():

    if os.path.isdir("scans/subdomains"):
        pass

    else:
        os.mkdir("scans/subdomains")

def minehost_folder():

    if os.path.isdir("scans/host/minehost"):
        pass

    else:
        os.mkdir("scans/host/minehost")

def holyhosting_folder():

    if os.path.isdir("scans/host/holyhosting"):
        pass

    else:
        os.mkdir("scans/host/holyhosting")

def config_folder():

    if os.path.isdir("config"):
        pass

    else:
        print(ERROR_MCPTOOL)

def data_folder():

    if os.path.isdir("config/data"):
        pass

    else:
        os.mkdir("config/data")
        print(script_version)
        version_file = open("config/data/version", "w")
        version_file.write(str(script_version))
        version_file.close()

def logs_folder():

    if os.path.isdir("logs"):
        pass

    else:
        os.mkdir("logs")

#######################
# Check connection
#######################

def check_connection():
    test = requests.get("https://www.google.com")


######################
# Save logs
#####################

def save_logs(error, error_name):
    save_logs_file = open("logs/logs.txt", "w", encoding="utf8")
    save_logs_file.write(f"[ERROR] {str(error_name)} -> {str(error)}")
    save_logs_file.close()


###################
# Clean the screen
###################

def cmd_clear(): 
    if so == "Windows":
        os.system("cls")

    if so == "Linux":
        os.system("clear")

##############
# Check xterm
##############

def check_xterm():

    test_xterm = os.system("which xterm >nul 2>&1")

    if str(test_xterm) == "0":

        pass

    else:
        
        print(ERROR_MCPTOOL)

#######################
# Check ngrok
#######################

def check_ngrok():
    if so == "Windows":

        if os.path.isfile("ngrok.exe"):
            pass

        else:
            print(ERROR_MCPTOOL)

    else:

        if os.path.isfile("ngrok"):
            pass

        else:
            print(ERROR_MCPTOOL)

##############################
# Check the operating system
##############################

def system():
    if so == "Windows":
        os.system(f"title MCPTool v{str(script_version_two)}")
        start()
        mcptool()

    elif so == "Linux":
        start()
        mcptool()
    
    else:
        exit()

######################################
#
# Check the latest version of mcptool
#
######################################

def check_version():
    global last_version
    global actual_version
    r = requests.get(urlversion)
    last_version = r.text
    version_file = open("config/data/version", "r")
    actual_version = version_file.read()

def banner():
    print("\n\n")
    print(f"    {red}███╗   ███╗ ██████╗██████╗     ████████╗ ██████╗  ██████╗ ██╗         {lred}Telegram: {white}wrrulos")
    print(f"    {red}████╗ ████║██╔════╝██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║         {lred}Discord: {white}Rulo#9224")
    print(f"    {red}██╔████╔██║██║     ██████╔╝       ██║   ██║   ██║██║   ██║██║         {lred}Github: {white}@wrrulos")
    print(f"    {white}██║╚██╔╝██║██║     ██╔═══╝        ██║   ██║   ██║██║   ██║██║     ")
    print(f"    {white}██║ ╚═╝ ██║╚██████╗██║            ██║   ╚██████╔╝╚██████╔╝███████╗    {lred}Minecraft Pentesting Tool {lgreen}v{str(script_version_two)}")
    print(f"    {white}╚═╝     ╚═╝ ╚═════╝╚═╝            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝" )
    print("\n")

def banner_two():
    print(f"\n\n\n\n\n\n\n\n\n                          {red}`7MMM.     ,MMF' .g8'''bgd `7MM'''Mq. MMP''MM''YMM              `7MM  ")
    print(f"                            {red}MMMb    dPMM .dP'     `M   MM   `MM.P'   MM   `7                MM ")
    print(f"                            {red}M YM   ,M MM dM'       `   MM   ,M9      MM  ,pW'Wq.   ,pW'Wq.  MM")
    print(f"                            {red}M  Mb  M' MM MM            MMmmdM9       MM 6W'   `Wb 6W'   `Wb M")
    print(f"                            {white}M  YM.P'  MM MM.           MM            MM 8M     M8 8M     M8 MM")
    print(f"                            {white}M  `YM'   MM `Mb.     ,'   MM            MM YA.   ,A9 YA.   ,A9 MM  ")
    print(f"                          {white}.JML. `'  .JMML. `'bmmmd'  .JMML.        .JMML.`Ybmd9'   `Ybmd9'.JMML.  \n\n\n")

def help():

    if language == "en":

        print("\n    ╔═════════════════════════════════════════════════════════════════════════════════════════════════╗")
        print("    ║                   Command                   ║                    Function                       ║")
        print("    ║                                             ║                                                   ║")
        print("    ║═════════════════════════════════════════════════════════════════════════════════════════════════║")
        print("    ║ server [ip]                                 ║ Displays information about a server.              ║")
        print("    ║ player [name]                               ║ Displays information about a player.              ║")
        print("    ║ scan-ports [ip] [ports] [y/n]               ║ Scan the ports of an IP.                          ║")
        print("    ║ scan-range [ip] [ports] [range] [y/n]       ║ Scan the range of an IP.                          ║")
        print("    ║ scan-host [host] [ports] [y/n]              ║ Scans the nodes of a host.                        ║")
        print("    ║ scan-subd [ip] [file]                       ║ Scans the nodes of a host.                        ║")
        print("    ║ bungee [ip:port]                            ║ Start a proxy server.                             ║")
        print("    ║ phishing [server]                           ║ Create a fake server to capture passwords.        ║")
        print("    ║                                             ║                                                   ║")
        print("    ║                                             ║                                                   ║")
        print("    ║ clear                                       ║ Clean the screen.                                 ║")
        #print("    ║ set-language [language]                     ║ Change the language of MCPTool.                   ║")
        print("    ╚═════════════════════════════════════════════════════════════════════════════════════════════════╝")
    
    elif language == "es":

        print("\n    ╔═════════════════════════════════════════════════════════════════════════════════════════════════╗")
        print("    ║                   Comando                   ║                 Funcion                           ║")
        print("    ║                                             ║                                                   ║")
        print("    ║═════════════════════════════════════════════════════════════════════════════════════════════════║")
        print("    ║ server [ip]                                 ║ Muestra informacion de un servidor.               ║")
        print("    ║ player [nombre]                             ║ Muestra informacion de un jugador.                ║")
        print("    ║ scan-ports [ip] [puertos] [y/n]             ║ Escanea los puertos de una IP.                    ║")
        print("    ║ scan-range [ip] [rango] [puertos] [y/n]     ║ Escanea el rango de una IP.                       ║")
        print("    ║ scan-host [host] [puertos] [y/n]            ║ Escanea los nodos de un host.                     ║")
        print("    ║ scan-subd [ip] [archivo]                    ║ Escanea los subdominios de un servidor.           ║")
        print("    ║ bungee [ip:puerto]                          ║ Inicia un servidor proxy.                         ║")
        print("    ║ phishing [server]                           ║ Crea un servidor falso para capturar contraseñas. ║")
        print("    ║                                             ║                                                   ║")
        print("    ║                                             ║                                                   ║")
        print("    ║ clear                                       ║ Limpia la pantalla.                               ║")
        #print("    ║ set-language [idioma]                       ║ Cambia el idioma de MCPTool.                      ║")
        print("    ╚═════════════════════════════════════════════════════════════════════════════════════════════════╝")


cmd_clear()
#banner()

def start():
    global language
    i = 0

    banner_two()

    for x in range(15):
        print(f"{white}                                                  Starting MCPTool..{animation[i % len(animation)]}", end="\r") 
        i += 1 
        time.sleep(0.2)

    # cargando configuraciones
    # verificar idioma y version

    try:

        cmd_clear()

        banner_two()

        for x in range(10):
            print(f"{white}                                               Loading configurations..{animation[i % len(animation)]}", end="\r") 
            i += 1 
            time.sleep(0.2)

        config_folder()
        data_folder()
        
        if os.path.isfile("config/data/language"):

            language_file = open("config/data/language", "r")
            language = language_file.read()
            language_file.close()

            if language == "en" or language == "es":
                pass
            
            else:

                language_file = open("config/data/language", "w+")
                language_file.truncate(0)
                language_file.write("en")
                language_file.close()

                language_file = open("config/data/language", "r")
                language = language_file.read()
                language_file.close()
        else:

            language_file = open("config/data/language", "w")
            language_file.write("en")
            language_file.close()

            language = "en"

        try:

            cmd_clear()

            banner_two()

            for x in range(10):
                print(f"{white}                                               Checking the connection..{animation[i % len(animation)]}", end="\r") 
                i += 1 
                time.sleep(0.2)

            check_connection()

            try:
                check_version()

                cmd_clear()

                banner_two()

                for x in range(10):
                    print(f"{white}                                                Checking for updates..{animation[i % len(animation)]}", end="\r") 
                    i += 1 
                    time.sleep(0.2)        

                try:

                    if int(last_version) > int(actual_version):

                        print(f"{white}                                           {lgreen}New version available on my github. ")
                        print(f"\n{white}                                               https://github.com/wrrulos/\n\n")

                        time.sleep(2)

                        for x in range(5):
                            print(f"{white}                                      Starting MCPTool with the current version in{lcyan} {animation_two[i % len(animation_two)]}", end="\r") 
                            i += 1 
                            time.sleep(1)
                        
                        cmd_clear()
                        banner()
                        
                    
                    else:
                        cmd_clear()
                        banner_two()

                        print(f"{white}                                           You are using the latest version!\n\n")

                        time.sleep(2)

                        cmd_clear()
                        banner()
                
                except:
                    cmd_clear()

                    banner_two()

                    print(f"\n{white}                                      There was an error checking for updates..\n\n")

                    time.sleep(2)

                    for x in range(5):
                        print(f"{white}                                   Starting MCPTool with the current version in{lcyan} {animation_two[i % len(animation_two)]}", end="\r") 
                        i += 1 
                        time.sleep(1)

                    cmd_clear()
                    banner()


            except Exception as error:
                cmd_clear()

                banner_two()

                print(f"\n{white}                                      There was an error checking for updates..\n\n")

                logs_folder()

                error_name = "Except(start/try.check_version)"

                save_logs(error, error_name)

                time.sleep(2)

                for x in range(5):
                    print(f"{white}                                     Starting MCPTool with the current version in{lcyan} {animation_two[i % len(animation_two)]}", end="\r") 
                    i += 1 
                    time.sleep(1)

                cmd_clear()
                banner()
        
        except:
            cmd_clear()

            banner_two()

            print(f"\n{white}                                      There was an error checking the connection.\n\n")

            time.sleep(2)

            for x in range(5):
                print(f"{white}                                     Starting MCPTool with the current version in{lcyan} {animation_two[i % len(animation_two)]}", end="\r") 
                i += 1 
                time.sleep(1)

            cmd_clear()
            banner()

        
    except Exception as error:
        cmd_clear()

        banner_two()

        print(f"\n{white}                                      There was an error loading the configuration.\n\n")

        logs_folder()

        error_name = "Except(start/try.config)"

        save_logs(error, error_name)

        time.sleep(2)

        for x in range(5):
            print(f"{white}                                     Starting MCPTool with the current version in{lcyan} {animation_two[i % len(animation_two)]}", end="\r") 
            i += 1 
            time.sleep(1)
        
        language = "en"

        cmd_clear()
        banner()



def mcptool():
    while True:

        print(f"\n {red}    MCPTool {lblack}» {white} ", end="")
        argument = input().split()
        
        if len(argument) == 0:

            if language == "en":

                print(f"\n     {lblack}[{red}-{lblack}] {lred}Unknown command. Type help to see the available commands.")

            elif language == "es":

                print(f"\n     {lblack}[{red}-{lblack}] {lred}Comando desconocido. Escribe help para ver los comandos disponibles")

        try:
            command = argument[0]

            if command == "help":

                help()

            elif command == "clear":

                cmd_clear()
                banner()

            elif command == "server":

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

                            if language == "en":

                                print(f"\n{white}     [{green}+{white}] IP: {lgreen} {str(ip)}")
                                print(f"{white}     [{green}+{white}] Port: {lgreen} {str(port)}")
                                print(f"{white}     [{green}+{white}] Version: {lgreen} {str(version)}")
                                print(f"{white}     [{green}+{white}] Players: {lgreen} {str(online_players)}/{str(online_players_max)}")
                                print(f"{white}     [{green}+{white}] MOTD: {lgreen} {str(clean)}")

                        except:

                            if language == "en":

                                print(f"\n     {white}[{red}-{white}] {lred}The server does not exist.")

                    except:

                        if language == "en":

                            print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                except:

                    if language == "en":

                        print(f"\n{white}     Usage: server [ip] or [ip:port]")

            elif command == "player":
                try:
                    player_name = argument[1]
                    try:

                        check_connection()

                        try:
                            r = requests.get(urlmojang + player_name)
                            r_json = r.json()

                            name = r_json["name"]
                            uuid = r_json["id"]

                            if language == "en":

                                print(f"\n{white}     [{green}+{white}] Name: {lgreen}{str(name)}")
                                print(f"{white}     [{green}+{white}] UUID: {lgreen}{str(uuid)}")

                        except:

                            if language == "en":

                                print(f"\n{white}     [{green}+{white}] Name: {lgreen}{str(player_name)}")
                                print(f"{white}     [{green}+{white}] UUID: {lred}None")

                    except:

                        if language == "en":

                            print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                except:

                    print(f"\n{white}     Usage: player [name]")

            elif command == "scan-ports":
                try:
                    ip = argument[1]
                    ports = argument[2]
                    show = argument[3].lower()
                    numservers = 0

                    # Detect ports

                    try:
                        # Errors

                        # If the ports are equal to "all"

                        if ports.lower() == "all":
                            ports = "0-65535"

                        # If ports are numbers...

                        elif ports.isdecimal():


                            # If the ports are less than or equal to 65535

                            if int(ports) <= 65535:
                                pass
                                
                            # Error 

                            else:

                                print(ERROR_MCPTOOL)

                        # If the ports are not "all" or are just numbers, then they are a range (25000-26000 for example)

                        else:

                            # If this gives an error, it shows the exception message

                            ports = ports.split("-")

                            # If rank 1 is greater than or equal to rank 2

                            if int(ports[0]) >= int(ports[1]):

                                print(ERROR_MCPTOOL)


                            # If rank 2 is greater than 65535

                            if int(ports[1]) > 65535:

                                print(ERROR_MCPTOOL)

                            # Return ports to normal

                            ports = f"{str(ports[0])}-{str(ports[1])}"
                        
                        try:

                            if not show == "y" and not show == "n":

                                 print(ERROR_MCPTOOL)
                                
                            else:
                                pass

                            try:
                                check_connection()
                                    
                                try:
                                    check_ip = socket.gethostbyname(str(ip))
                                    try:

                                        date = datetime.now()

                                        file = f"temp_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"

                                        os.system(f"nmap -p {str(ports)} -T5 -Pn -v -oN {file} {str(ip)} >nul 2>&1")

                                        scans_folder()
                                        ports_folder()

                                        data_file_date = datetime.now()

                                        logs_file = open(f"scans/ports/Port_{str(data_file_date.day)}-{str(data_file_date.month)}-{str(data_file_date.year)}_{str(data_file_date.hour)}.{str(data_file_date.minute)}.{str(data_file_date.second)}.txt", "w", encoding="utf8")

                                        logs_file.write("MCPTool @wrrulos \n\n")

                                        if language == "en":

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
                                                ports = re.findall(r"([0-9]+)/tcp", result)

                                                for port in ports:
                                                    try:

                                                        scket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                                                        scket.settimeout(2)
                                                        scket.connect((ip, int(port)));
                                                        scket.send(b"\xfe\x01");

                                                        data = scket.recv(1024)[3:].decode("utf-16be")[3:].split("\x00")

                                                        scket.close()

                                                        version = re.sub(r"§[a-zA-Z0-9]", "", data[1].strip().replace("  ", "").replace("  ", ""))
                                                        motd = re.sub(r"§[a-zA-Z0-9]", "", data[2].strip().replace("  ", "").replace("  ", ""))
                                                        players = re.sub(r"§[a-zA-Z0-9]", "", f"{data[3]}/{data[4]}".strip().replace("  ", "").replace("  ", ""))

                                                        if language == "en":

                                                            numservers += 1

                                                            print(f"\n{white}     [{lgreen}√{white}] {green} Server found:")
                                                            print(f"\n{white}        IP: {lcyan}{str(ip)}:{str(port)}")
                                                            print(f"        {white}MOTD: {lcyan}{str(motd)}")
                                                            print(f"        {white}Version: {lcyan}{str(version)}")
                                                            print(f"        {white}Players: {lcyan}{str(players)}\n")

                                                            logs_file.write("[+] Server found: \n\n")
                                                            logs_file.write(f"    IP: {str(ip)}:{str(port)}\n")
                                                            logs_file.write(f"    MOTD: {str(motd)}\n")
                                                            logs_file.write(f"    Version: {str(version)}\n")
                                                            logs_file.write(f"    Players: {str(players)}\n")

                                                    except socket.timeout:

                                                        if show == "y":

                                                            if language == "en":

                                                                print(f"\n{white}    [{lred}-{white}] {green}Server found: {red}(time out){green}: ")
                                                                print(f"\n        {white}IP: {lcyan}{str(ip)}:{str(port)}\n")
                                                                logs_file.write(f"[-] Server found (Offline)     IP: {str(ip)}:{str(port)}\n\n")

                                                    except:
                                                        pass

                                            print("")

                                            if language == "en":

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

                                        except Exception as error:
                                                
                                            logs_folder()
                                            error_name = "Except/scan-ports/try.temp-file"
                                            save_logs(error, error_name)

                                    except Exception as error:
                                            
                                        logs_folder()
                                        error_name = "Except/scan-ports/try.date.timenow"
                                        save_logs(error, error_name)

                                except:

                                    if language == "en":

                                        print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid IP")
                                        
                            except:

                                if language == "en":

                                    print(f"\n     {white}[{red}-{white}] {lred}Connection error.")
                                        
                        except:

                            if language == "en":

                                print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Enter a valid option (y or n)") 

                    except:

                        if language == "en":

                            print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid port range")

                except:
                    
                    if language == "en":

                        print(f"\n{white}     Usage: scan-ports [ip] [ports] [y/n]")
            
            elif command == "scan-range":
                try:
                    ip = argument[1]
                    iprange = argument[2]
                    ports_range = argument[3].lower()
                    show = argument[4].lower()

                    numservers = 0

                    # Detect ports

                    try:       

                        # Errors

                        # If the ports are equal to "all"

                        if ports_range == "all":

                            ports_range = "0-65535"

                        # If ports are numbers...

                        elif ports_range.isdecimal():

                            # If the ports are less than or equal to 65535

                            if int(ports_range) <= 65535:
                                pass
                            
                            # Error

                            else:

                                print(ERROR_MCPTOOL)
                        
                        # If the ports are not "all" or are just numbers, then they are a range (25000-26000 for example)

                        else:

                            # If this gives an error, it shows the exception message

                            ports_range = ports_range.split("-")

                            # If rank 1 is greater than or equal to rank 2

                            if ports_range[0] >= ports_range[1]:

                                print(ERROR_MCPTOOL)

                            # If rank 2 is greater than 65535

                            if int(ports_range[1]) > 65535:

                                print(ERROR_MCPTOOL)

                            # Return ports to normal

                            ports_range = f"{str(ports_range[0])}-{str(ports_range[1])}"
                        
                        try:
                            
                            if iprange == "*":

                                x = 0
                                y = 255

                            else:

                                iprange = iprange.split("-")

                                if iprange[0] >= iprange[1]:

                                    print(ERROR_MCPTOOL)

                                x = iprange[0]
                                y = iprange[1]

                                x = int(x)
                                y = int(y)

                                if y >= 255:
                                    y = 255

                            try:
                                
                                if not show == "y" and not show == "n":

                                    print(ERROR_MCPTOOL)
                                    
                                else:
                                    pass

                                try:
                                    check_connection()

                                    try:
                                        check_ip = socket.gethostbyname(f"{str(ip)}.{str(x)}")

                                        try:

                                            scans_folder()
                                            range_folder()

                                            data_file_date = datetime.now()

                                            logs_file = open(f"scans/range/Range_{str(data_file_date.day)}-{str(data_file_date.month)}-{str(data_file_date.year)}_{str(data_file_date.hour)}.{str(data_file_date.minute)}.{str(data_file_date.second)}.txt", "w", encoding="utf8")

                                            logs_file.write("MCPTool @wrrulos \n\n")

                                            if language == "en":

                                                logs_file.write("Range Scan \n\n")
                                                logs_file.write("Information:\n\n")
                                                logs_file.write(f"    Date: {str(data_file_date.year)}-{str(data_file_date.month)}-{str(data_file_date.day)}\n")
                                                logs_file.write(f"    Hour: {str(data_file_date.hour)}.{str(data_file_date.minute)}.{str(data_file_date.second)}\n")
                                                logs_file.write(f"    IP: {str(ip)}\n")
                                                logs_file.write(f"    Ports: {str(ports_range)}\n")

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

                                                    if language == "en":

                                                        print(f"     {lblack}[{lgreen}+{lblack}] {white}Scanning {green} {ip_range}")

                                                    #print(f"nmap -p {str(ports_range)} -T5 -v -oN {file} {str(ip_range)} >nul")

                                                    os.system(f"nmap -p {str(ports_range)} -T5 -Pn -v -oN {file} {str(ip_range)} >nul 2>&1")
                                                        
                                                    try:

                                                        temp_file = open(file, "r")

                                                        temp_file_result = temp_file.read()

                                                        temp_file.close()

                                                        temp_file_result = temp_file_result.split("Nmap scan report for ")

                                                        for result in temp_file_result:

                                                            ports = re.findall(r"([0-9]+)/tcp", result)

                                                            for port in ports:
                                                                try:

                                                                    scket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                                                                    scket.settimeout(2)
                                                                    scket.connect((ip_range, int(port)));
                                                                    scket.send(b"\xfe\x01");

                                                                    data = scket.recv(1024)[3:].decode("utf-16be")[3:].split("\x00")

                                                                    scket.close()

                                                                    version = re.sub(r"§[a-zA-Z0-9]", "", data[1].strip().replace("  ", "").replace("  ", ""))
                                                                    motd = re.sub(r"§[a-zA-Z0-9]", "", data[2].strip().replace("  ", "").replace("  ", ""))
                                                                    players = re.sub(r"§[a-zA-Z0-9]", "", f"{data[3]}/{data[4]}".strip().replace("  ", "").replace("  ", ""))

                                                                    if language == "en":

                                                                        numservers += 1

                                                                        print(f"\n{white}     [{lgreen}√{white}] {green} Server found:")
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

                                                                        if language == "en":

                                                                            print(f"\n{white}     [{lred}-{white}] {green}Server found: {red}(time out){green}: ")
                                                                            print(f"\n        {white}IP: {lcyan}{str(ip_range)}:{str(port)}\n")
                                                                            logs_file.write(f"[-] Server found (Offline)     IP: {str(ip)}:{str(port)}\n\n")

                                                                except:
                                                                    pass

                                                        os.remove(file)
                                                        print(reset)

                                                        x +=1

                                                    except Exception as error:

                                                        logs_folder()
                                                        error_name = "Except/scan-range/try.temp-file"
                                                        save_logs(error, error_name)

                                                if language == "en":

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

                                            except Exception as error:

                                                logs_folder()
                                                error_name = "Except/scan-range/try.while.x"
                                                save_logs(error, error_name)

                                        except Exception as error:

                                            logs_folder()
                                            error_name = "Except/scan-range/try.data.file.date"
                                            save_logs(error, error_name)

                                    except:

                                        if language == "en":

                                            print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid IP")

                                except:

                                    if language == "en":

                                        print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                            except:

                                if language == "en":

                                    print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Enter a valid option (y or n)") 

                        except:

                            if language == "en":

                                print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid IP range")
                                
                    except:

                        if language == "en":

                            print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid port range")

                except: 
                    
                    if language == "en":

                        print(f"\n{white}     Usage: scan-range [ip] [range] [ports] [y/n]")
        
            elif command == "scan-host":
                try:
                    host = argument[1].lower()
                    host_ports = argument[2]
                    show = argument[3].lower()

                    numservers = 0

                    try:

                        show_host_list = host_list

                        show_host_list = str(show_host_list).replace("[", "").replace("]", "").replace("'", "")

                        try:
                            
                            if host in host_list:
                                pass
                        
                            else:

                                print(ERROR_MCPTOOL)
                            
                            try:

                                # Errors

                                # If the ports are equal to "all"

                                if host_ports.lower() == "all":
                                    host_ports = "0-65535"
                                
                                # If ports are numbers...

                                elif host_ports.isdecimal():
                        
                                    # If the ports are less than or equal to 65535

                                    if int(host_ports) <= 65535:
                                        pass

                                    # Error

                                    else:

                                        print(ERROR_MCPTOOL)
                                
                                else:

                                    # If this gives an error, it shows the exception message

                                    host_ports = host_ports.split("-")

                                    # If rank 1 is greater than or equal to rank 2

                                    if int(host_ports[0]) >= int(host_ports[1]):

                                        print(ERROR_MCPTOOL)

                                    # If rank 2 is greater than 65535

                                    if int(host_ports[1]) > 65535:

                                        print(ERROR_MCPTOOL)

                                    # Return ports to normal

                                    host_ports = f"{str(host_ports[0])}-{str(host_ports[1])}"

                                try:
                                    if not show == "y" and not show == "n":

                                        print(ERROR_MCPTOOL)
                                        
                                    else:
                                        pass

                                    try:
                                        check_connection()

                                        try:
                                            
                                            scans_folder()
                                            host_folder()

                                            date = datetime.now()

                                            if host == "minehost":
                                                minehost_folder()
                                                nodes = ("sv1", "sv10", "sv11", "sv15", "sv16", "sv17")
                                                domain = ".minehost.com.ar"
                                                file = f"scans/host/minehost/Minehost_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"
                                                nmap_file = "minehost_temp.txt"
                                            
                                            elif host == "holyhosting":
                                                holyhosting_folder()
                                                nodes = ("node-premium", "node-premium1", "node-premium2", "node-ashburn", "node-newyork", "node-valdivia", "node-dallas", "node-paris", "ca", "tx", "tx2", "fr")
                                                domain = ".holy.gg"
                                                file = f"scans/host/holyhosting/Holyhosting_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"
                                                nmap_file = "holyhosting_temp.txt"     
                                            
                                            nodes_file = f"nodes_host_{str(host)}{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt"
                                            nodes_list = open(nodes_file, "w", encoding="utf8")
                                            nodes_list.truncate(0)
                                            logs_file = open(file, "w", encoding="utf8")

                                            if language == "en":

                                                logs_file.write("Host scan \n\n")
                                                logs_file.write("Information:\n\n")
                                                logs_file.write(f"    Date: {str(date.year)}-{str(date.month)}-{str(date.day)}\n")
                                                logs_file.write(f"    Hour: {str(date.hour)}.{str(date.minute)}.{str(date.second)}\n")
                                                logs_file.write(f"    Host: {str(host)}\n")
                                                logs_file.write(f"    Ports: {str(host_ports)}\n\n")
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

                                            for line in ip_list:

                                                ip = ip_list.readline()
                                                ip = ip.replace("\n", "")

                                                print("")

                                                if language == "en":

                                                    print(f"     {lblack}[{lgreen}+{lblack}] {white}Scanning {green} {ip}")

                                                os.system(f"nmap -p {str(host_ports)} -T5 -Pn -v -oN {nmap_file} {str(ip)} >nul 2>&1")

                                                print("")

                                                host_scan = open(nmap_file, "r", encoding="utf8")
                                                host_result = host_scan.read()
                                                results = host_result.split("Nmap scan report for ")

                                                for result in results:

                                                    ports = re.findall(r"([0-9]+)/tcp", result)

                                                    for port in ports:

                                                        try:

                                                            scket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                                                            scket.settimeout(2)
                                                            scket.connect((ip, int(port)));
                                                            scket.send(b"\xfe\x01");

                                                            data = scket.recv(1024)[3:].decode("utf-16be")[3:].split("\x00")

                                                            scket.close()

                                                            version = re.sub(r"§[a-zA-Z0-9]", "", data[1].strip().replace("  ", "").replace("  ", ""))
                                                            motd = re.sub(r"§[a-zA-Z0-9]", "", data[2].strip().replace("  ", "").replace("  ", ""))
                                                            players = re.sub(r"§[a-zA-Z0-9]", "", f"{data[3]}/{data[4]}".strip().replace("  ", "").replace("  ", ""))


                                                            if language == "en":

                                                                numservers += 1

                                                                print(f"\n{white}     [{lgreen}√{white}] {green} Server found:")
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

                                                                if language == "en":

                                                                    print(f"\n{white}     [{lred}-{white}] {green}Server found: {red}(time out){green}: ")
                                                                    print(f"\n        {white}IP: {lcyan}{str(ip)}:{str(port)}\n")
                                                                    logs_file.write(f"[-] Server found (Offline)     IP: {str(ip)}:{str(port)}\n\n")

                                                        except:
                                                            pass
                                                
                                                host_scan.close()
                                            
                                            if language == "en":

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

                                        except Exception as error:
                                            logs_folder()
                                            error_name = "Except/scan-host/try.date.timenow"
                                            save_logs(error, error_name)
                                    
                                    except:

                                        if language == "en":

                                            print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                                except:

                                    if language == "en":

                                        print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Enter a valid option (y or n)") 
                                        
                            except:

                                if language == "en":

                                    print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid port range")

                        except:

                            if language == "en":

                                print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Host not found.") 
                                print(f"     {white}Availables host: {green}{str(show_host_list)}")

                    except Exception as error:

                        if language == "en":

                            print(f"\n     {white}[{lred}ERROR{white}] {white}There is a problem with the variable {red}host_list {white}({str(error)})")

                except:

                    if language == "en":

                        print(f"\n{white}     Usage: scan-host [host] [ports] [y/n]")
            
            elif command == "scan-subd":
                try:
                    domain = argument[1]
                    subdomains_file = argument[2].lower()

                    number_of_lines = 0
                    num_subd = 0
                    ips_list = []

                    try:
                        location = f"config/subdomains/{str(subdomains_file)}"

                        with open(location) as file:
                            for lines in file:
                                number_of_lines += 1
                        
                        try:
                            check_connection()

                            try:

                                check_domain = socket.gethostbyname(f"{str(domain)}")

                                try:

                                    if language == "en":

                                        print(f"\n     {white}[{lgreen}+{white}] Scanning the domain {green}{str(domain)}\n")
                                        print(f"     {white}File: {str(subdomains_file)} ({str(number_of_lines)} subdomains)")

                                    date = datetime.now()
                                    scans_folder()
                                    subd_folder()

                                    logs_file = open(f"scans/subdomains/Subdomain_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt", "w", encoding="utf8")

                                    print("")

                                    if language == "en":
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

                                                if str(ip_subdomain) not in ips_list:
                                                    ips_list.append(str(ip_subdomain))

                                                    if language == "en":
                                                        num_subd += 1
                                                        print(f"     {white}[{lgreen}√{white}] Subdomain found {lblack}» {green}{str(subdomain)} {lgreen}{str(ip_subdomain)}")
                                            
                                            except:
                                                pass

                                    print("")

                                    if language == "en":

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

                                if language == "en":

                                    print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid Domain")

                        except:

                            if language == "en":

                                print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                    except:
                        
                        if language == "en":

                            print(f"\n     {white}[{lred}Invalid arguments{white}] {white}The file ({str(subdomains_file)}) was not found")
                except:

                    if language == "en":

                        print(f"{white}\n     Usage: scan-subd [domain] [file]")

            elif command == "bungee":
                    try:
                        ip = argument[1]
                        try:

                            if so == "Windows":

                                pass
                            
                            else:

                                check_xterm()

                            try:
                                print("")

                                if language == "en":
                                    print(f"     {white}[{green}+{white}] {lgreen}Starting proxy...")

                                config_file = open("config/files/config_bungee.txt", "r")
                                yml_config = config_file.read()
                                config_file.close()

                                config_file = open("config/bungee/config.yml", "w+")
                                config_file.truncate(0)
                                config_file.write(yml_config)
                                config_file.write(f"\n    address: {str(ip)}\n")
                                config_file.write(f"    restricted: false")
                                config_file.close()

                                if so == "Windows":

                                    os.system("cd config/bungee && start iniciar.bat")
                                
                                else:

                                    os.system('cd config/bungee && xterm -T "Proxy" -e bash iniciar.sh &')

                                time.sleep(10)

                                print(f"\n     {white}[{green}+{white}] IP: {lgreen}0.0.0.0:25567")

                            except Exception as error:

                                print(f"\n     {white}[{red}ERROR{white}] {lred}Unknown error (The error was saved in the logs)")

                                logs_folder()
                                error_name = "Except/bungees/try"
                                save_logs(error, error_name)

                        except:

                            if language == "en":

                                    print(f"\n     {white}[{red}-{white}] {lred}You don't have xterm installed. (Try installing it using sudo apt-get install -y xterm)")

                    except:

                        if language == "en":

                            print(f"{white}\n     Usage: bungee [ip:port]")

            elif command == "phishing":
                try:
                    server = argument[1].lower()

                    try:

                        show_phishing_list = phishing_list

                        show_phishing_list = str(show_phishing_list).replace("[", "").replace("]", "").replace("'", "")

                        if server in phishing_list:
                            pass

                        else:
                            print(ERROR_MCPTOOL)
                        
                        try:
                            check_ngrok()

                            try:
                                if so == "Windows":

                                    pass

                                else:
                                    check_xterm()
                                
                                try:
                                    check_connection()

                                    try:

                                        if server == "mc.universocraft.com":
                                            configplayers_directory = "config/phishing/mc.universocraft.com/plugins/FakePlayers/config.yml"
                                            properties_directory = "config/phishing/mc.universocraft.com/server.properties"
                                            data_directory = "config/phishing/mc.universocraft.com/datos.txt"
                                            ipp_file_directory = "config/phishing/mc.universocraft.com/ip_phishing.txt"

                                        if so == "Windows":

                                            command_start_server = "cd config/phishing && cd mc.universocraft.com && start iniciar.bat"
                                            command_start_console = "cd config/phishing && cd mc.universocraft.com && start python consola.py"

                                            server_properties = open("config/files/server.properties_windows", "r")
                                            config_server_properties = server_properties.read()
                                            server_properties.close()

                                            server_properties = open(properties_directory, "w+")
                                            server_properties.truncate(0)
                                            server_properties.write(config_server_properties)
                                            server_properties.close()


                                        else:

                                            command_start_server = 'cd config/phishing && cd mc.universocraft.com && xterm -T "Phishing: mc.universocraft.com" -e bash iniciar.sh &'
                                            command_start_console = 'cd config/phishing && cd mc.universocraft.com && xterm -T "Consola: mc.universocraft.com" -e python3 consola.py &'

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

                                            random_number = randint(1000,8000)

                                            configplayers_file = open(configplayers_directory, "w+")
                                            configplayers_file.truncate(0)
                                            configplayers_file.write("Enabled: true \n")
                                            configplayers_file.write("Add Real Players: true \n")
                                            configplayers_file.write("Online Players: " + str(random_number) + " \n")
                                            configplayers_file.write("Max Players: 20000")
                                            configplayers_file.close()

                                        print("")

                                        if language == "en":

                                            print(f"     {white}[{green}+{white}] {lgreen}Starting server...")
                                        
                                        os.system(command_start_server)
                                        time.sleep(3)

                                        if language == "en":

                                            print(f"     {white}[{green}+{white}] {lgreen}Starting ngrok...")

                                        if so == "Windows":
                                        
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

                                    except Exception as error:

                                        print(f"\n     {white}[{red}ERROR{white}] {lred}Unknown error (The error was saved in the logs)")

                                        logs_folder()
                                        error_name = "Except/phishing/try"
                                        save_logs(error, error_name)

                                except:

                                    if language == "en":

                                        print(f"\n     {white}[{red}-{white}] {lred}Connection error.")

                            except:

                                if language == "en":

                                    print(f"\n     {white}[{red}-{white}] {lred}You don't have xterm installed. (Try installing it using sudo apt-get install -y xterm)")
                        
                        except:

                            if so == "Windows":

                                if language == "en":

                                        print(f"\n     {white}[{red}-{white}] {lred}The file ngrok.exe could not be found")

                            else:

                                if language == "en":

                                    print(f"\n     {white}[{red}-{white}] {lred}The file ngrok could not be found")

                    except:
                        if language == "en":

                            print(f"\n     {white}[{lred}Invalid arguments{white}] {white}Please enter a valid server")
                            print(f"     {white}Available servers: {green}{str(show_phishing_list)}")

                except:
                    if language == "en":

                            print(f"{white}\n     Usage: phishing [server]")
                            print(f"     {white}Available servers: {green}{str(show_phishing_list)}")

            elif command == "discord":

                if language == "en":

                    print(f"\n     My Discord server: {green}{str(discord)}")

            else:

                if language == "en":

                    print(f"\n     {lblack}[{red}-{lblack}] {lred}Unknown command. Type help to see the available commands.")

        except:

            pass

system()







