#=============================================================================
#                      MCPTool v1.0 www.github.com/wrrulos
#                    Herramienta de Pentesting para Minecraft
#                               Hecho por wRRulos
#                                   @wrrulos
#=============================================================================

# Cualquier error reportarlo en mi discord por favor, gracias.
# Programado en Python 3.9.7

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

init ()

os.system("title MCPTool v1.0")
#os.system("mode con cols=120 LINES=40")

#=====================
#     VARIABLES
#=====================

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

#==========================
#    Limpia la pantalla
#==========================

def cmd_clear(): 
    if so == "Windows":
        os.system("cls")

#===========================
#    Verifica la conexion
#===========================

def verificar_conexion():
    prueba = requests.get(urlmojang)

#===================================
#    Verifica el sistema operativo
#===================================

def verificar_so():
    if so == "Windows":
        pass

    else:
        print("\n" + lrojo + "    Sistema operativo no compatible.")
        time.sleep(2)
        exit()

#==========================
#    Verifica el idioma
#==========================

def verificar_idioma():
    global idioma
    if os.path.isdir("config/datos"): 
        if os.path.isfile("config/datos/idioma"):
            archivo_idioma = open("config/datos/idioma", "r")
            idioma = archivo_idioma.read()
            archivo_idioma.close()

            if idioma == "es" or idioma == "en":
                pass

            else:
                print("\n" + lnegro + "    [" + rojo + "-" + lnegro + "]" + lrojo + " Se ha detectado un idioma desconocido. ")

                time.sleep(2)

                print("\n" + lrojo + "    MCPTool se ejecutara en su idioma predeterminado (Español).")

                archivo_idioma = open("config/datos/idioma", "w+")
                archivo_idioma.truncate(0)
                archivo_idioma.write("es")
                archivo_idioma.close()

                archivo_idioma = open("config/datos/idioma", "r")
                idioma = archivo_idioma.read()
                archivo_idioma.close()

                time.sleep(2)
            
        else:
            print("\n" + lnegro + "    [" + rojo + "-" + lnegro + "]" + lrojo + " No se encontro la configuracion del idioma.")

            time.sleep(2)

            print("\n" + lrojo + "    MCPTool se ejecutara en su idioma predeterminado (Español).")

            archivo_idioma = open("config/datos/idioma", "w")
            archivo_idioma.write("es")
            archivo_idioma.close()

            archivo_idioma = open("config/datos/idioma", "r")
            idioma = archivo_idioma.read()
            archivo_idioma.close()

            time.sleep(2)

    else:
        print("\n" + lnegro + "    [" + rojo + "-" + lnegro + "]" + lrojo + " No se encontro la carpeta datos.")

        time.sleep(2)

        print("\n" + lrojo + "    MCPTool se ejecutara en su idioma predeterminado (Español).")

        os.mkdir("config/datos")

        archivo_idioma = open("config/datos/idioma", "w")
        archivo_idioma.write("es")
        archivo_idioma.close()

        archivo_idioma = open("config/datos/idioma", "r")
        idioma = archivo_idioma.read()
        archivo_idioma.close()

        time.sleep(2)

#======================================
#   Verifica si esta instalado Nmap
#======================================

def verificar_nmap():
    nmap = os.system("nmap -version >nul")

    if str(nmap) == "0":
        pass

    else:
        cmd_clear()
        print("\n" + lrojo + "    No está instalado Nmap. Por favor instalalo y vuelva a ejecutar MCPTool.")
        time.sleep(4)
        exit()

#===========================================
#   Verifica si existe la carpeta escaneos
#===========================================

def carpeta_escaneos(): 
    if os.path.isdir("escaneos"):
        pass

    else:
        os.mkdir("escaneos")

#===========================================
#   Verifica si existe la carpeta host
#===========================================

def carpeta_escaneos_host(): 
    if os.path.isdir("escaneos/host"):
        pass

    else:
        os.mkdir("escaneos/host")

#===========================================
#   Verifica si existe la carpeta minehost
#===========================================

def carpeta_host_minehost(): 
    if os.path.isdir("escaneos/host/minehost"):
        pass

    else:
        os.mkdir("escaneos/host/minehost")

#=============================================
#   Verifica si existe la carpeta vyxterhost
#=============================================

def carpeta_host_vyxterhost(): 
    if os.path.isdir("escaneos/host/vyxterhost"):
        pass

    else:
        os.mkdir("escaneos/host/vyxterhost")

#==============================================
#   Verifica si existe la carpeta holyhosting
#==============================================

def carpeta_host_holyhosting(): 
    if os.path.isdir("escaneos/host/holyhosting"):
        pass

    else:
        os.mkdir("escaneos/host/holyhosting")


#===========================================
#   Verifica si existe la carpeta subdominios
#===========================================

def carpeta_subd(): 
    if os.path.isdir("escaneos/subdominios"):
        pass

    else:
        os.mkdir("escaneos/subdominios")

#==============
#   BANNER 1
#==============

def banner():
    print("\n\n")
    print(rojo + "    ███╗   ███╗ ██████╗██████╗     ████████╗ ██████╗  ██████╗ ██╗     " + lrojo + "    Telegram: " + blanco + "wrrulos")
    print(rojo + "    ████╗ ████║██╔════╝██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     " + lrojo + "    Discord: " + blanco + "Rulo#9224")
    print(rojo + "    ██╔████╔██║██║     ██████╔╝       ██║   ██║   ██║██║   ██║██║     " + lrojo + "    Github: " + blanco + "@wrrulos")
    print(blanco + "    ██║╚██╔╝██║██║     ██╔═══╝        ██║   ██║   ██║██║   ██║██║     " )
    print(blanco + "    ██║ ╚═╝ ██║╚██████╗██║            ██║   ╚██████╔╝╚██████╔╝███████╗" + lrojo + "    Minecraft Pentesting Tool " + lverde + "v0.3")
    print(blanco + "    ╚═╝     ╚═╝ ╚═════╝╚═╝            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝" )
    print("\n")

#============
#  Help_ES
#============

def cmd_help_es():
    print("")
    print("    ╔═════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print("    ║                   Comando                   ║                 Funcion                           ║")
    print("    ║                                             ║                                                   ║")
    print("    ║═════════════════════════════════════════════════════════════════════════════════════════════════║")
    print("    ║ server [ip]                                 ║ Muestra informacion de un servidor.               ║")
    print("    ║ player [nombre]                             ║ Muestra informacion de un jugador.                ║")
    print("    ║ scan-ports [ip] [puertos] [y/n]             ║ Escanea los puertos de una IP.                    ║")
    print("    ║ scan-range [ip] [rango] [puertos] [y/n]     ║ Escanea el rango de una IP.                       ║")
    print("    ║ scan-host [host] [puertos] [y/n]            ║ Escanea los nodos de un host.                     ║")
    print("    ║ scan-subd [ip]                              ║ Escanea los subdominios de un servidor.           ║")
    print("    ║ bungee [ip:puerto]                          ║ Inicia un servidor proxy.                         ║")
    print("    ║ phishing [server]                           ║ Crea un servidor falso para capturar contraseñas. ║")
    print("    ║                                             ║                                                   ║")
    print("    ║                                             ║                                                   ║")
    print("    ║ clear                                       ║ Limpia la pantalla.                               ║")
    print("    ║ help-cmd [command]                          ║ Obten ayuda de un comando especifico.             ║")
    print("    ║ set-language [idioma]                       ║ Cambia el idioma de MCPTool.                      ║")
    print("    ╚═════════════════════════════════════════════════════════════════════════════════════════════════╝") 

#============
#  Help_EN
#============

def cmd_help_en():
    print("")
    print("    ╔═════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print("    ║                   Command                   ║                    Function                       ║")
    print("    ║                                             ║                                                   ║")
    print("    ║═════════════════════════════════════════════════════════════════════════════════════════════════║")
    print("    ║ server [ip]                                 ║ Displays information about a server.              ║")
    print("    ║ player [name]                               ║ Displays information about a player.              ║")
    print("    ║ scan-ports [ip] [ports] [y/n]               ║ Scan the ports of an IP.                          ║")
    print("    ║ scan-range [ip] [ports] [range] [y/n]       ║ Scan the range of an IP.                          ║")
    print("    ║ scan-host [host] [ports] [y/n]              ║ Scans the nodes of a host.                        ║")
    print("    ║ scan-subd [ip]                              ║ Scans the nodes of a host.                        ║")
    print("    ║ bungee [ip:port]                            ║ Start a proxy server.                             ║")
    print("    ║ phishing [server]                           ║ Create a fake server to capture passwords.        ║")
    print("    ║                                             ║                                                   ║")
    print("    ║                                             ║                                                   ║")
    print("    ║ clear                                       ║ Clean the screen.                                 ║")
    print("    ║ help-cmd [command]                          ║ Get help from a specific command.                 ║")
    print("    ║ set-language [language]                     ║ Change the language of MCPTool.                   ║")
    print("    ╚═════════════════════════════════════════════════════════════════════════════════════════════════╝")

cmd_clear()
banner()

def menu():
    while True:
        verificar_idioma()
        print("")
        print(rojo + "    MCPTool " + lnegro + "» " + blanco + "" + "", end="")
        argumento = input().split()
        try:
            comando = argumento[0].lower()
            if comando == "help": # Comando de ayuda
                if idioma == "es":
                    cmd_help_es()

                elif idioma == "en":
                    cmd_help_en()

            elif comando == "clear": # Comando para Limpiar la pantalla
                cmd_clear()
                banner()

            elif comando == "server": # Comando para obtener informacion de un servidor (IP, puerto, jugadores, version y motd)
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
                                print("\n" + blanco + "    [" + verde + "+" + blanco + "]" + blanco + " IP Númerica: " + lverde + str(ip))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Puerto: " + lverde + str(puerto))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Versión: " + lverde + str(version))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Jugadores: " + lverde + str(jugadores_online) + lnegro + "/" + verde + str(jugadores_maximo))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " MOTD: " + lverde + str(clean))

                            elif idioma == "en":
                                print("\n" + blanco + "    [" + verde + "+" + blanco + "]" + blanco + " IP: " + lverde + str(ip))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Port: " + lverde + str(puerto))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Versión: " + lverde + str(version))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Players: " + lverde + str(jugadores_online) + lnegro + "/" + verde + str(jugadores_maximo))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " MOTD: " + lverde + str(clean))

                        except:
                            if idioma == "es":
                                print("\n" + blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " El servidor no existe.")

                            elif idioma == "en":
                                print("\n" + blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " The server does not exist.")

                    except:
                        if idioma == "es":
                            print("\n" + blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Error de conexión.")

                        elif idioma == "en":
                            print("\n" + blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Connection error.")

                except:
                    if idioma == "es":
                        print("\n" + blanco + "    Usa: server [ip] o [ip:port]")
                        print("\n" + blanco + "    Para ver más informacion usa " + lcyan + "help-cmd server")

                    elif idioma == "en":
                        print("\n" + blanco + "    Usage: server [ip] or [ip:port]")
                        print("\n" + blanco + "    To see more information use " + lcyan + "help-cmd server")

            elif comando == "player": # Comando para obtener informacion de un nombre de Minecraft (Nombre y uuid)
                try:
                    jugador = argumento[1]
                    try:
                        verificar_conexion()
                        print("")
                        try:
                            respuesta = requests.get(urlmojang + jugador)
                            respuesta_json = respuesta.json()

                            nombre = respuesta_json["name"]
                            uuid =  respuesta_json["id"]
                            
                            if idioma == "es":
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Nombre: " + lverde + str(nombre))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " UUID: " + lverde + str(uuid))

                            elif idioma == "en":
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Name: " + lverde + str(nombre))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " UUID: " + lverde + str(uuid))           

                        except:
                            if idioma == "es":
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Nombre: " + verde + str(jugador))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " UUID: " + lrojo + "Ninguna")

                            elif idioma == "en":
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " Name: " + verde + str(jugador))
                                print(blanco + "    [" + verde + "+" + blanco + "]" + blanco + " UUID: " + lrojo + "None") 

                    except:
                        if idioma == "es":
                            print("\n" + blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Error de conexión.")

                        elif idioma == "en":
                            print("\n" + blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Connection error.")

                except:
                    if idioma == "es":
                        print("\n" + blanco + "    Usa: player [nombre]")
                        print("\n" + blanco + "    Para ver más informacion usa " + lcyan + "help-cmd player")

                    elif idioma == "en":
                        print("\n" + blanco + "    Usage: player [name]")
                        print("\n" + blanco + "    To see more information use " + lcyan + "help-cmd player")

            elif comando == "scan-ports": # Comando para escanear puertos de una IP
                try:
                    ip = argumento[1]
                    puertos = argumento[2]
                    mostrar = argumento[3].lower()
                    numservers = 0

                    if not mostrar == "y" and not mostrar == "n":
                        menu()

                    if puertos.lower() == "all":
                        puertos = "0-65535"

                    #if re.search(r".txt\b", ip):
                    #    print("archivo")
                    
                    try:
                        verificar_conexion()
                        try:
                            fecha = datetime.now()

                            archivo = "temp" + "_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt "

                            os.system("nmap -p " + str(puertos) + " -Pn -T5 -v -oN " + archivo + ip + " >nul")

                            carpeta_escaneos()

                            if os.path.isdir("escaneos/puertos"):
                                pass
                            else:
                                os.mkdir("escaneos/puertos")

                            fecha_archivos_datos_puerto = datetime.now()
                            archivo_datos_puerto = open("escaneos/puertos/Puerto_" + str(fecha_archivos_datos_puerto.day) + "-" + str(fecha_archivos_datos_puerto.month) + "-" + str(fecha_archivos_datos_puerto.year) + "_" + str(fecha_archivos_datos_puerto.hour) + "." + str(fecha_archivos_datos_puerto.minute) + "." + str(fecha_archivos_datos_puerto.second) + ".txt", "w", encoding="utf8")

                            archivo_datos_puerto.write("MCPTool @wrrulos \n\n")

                            if idioma == "es":
                                archivo_datos_puerto.write("Escaneo de Puertos \n\n")
                                archivo_datos_puerto.write("Información:\n\n")
                                archivo_datos_puerto.write("    Fecha: " + str(fecha_archivos_datos_puerto) + "-" + str(fecha_archivos_datos_puerto.month) + "-" + str(fecha_archivos_datos_puerto.year) + "\n")
                                archivo_datos_puerto.write("    Hora: " + str(fecha_archivos_datos_puerto.hour) + "." + str(fecha_archivos_datos_puerto.minute) + "." + str(fecha_archivos_datos_puerto.second) + "\n")
                                archivo_datos_puerto.write("    IP: " + str(ip) + "\n")
                                archivo_datos_puerto.write("    Puertos: " + str(puertos) + "\n")
                
                                if mostrar.lower() == "y":
                                    archivo_datos_puerto.write("    Mostrar servidores apagados: Si\n\n")
                                else:
                                    archivo_datos_puerto.write("    Mostrar servidores apagados: No\n\n")

                                archivo_datos_puerto.write("Servidores:\n\n")

                            elif idioma == "en":
                                archivo_datos_puerto.write("Port Scan \n\n")
                                archivo_datos_puerto.write("Information:\n\n")
                                archivo_datos_puerto.write("    Date: " + str(fecha_archivos_datos_puerto) + "-" + str(fecha_archivos_datos_puerto.month) + "-" + str(fecha_archivos_datos_puerto.year) + "\n")
                                archivo_datos_puerto.write("    Hour: " + str(fecha_archivos_datos_puerto.hour) + "." + str(fecha_archivos_datos_puerto.minute) + "." + str(fecha_archivos_datos_puerto.second) + "\n")
                                archivo_datos_puerto.write("    IP: " + str(ip) + "\n")
                                archivo_datos_puerto.write("    Ports: " + str(puertos) + "\n")
                
                                if mostrar.lower() == "y":
                                    archivo_datos_puerto.write("    Show shutdown servers: Yes\n\n")
                                else:
                                    archivo_datos_puerto.write("    Show shutdown servers: No\n\n")

                                archivo_datos_puerto.write("Servers:\n\n")

                            print("")

                            try:
                                archivo_temp = open(archivo , "r")

                                resultado_temp = archivo_temp.read()

                                archivo_temp.close()

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

                                            version = re.sub(r"§[a-zA-Z0-9]", "", datos[1].strip().replace("  ", "").replace("  ", ""))
                                            motd = re.sub(r"§[a-zA-Z0-9]", "", datos[2].strip().replace("  ", "").replace("  ", ""))
                                            jugadores = re.sub(r"§[a-zA-Z0-9]", "", f"{datos[3]}/{datos[4]}".strip().replace("  ", "").replace("  ", ""))

                                            if idioma == "es":
                                                numservers += 1
                                                print(blanco + "    [" + lverde + "√" + blanco + "] " + verde + "Servidor encontrado:")
                                                print("\n" + blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                                print(blanco + "        MOTD: " + lcyan + motd)
                                                print(blanco + "        Versión: " + lcyan + version)
                                                print(blanco + "        Jugadores: " + lcyan + jugadores + "\n")
                                                archivo_datos_puerto.write("[+] Servidor encontrado: \n\n")
                                                archivo_datos_puerto.write("    IP: " + str(ip) + ":" + str(puerto) + "\n")
                                                archivo_datos_puerto.write("    MOTD: " + str(motd) + "\n")
                                                archivo_datos_puerto.write("    Versión: " + str(version) + "\n")
                                                archivo_datos_puerto.write("    Jugadores: " + str(jugadores) + "\n\n")

                                            elif idioma == "en":
                                                numservers += 1                        
                                                print(blanco + "    [" + lverde + "√" + blanco + "] " + verde + "Server found:")
                                                print("\n" + blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                                print(blanco + "        MOTD: " + lcyan + motd)
                                                print(blanco + "        Versión: " + lcyan + version)
                                                print(blanco + "        Players: " + lcyan + jugadores + "\n")
                                                archivo_datos_puerto.write("[+] Server found: \n\n")
                                                archivo_datos_puerto.write("    IP: " + str(ip) + ":" + str(puerto) + "\n")
                                                archivo_datos_puerto.write("    MOTD: " + str(motd) + "\n")
                                                archivo_datos_puerto.write("    Version: " + str(version) + "\n")
                                                archivo_datos_puerto.write("    Players: " + str(jugadores) + "\n\n")

                                        except socket.timeout:
                                            if mostrar == "y":
                                                if idioma == "es":
                                                    print(blanco + "    [" + lrojo + "-" + blanco + "] " + verde + "Servidor encontrado " + rojo + "(tiempo agotado)" + verde + ":")
                                                    print("\n" + blanco + "        IP: " + lcyan + ip + ":" + puerto + "\n")
                                                    archivo_datos_puerto.write("[-] Servidor encontrado (Apagado)     IP: " + str(ip) +  ":" + str(puerto) + "\n\n")

                                                elif idioma == "en":                        
                                                    print(blanco + "    [" + lrojo + "-" + blanco + "] " + verde + "Server found: " + rojo + "(time out)" + verde + ":")
                                                    print("\n" + blanco + "        IP: " + lcyan + ip + ":" + puerto + "\n")
                                                    archivo_datos_puerto.write("[-] Server found (Offline)     IP: " + str(ip) +  ":" + str(puerto) + "\n\n")

                                        except:
                                            pass

                                if idioma == "es":
                                    if numservers == 1:
                                        print(blanco + "    El escaneo termino y se encontro " + verde + str(numservers) + blanco + " servidor.")

                                    elif numservers == 0:
                                        print(blanco + "    El escaneo termino y se encontraron " + lrojo + str(numservers) + blanco + " servidores.")

                                        if mostrar.lower() == "n":
                                            archivo_datos_puerto.write("No se encontraron servidores.")

                                    else:
                                        print(blanco + "    El escaneo termino y se encontraron " + verde + str(numservers) + blanco + " servidores.")

                                    print(blanco + "    Todos los datos del escaneo se guardaron en escaneos/puertos/Puerto" + "_" + str(fecha_archivos_datos_puerto.day) + "-" + str(fecha_archivos_datos_puerto.month) + "-" + str(fecha_archivos_datos_puerto.year) + "_" + str(fecha_archivos_datos_puerto.hour) + "." + str(fecha_archivos_datos_puerto.minute) + "." + str(fecha_archivos_datos_puerto.second) + ".txt" + reset)

                                elif idioma == "en":
                                    if numservers == 1:
                                        print(blanco + "    The scan ended and found " + verde + str(numservers) + blanco + " server.")

                                    elif numservers == 0:
                                        print(blanco + "    The scan ended and found " + lrojo + str(numservers) + blanco + " servers.")

                                        if mostrar.lower() == "n":
                                            archivo_datos_puerto.write("No servers found.")

                                    else:
                                        print(blanco + "    The scan ended and found " + verde + str(numservers) + blanco + " servers.")

                                    print(blanco + "    All scan data was saved in escaneos/puertos/Puerto" + "_" + str(fecha_archivos_datos_puerto.day) + "-" + str(fecha_archivos_datos_puerto.month) + "-" + str(fecha_archivos_datos_puerto.year) + "_" + str(fecha_archivos_datos_puerto.hour) + "." + str(fecha_archivos_datos_puerto.minute) + "." + str(fecha_archivos_datos_puerto.second) + ".txt" + reset)

                                archivo_datos_puerto.close()
                                os.remove(archivo)
                                print(reset)
                                
                            except Exception as error:
                                print("Error [2]" + str(error))

                        except Exception as error:
                            print("Error [1]" + str(error))

                    except:
                        if idioma == "es":
                            print("\n" + blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Error de conexión.")

                        elif idioma == "en":
                            print("\n" + blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Connection error.")

                except:
                    if idioma == "es":
                        print("\n" + blanco + "    Usa: scan-ports [ip] [puertos] [y/n]")
                        print("\n" + blanco + "    Para ver más informacion usa " + lcyan + "help-cmd scan-ports")

                    elif idioma == "en":
                        print("\n" + blanco + "    Usage: scan-ports [ip] [ports] [y/n]")
                        print("\n" + blanco + "    To see more information use " + lcyan + "help-cmd scan-ports")

            elif comando == "scan-range": # Comando para escanear un rango de IP 
                try:
                    ip = argumento[1]
                    rango = argumento[2]
                    puertos_rango = argumento[3].lower()
                    mostrar = argumento[4].lower()

                    numservers = 0

                    if not mostrar == "y" and not mostrar == "n":
                        menu() 

                    if puertos_rango == "all":
                        puertos_rango = "0-65535"

                    if rango == "*":
                        x = 0
                        y = 255
                        
                    else:
                        rango = rango.split("-")

                        x = rango[0]
                        y = rango[1]
                        x = int(x)
                        y = int(y)

                        if y >= 255:
                            y = 255

                    carpeta_escaneos()

                    if os.path.isdir("escaneos/rangos"):
                        pass

                    else:
                        os.mkdir("escaneos/rangos")

                    fecha_archivo_datos_rango = datetime.now()
                    archivo_datos_rango = open("escaneos/rangos/Rango_" + str(fecha_archivo_datos_rango.day) + "-" + str(fecha_archivo_datos_rango.month) + "-" + str(fecha_archivo_datos_rango.year) + "_" + str(fecha_archivo_datos_rango.hour) + "." + str(fecha_archivo_datos_rango.minute) + "." + str(fecha_archivo_datos_rango.second) + ".txt", "w", encoding="utf8")

                    archivo_datos_rango.write("MCPTool @wrrulos \n\n")

                    if idioma == "es":
                        archivo_datos_rango.write("Escaneo de Rango \n\n")
                        archivo_datos_rango.write("Información:\n\n")
                        archivo_datos_rango.write("    Fecha: " + str(fecha_archivo_datos_rango.day) + "-" + str(fecha_archivo_datos_rango.month) + "-" + str(fecha_archivo_datos_rango.year) + "\n")
                        archivo_datos_rango.write("    Hora: " + str(fecha_archivo_datos_rango.hour) + "." + str(fecha_archivo_datos_rango.minute) + "." + str(fecha_archivo_datos_rango.second) + "\n")
                        archivo_datos_rango.write("    IP: " + str(ip) + "\n")
                        archivo_datos_rango.write("    Rango: " + str(x) + "-" + str(y) + "\n")
                        archivo_datos_rango.write("    Puertos: " + str(puertos_rango) + "\n")

                        if mostrar.lower() == "y":
                            archivo_datos_rango.write("    Mostrar servidores apagados: Si\n\n")
                        else:
                            archivo_datos_rango.write("    Mostrar servidores apagados: No\n\n")

                        archivo_datos_rango.write("Servidores:\n\n")
                    
                    elif idioma == "en":
                        archivo_datos_rango.write("Range Scan \n\n")
                        archivo_datos_rango.write("Information:\n\n")
                        archivo_datos_rango.write("    Date: " + str(fecha_archivo_datos_rango.day) + "-" + str(fecha_archivo_datos_rango.month) + "-" + str(fecha_archivo_datos_rango.year) + "\n")
                        archivo_datos_rango.write("    Hour: " + str(fecha_archivo_datos_rango.hour) + "." + str(fecha_archivo_datos_rango.minute) + "." + str(fecha_archivo_datos_rango.second) + "\n")
                        archivo_datos_rango.write("    IP: " + str(ip) + "\n")
                        archivo_datos_rango.write("    Range: " + str(x) + "-" + str(y) + "\n")
                        archivo_datos_rango.write("    Ports: " + str(puertos_rango) + "\n")

                        if mostrar.lower() == "y":
                            archivo_datos_rango.write("    Show shutdown servers: Yes\n\n")
                        else:
                            archivo_datos_rango.write("    Show shutdown servers: No\n\n")

                        archivo_datos_rango.write("Servers:\n\n")

                    try:
                        verificar_conexion()
                        try:
                            print("")

                            while x <= y:
                                fecha = datetime.now()

                                archivo = "temp_range" + "_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt "

                                ip_range = str(ip) + "." + str(x)

                                if idioma == "es":
                                    print(lnegro + "    [" + lverde + "+" + lnegro + "]" + blanco + " Escaneando " + verde + ip_range)
                                
                                elif idioma == "en":
                                    print(lnegro + "    [" + lverde + "+" + lnegro + "]" + blanco + " Scanning " + verde + ip_range)

                                os.system("nmap -p " + str(puertos_rango) + " -Pn -T5 -oN " + archivo + str(ip) + "." + str(x) + " >nul")

                                try:
                                    archivo_temp_range = open(archivo, "r")

                                    resultado_temp_range = archivo_temp_range.read()

                                    archivo_temp_range.close()

                                    resultados = resultado_temp_range.split('Nmap scan report for ')

                                    for resultado in resultados:
                                        puertos = re.findall(r'([0-9]+)/tcp', resultado)

                                        for puerto in puertos:
                                            try:
                                                sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                                                sckt.settimeout(2);
                                                sckt.connect((ip_range, int(puerto)));
                                                sckt.send(b"\xfe\x01");
                                                datos = sckt.recv(1024)[3:].decode("utf-16be")[3:].split("\x00")
                                                sckt.close()

                                                version = re.sub(r"§[a-zA-Z0-9]", "", datos[1].strip().replace("  ", "").replace("  ", ""))
                                                motd = re.sub(r"§[a-zA-Z0-9]", "", datos[2].strip().replace("  ", "").replace("  ", ""))
                                                jugadores = re.sub(r"§[a-zA-Z0-9]", "", f"{datos[3]}/{datos[4]}".strip().replace("  ", "").replace("  ", ""))

                                                if idioma == "es":
                                                    numservers += 1
                                                    print("\n" + blanco + "    [" + lverde + "√" + blanco + "] " + verde + "Servidor encontrado:")
                                                    print("\n" + blanco + "        IP: " + lcyan + ip_range + ":" + puerto)
                                                    print(blanco + "        MOTD: " + lcyan + motd)
                                                    print(blanco + "        Versión: " + lcyan + version)
                                                    print(blanco + "        Jugadores: " + lcyan + jugadores + "\n")
                                                    archivo_datos_rango.write("[+] Servidor encontrado: \n\n")
                                                    archivo_datos_rango.write("    IP: " + str(ip_range) + ":" + str(puerto) + "\n")
                                                    archivo_datos_rango.write("    MOTD: " + str(motd) + "\n")
                                                    archivo_datos_rango.write("    Versión: " + str(version) + "\n")
                                                    archivo_datos_rango.write("    Jugadores: " + str(jugadores) + "\n\n")

                                                elif idioma == "en":
                                                    numservers += 1                  
                                                    print("\n" + blanco + "    [" + lverde + "√" + blanco + "] " + verde + "Server found:")
                                                    print("\n" + blanco + "        IP: " + lcyan + ip_range + ":" + puerto)
                                                    print(blanco + "        MOTD: " + lcyan + motd)
                                                    print(blanco + "        Versión: " + lcyan + version)
                                                    print(blanco + "        Players: " + lcyan + jugadores + "\n")
                                                    archivo_datos_rango.write("[+] Server found: \n\n")
                                                    archivo_datos_rango.write("    IP: " + str(ip_range) + ":" + str(puerto) + "\n")
                                                    archivo_datos_rango.write("    MOTD: " + str(motd) + "\n")
                                                    archivo_datos_rango.write("    Version: " + str(version) + "\n")
                                                    archivo_datos_rango.write("    Players: " + str(jugadores) + "\n\n")
                                                                                                   
                                            except socket.timeout:
                                                if mostrar.lower() == "y":
                                                    if idioma == "es":
                                                        print("\n" + blanco + "    [" + lrojo + "-" + blanco + "] " + verde + "Servidor encontrado " + rojo + "(tiempo agotado)" + verde + ":")
                                                        print("\n" + blanco + "        IP: " + lcyan + ip_range + ":" + puerto + "\n")
                                                        archivo_datos_rango.write("[-] Servidor encontrado (Apagado)     IP: " + str(ip_range) +  ":" + str(puerto) + "\n\n")

                                                    elif idioma == "en":                        
                                                        print("\n" + blanco + "    [" + lrojo + "-" + blanco + "] " + verde + "Servidor found: " + rojo + "(time out)" + verde + ":")
                                                        print("\n" + blanco + "        IP: " + lcyan + ip + ":" + puerto + "\n")
                                                        archivo_datos_rango.write("[-] Server found (Offline)     IP: " + str(ip_range) +  ":" + str(puerto) + "\n\n")

                                            except:
                                                pass

                                    os.remove(archivo)
                                    print(reset)
                                    
                                    x += 1

                                except Exception as error:
                                    print("Error [2]" + str(error))

                            if idioma == "es":
                                if numservers == 1:
                                    print(blanco + "    El escaneo termino y se encontro " + verde + str(numservers) + blanco + " servidor.")

                                elif numservers == 0:
                                    print(blanco + "    El escaneo termino y se encontraron " + verde + str(numservers) + blanco + " servidores.")

                                    if mostrar.lower() == "n":
                                        archivo_datos_rango.write("No se encontraron servidores.")
                                else:
                                    print(blanco + "    El escaneo termino y se encontraron " + verde + str(numservers) + blanco + " servidores.")

                                print(blanco + "    Todos los datos del escaneo se guardaron en escaneos/rangos/Rango" + "_" + str(fecha_archivo_datos_rango.day) + "-" + str(fecha_archivo_datos_rango.month) + "-" + str(fecha_archivo_datos_rango.year) + "_" + str(fecha_archivo_datos_rango.hour) + "." + str(fecha_archivo_datos_rango.minute) + "." + str(fecha_archivo_datos_rango.second) + ".txt" + reset)

                            elif idioma == "en":
                                if numservers == 1:
                                    print(blanco + "    The scan ended and found " + verde + str(numservers) + blanco + " server.")

                                elif numservers == 0:
                                    print(blanco + "    The scan ended and found " + verde + str(numservers) + blanco + " servers.")

                                    if mostrar.lower() == "n":
                                        archivo_datos_rango.write("No servers found.")
                                else:
                                    print(blanco + "    The scan ended and found " + verde + str(numservers) + blanco + " servers.")

                                print(blanco + "    All scan data was saved in escaneos/rangos/Rango" + "_" + str(fecha_archivo_datos_rango.day) + "-" + str(fecha_archivo_datos_rango.month) + "-" + str(fecha_archivo_datos_rango.year) + "_" + str(fecha_archivo_datos_rango.hour) + "." + str(fecha_archivo_datos_rango.minute) + "." + str(fecha_archivo_datos_rango.second) + ".txt" + reset)

                            archivo_datos_rango.close()

                        except Exception as error:
                            print("Error [1] " + str(error))

                    except:
                        if idioma == "es":
                            print("\n" + blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Error de conexión.")

                        elif idioma == "en":
                            print("\n" + blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Connection error.")
                except:
                    if idioma == "es":
                        print("\n" + blanco + "    Usa: scan-range [ip] [rango] [puertos] [y/n]")
                        print("\n" + blanco + "    Para ver más informacion usa " + lcyan + "help-cmd scan-range")

                    elif idioma == "en":
                        print("\n" + blanco + "    Usage: scan-range [ip] [range] [ports] [y/n]")
                        print("\n" + blanco + "    To see more information use " + lcyan + "help-cmd scan-range")

            elif comando == "scan-host": # Comando para escanear nodos de un host
                try:
                    host = argumento[1].lower()
                    puertos_host = argumento[2]
                    numservers = 0

                    if puertos_host.lower() == "all":
                        puertos_host = "0-65535"

                    if host == "minehost" or host == "vyxterhost" or host == "holyhosting":
                        pass

                    else:
                        print(ERROR_SCAN-HOST)

                    try:
                        verificar_conexion()
                        carpeta_escaneos()
                        carpeta_escaneos_host()

                        fecha = datetime.now()

                        if host == "minehost":
                            carpeta_host_minehost()
                            nodos = ("sv10", "sv11", "sv12", "sv13", "sv14", "sv15", "sv16", "sv17", "sv18")
                            dominio = ".minehost.com.ar"
                            archivo = "escaneos/host/minehost/minehost_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt"
                            archivo_nmap = "minehost_temp.txt"

                        elif host == "vyxterhost":
                            carpeta_host_vyxterhost()
                            nodos = ("free1", "free2", "usapay1", "usapay2", "usapay3", "usapay4", "usapay5", "usapay6" "usa1" , "usa2", "usa3", "usa4", "usa5", "usa6", "usa7", "usa8", "usa9", "usa10", "usa11", "usa12", "usa13", "usa14", "usa15", "usa16", "usa17", "usa18", "usa19", "usa20", "usa21", "usa22", "usa23", "usa24", "usa25", "usa26", "usa27", "usa28", "usa29", "usa30", "usa31", "usa32", "usa33", "usa34", "usa35")
                            dominio = ".vyxterhost.com"
                            archivo = "escaneos/host/vyxterhost/vyxterhost_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt"
                            archivo_nmap = "vyxterhost_temp.txt"

                        elif host == "holyhosting":
                            carpeta_host_holyhosting()
                            nodos = ("node-premium", "node-premium1", "node-premium2", "node-ashburn", "node-newyork", "node-valdivia", "node-dallas", "node-paris", "ca", "tx", "tx2", "fr")
                            dominio = ".holy.gg"
                            archivo = "escaneos/host/holyhosting/holyhosting_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt"
                            archivo_nmap = "holyhosting_temp.txt"           

                        archivo_nodos = "nodos_host_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt"
                        lista_nodos = open(archivo_nodos, "w", encoding="utf8")
                        lista_nodos.truncate(0)
                        archivo_escaneo_host = open(archivo, "w", encoding="utf8")

                        if idioma == "es":
                            archivo_escaneo_host.write("Escaneo de Host \n\n")
                            archivo_escaneo_host.write("Información: \n\n")
                            archivo_escaneo_host.write("    Fecha: " + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "\n")
                            archivo_escaneo_host.write("    Hora: " + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + "\n")
                            archivo_escaneo_host.write("    Host: " + str(host) + "\n\n")
                            archivo_escaneo_host.write("Nodos encontrados: \n\n")

                        elif idioma == "en":
                            archivo_escaneo_host.write("Host scan \n\n")
                            archivo_escaneo_host.write("Information: \n\n")
                            archivo_escaneo_host.write("    Date: " + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "\n")
                            archivo_escaneo_host.write("    Hour: " + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + "\n")
                            archivo_escaneo_host.write("    Host: " + str(host) + "\n\n")
                            archivo_escaneo_host.write("Found nodes: \n\n")

                        for nodo in nodos:
                            try:
                                ip = socket.gethostbyname(str(nodo) + str(dominio))     

                                lista_nodos.write("\n")
                                lista_nodos.write(str(ip) + "\n")
                                archivo_escaneo_host.write("Nodo: " + str(nodo) + str(dominio) + "    IP: " + str(ip) + "\n")
                            
                            except:
                                pass
                        
                        lista_nodos.close()
                        archivo_escaneo_host.write("\n")
                        lista_ip = open(archivo_nodos, "r")

                        for linea in lista_ip:
                            ip = lista_ip.readline()
                            ip = ip.replace("\n", "")

                            print("")

                            if idioma == "es":
                                print(lnegro + "    [" + lverde + "+" + lnegro + "]" + blanco + " Escaneando " + verde + str(ip))
                                
                            elif idioma == "en":
                                print(lnegro + "    [" + lverde + "+" + lnegro + "]" + blanco + " Scanning " + verde + str(ip))

                            os.system("nmap -p " + str(puertos_host) + " -T4 -v -oN " + archivo_nmap + " " + ip + " >nul")
                            print("")

                            escaneo_host = open(archivo_nmap, "r", encoding="utf8")
                            resultado_host = escaneo_host.read()
                            resultados = resultado_host.split('Nmap scan report for ')

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

                                        version = re.sub(r"§[a-zA-Z0-9]", "", datos[1].strip().replace("  ", "").replace("  ", ""))
                                        motd = re.sub(r"§[a-zA-Z0-9]", "", datos[2].strip().replace("  ", "").replace("  ", ""))
                                        jugadores = re.sub(r"§[a-zA-Z0-9]", "", f"{datos[3]}/{datos[4]}".strip().replace("  ", "").replace("  ", ""))

                                        if idioma == "es":
                                            numservers += 1
                                            print(blanco + "    [" + lverde + "√" + blanco + "] " + verde + "Servidor encontrado:")
                                            print("\n" + blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                            print(blanco + "        MOTD: " + lcyan + motd)
                                            print(blanco + "        Versión: " + lcyan + version)
                                            print(blanco + "        Jugadores: " + lcyan + jugadores + "\n")
                                            archivo_escaneo_host.write("[+] Servidor encontrado: \n\n")
                                            archivo_escaneo_host.write("    IP: " + str(ip) + ":" + str(puerto) + "\n")
                                            archivo_escaneo_host.write("    MOTD: " + str(motd) + "\n")
                                            archivo_escaneo_host.write("    Versión: " + str(version) + "\n")
                                            archivo_escaneo_host.write("    Jugadores: " + str(jugadores) + "\n\n")

                                        elif idioma == "en":
                                            numservers += 1
                                            print(blanco + "    [" + lverde + "√" + blanco + "] " + verde + "Server found:")
                                            print("\n" + blanco + "        IP: " + lcyan + ip + ":" + puerto)
                                            print(blanco + "        MOTD: " + lcyan + motd)
                                            print(blanco + "        Versión: " + lcyan + version)
                                            print(blanco + "        Players: " + lcyan + jugadores + "\n")
                                            archivo_escaneo_host.write("[+] Server found: \n\n")
                                            archivo_escaneo_host.write("    IP: " + str(ip) + ":" + str(puerto) + "\n")
                                            archivo_escaneo_host.write("    MOTD: " + str(motd) + "\n")
                                            archivo_escaneo_host.write("    Versión: " + str(version) + "\n")
                                            archivo_escaneo_host.write("    Players: " + str(jugadores) + "\n\n")
                                    
                                    except socket.timeout:
                                        if idioma == "es":
                                            print(blanco + "    [" + lrojo + "-" + blanco + "] " + verde + "Servidor encontrado " + rojo + "(tiempo agotado)" + verde + ":")
                                            print("\n" + blanco + "        IP: " + lcyan + ip + ":" + puerto + "\n")
                                            archivo_escaneo_host.write("[-] Servidor encontrado (Apagado)     IP: " + str(ip) +  ":" + str(puerto) + "\n\n")

                                        elif idioma == "en":
                                            print(blanco + "    [" + lrojo + "-" + blanco + "] " + verde + "Servidor found: " + rojo + "(time out)" + verde + ":")
                                            print("\n" + blanco + "        IP: " + lcyan + ip + ":" + puerto + "\n")
                                            archivo_escaneo_host.write("[-] Server found (Offline)     IP: " + str(ip) +  ":" + str(puerto) + "\n\n")

                                    except:
                                        pass   

                            escaneo_host.close()       

                        if idioma == "es":
                            if numservers == 1:
                                print(blanco + "\n    El escaneo termino y se encontro " + verde + str(numservers) + blanco + " servidor.")

                            elif numservers == 0:
                                print(blanco + "\n    El escaneo termino y se encontraron " + lrojo + str(numservers) + blanco + " servidores.")
                            
                            else:
                                print(blanco + "\n    El escaneo termino y se encontraron " + lverde + str(numservers) + blanco + " servidores.")

                            print(blanco + "    Los datos del escaneo se guardaron en escaneos/host/" + str(host) + "/" + str(host) + "_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt")

                        if idioma == "en":
                            if numservers == 1:
                                print(blanco + "\n    The scan ended and found " + verde + str(numservers) + blanco + " server.")

                            elif numservers == 0:
                                print(blanco + "\n    The scan ended and found " + lrojo + str(numservers) + blanco + " servers.")
                            
                            else:
                                print(blanco + "\n    The scan ended and found " + lverde + str(numservers) + blanco + " servers.")

                            print(blanco + "    All scan data was saved in escaneos/host/" + str(host) + "/" + str(host) + "_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt")

                        archivo_escaneo_host.close()
                        lista_ip.close()
                        os.remove(archivo_nodos)
                        os.remove(archivo_nmap)

                    except Exception as e:
                        print("Error [1] " + str(e))

                except:
                    if idioma == "es":
                        print("\n" + blanco + "    Usa: scan-host [host] [puertos] [y/n]")
                        print("\n" + blanco + "    Para ver más informacion usa " + lcyan + "help-cmd scan-host")

                    elif idioma == "en":
                        print("\n" + blanco + "    Usage: scan-host [host] [ports] [y/n]")
                        print("\n" + blanco + "    To see more information use " + lcyan + "help-cmd scan-host")


            elif comando == "scan-subd": # Comando para escanear subdominios de un dominio.
                try:
                    dominio = argumento[1]
                    archivo_subdominios = argumento[2].lower()
                    cantidad_lineas = 0

                    if archivo_subdominios == "default":
                        archivo_subdominios = "mcptool.txt"

                    ubicacion = "config/subdominios/" + archivo_subdominios
                        
                    try:
                        verificar_conexion()
                        try:
                            with open(ubicacion) as archivo:
                                for lineas in archivo:
                                    cantidad_lineas += 1

                            if idioma == "es":
                                print(blanco + "\n    [" + lverde + "+" + blanco + "]" + blanco + " Escaneando el dominio " + verde + dominio + "\n")
                                print(blanco + "    Archivo: " + archivo_subdominios + " (" + str(cantidad_lineas) + " subdominios)")
                            elif idioma == "en":
                                print(blanco + "\n    [" + lverde + "+" + blanco + "]" + blanco + " Scanning the domain " + verde + dominio + "\n")
                                print(blanco + "    File: " + archivo_subdominios + " (" + str(cantidad_lineas) + " subdomains)")

                            numsubd = 0
                            fecha = datetime.now()
                            carpeta_escaneos()
                            carpeta_subd()
                            lista_ips = []

                            archivo_datos_subd = open("escaneos/subdominios/Subdominio_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt", "w", encoding="utf8")
                            
                            print("")

                            if idioma == "es":
                                archivo_datos_subd.write("Escaneo de Subdominios \n\n")
                                archivo_datos_subd.write("Información:\n\n")
                                archivo_datos_subd.write("    Fecha: " + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "\n")
                                archivo_datos_subd.write("    Hora: " + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + "\n")
                                archivo_datos_subd.write("    Dominio: " + str(dominio) + "\n\n")

                                archivo_datos_subd.write("Subdominios encontrados: \n\n")

                            elif idioma == "en":
                                archivo_datos_subd.write("Subdomains Scan \n\n")
                                archivo_datos_subd.write("Information:\n\n")
                                archivo_datos_subd.write("    Date: " + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "\n")
                                archivo_datos_subd.write("    Hour: " + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + "\n")
                                archivo_datos_subd.write("    Domain: " + str(dominio) + "\n\n")

                                archivo_datos_subd.write("Subdomains found: \n\n")

                            with open(ubicacion) as lista_subdominios:
                                for linea in lista_subdominios:
                                    linea_subdominios = linea.split("\n")
                                    try:
                                        subdominio = str(linea_subdominios[0]) + "." + str(dominio)
                                        ip_subdominio = socket.gethostbyname(str(subdominio))
                                        if str(ip_subdominio) not in lista_ips:
                                            lista_ips.append(str(ip_subdominio))

                                            if idioma == "es":
                                                numsubd += 1
                                                print (blanco + "    [" + lverde + "√" + blanco + "]" + blanco + " Subdominio encontrado " + lnegro + "» " + verde + str(subdominio) + " " + lverde + str(ip_subdominio))
                                                archivo_datos_subd.write(str(subdominio) + " " + str(ip_subdominio) + "\n")
                                            elif idioma == "en":
                                                numsubd += 1
                                                print (blanco + "    [" + lverde + "√" + blanco + "]" + blanco + " Subdomain found " + lnegro + "» " + verde + str(subdominio) + " " + lverde + str(ip_subdominio))
                                                archivo_datos_subd.write(str(subddominio) + " " + str(ip_subdominio) + "\n")

                                    except:
                                        pass
          
                            if idioma == "es":
                                if numsubd == 1:
                                    print(blanco + "\n    El escaneo termino y se encontro " + verde + str(numsubd) + blanco + " subdominio.")

                                elif numsubd == 0:
                                    print(blanco + "\n    El escaneo termino y se encontraron " + lrojo + str(numsubd) + blanco + " subdominios.")
                            
                                else:
                                    print(blanco + "\n    El escaneo termino y se encontraron " + lverde + str(numsubd) + blanco + " subdominios.")

                                print(blanco + "    Todos los datos del escaneo se guardaron en escaneos/subdominios/Subdomino_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt" + reset)

                            elif idioma == "en":
                                if numsubd == 1:
                                    print(blanco + "\n    The scan ended and found " + verde + str(numsubd) + blanco + " subdomain.")

                                elif numsubd == 0:
                                    print(blanco + "\n    The scan ended and found " + lrojo + str(numsubd) + blanco + " subdomains.")
                            
                                else:
                                    print(blanco + "\n    The scan ended and found " + lverde + str(numsubd) + blanco + " subdomains.")

                                print(blanco + "    All scan data was saved in escaneos/subdominios/Subdomino_" + str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year) + "_" + str(fecha.hour) + "." + str(fecha.minute) + "." + str(fecha.second) + ".txt" + reset)

                            archivo_datos_subd.close()
                        
                        except:
                            if idioma == "es":
                                print("\n" + blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " No se encontro el archivo " + str(archivo_subdominios))

                            elif idioma == "en":
                                print("\n" + blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " The " + str(archivo_subdominios) + " file was not found")                      

                    except:
                        if idioma == "es":
                            print("\n" + blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Error de conexión.")

                        elif idioma == "en":
                            print("\n" + blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Connection error.")

                except:
                    if idioma == "es":
                        print("\n" + blanco + "    Usa: scan-subd [dominio] [archivo]")
                        print("\n" + blanco + "    Para ver más informacion usa " + lcyan + "help-cmd scan-subd")

                    elif idioma == "en":
                        print("\n" + blanco + "    Usage: scan-subd [domain] [file]")
                        print("\n" + blanco + "    To see more information use " + lcyan + "help-cmd scan-subd")

            elif comando == "bungee": # Comando para iniciar un bungee local 
                try:
                    ip = argumento[1]
                    try:
                        print("")

                        if idioma == "es":
                            print(blanco + "    [" + verde + "+" + blanco + "] " + lverde + "Iniciando proxy...")

                        elif idioma == "en":
                            print(blanco + "    [" + verde + "+" + blanco + "] " + lverde + "Starting proxy...")

                        archivo_config = open("config/bungee/config.txt", "r")
                        config_yml = archivo_config.read()
                        archivo_config.close()

                        archivo_config = open("config/bungee/config.yml", "w+")
                        archivo_config.truncate(0)
                        archivo_config.write(config_yml)
                        archivo_config.write("    address: " + str(ip) + "\n")
                        archivo_config.write("    restricted: false")
                        archivo_config.close()

                        os.system("cd config/bungee & start iniciar.bat")

                        time.sleep(10)

                        print("\n" + blanco + "    [" + verde + "√" + blanco + "]" + blanco + " IP: " + lverde + "0.0.0.0:25567")

                    except:
                        print("\n" + blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Error.")

                except:
                    if idioma == "es":
                        print("\n" + blanco + "    Usa: bungee [ip:puerto]")
                        print("\n" + blanco + "    Para ver más informacion usa " + lcyan + "help-cmd bungee")

                    elif idioma == "en":
                        print("\n" + blanco + "    Usage: bungee [ip:port]")
                        print("\n" + blanco + "    To see more information use " + lcyan + "help-cmd bungee")

            elif comando == "phishing": # Comando para crear un servidor falso y capturar contraseñas
                try:
                    servidor = argumento[1].lower()

                    if servidor == "mc.universocraft.com":
                        pass

                    else:
                        print(ERROR_PHISHING)

                    try:
                        verificar_conexion()
                        try:
                            if servidor == "mc.universocraft.com":
                                ruta_configplayers = "config/phishing/mc.universocraft.com/plugins/FakePlayers/config.yml"
                                ruta_datos_phishing = "config/phishing/mc.universocraft.com/datos.txt"
                                ruta_archivo_ipp = "config/phishing/mc.universocraft.com/ip_phishing.txt"
                                comando_iniciar_server = "cd config/phishing && cd mc.universocraft.com && start iniciar.bat"
                                comando_iniciar_consola = "cd config/phishing && cd mc.universocraft.com && start python consola.py"

                            try:  
                                respuesta = requests.get(urlmcsrv + servidor)
                                respuesta_json = respuesta.json()

                                jugadores_online = respuesta_json["players"]["online"]
                                jugadores_maximo = respuesta_json["players"]["max"]

                                archivo_configplayers = open(ruta_configplayers, "w+")
                                archivo_configplayers.truncate(0)
                                archivo_configplayers.write("Enabled: true \n")
                                archivo_configplayers.write("Add Real Players: true \n")
                                archivo_configplayers.write("Online Players: " + str(jugadores_online) + "\n")
                                archivo_configplayers.write("Max Players: " + str(jugadores_maximo))
                                archivo_configplayers.close()

                            except:
                                numaleatorio = randint(1000,8000)

                                archivo_configplayers = open(ruta_configplayers, "w+")
                                archivo_configplayers.truncate(0)
                                archivo_configplayers.write("Enabled: true \n")
                                archivo_configplayers.write("Add Real Players: true \n")
                                archivo_configplayers.write("Online Players: " + str(numaleatorio) + " \n")
                                archivo_configplayers.write("Max Players: 20000")
                                archivo_configplayers.close()

                            print("")

                            if idioma == "es":
                                print(blanco + "    [" + verde + "+" + blanco + "] " + lverde + "Iniciando servidor...\n")

                            elif idioma == "en":
                                print(blanco + "    [" + verde + "+" + blanco + "] " + lverde + "Starting server...\n")

                            os.system(comando_iniciar_server)
                            time.sleep(3)

                            if idioma == "es":
                                print(blanco + "    [" + verde + "+" + blanco + "] " + lverde + "Iniciando ngrok...")

                            elif idioma == "en":
                                print(blanco + "    [" + verde + "+" + blanco + "] " + lverde + "Starting ngrok...")
                                               
                            ngrok_segundo = open("taskkill.vbs", "w+")
                            ngrok_segundo.truncate(0)
                            ngrok_segundo.write('set objshell = createobject("wscript.shell")\nobjshell.run "taskkill /f /im ngrok.exe",vbhide')
                            ngrok_segundo.close()

                            os.system("start taskkill.vbs")

                            time.sleep(2)

                            ngrok_segundo = open("ngrok.vbs", "w+")
                            ngrok_segundo.truncate(0)
                            ngrok_segundo.write('set objshell = createobject("wscript.shell")\nobjshell.run "ngrok.exe tcp 25565",vbhide')
                            ngrok_segundo.close()

                            os.system("start ngrok.vbs")

                            time.sleep(2)

                            os.remove("ngrok.vbs")
                            os.remove("taskkill.vbs")

                            archivo_datos_phishing = open(ruta_datos_phishing, "w+")
                            archivo_datos_phishing.truncate(0)
                            archivo_datos_phishing.close()

                            url = "http://localhost:4040/api/tunnels"

                            respuesta = requests.get(url) 
                            respuesta_unicode = respuesta.content.decode("utf-8")
                            respuesta_json = json.loads(respuesta_unicode)
                            link = respuesta_json["tunnels"][0]["public_url"]
                            ipngrok = link.replace("tcp://", "")
                            ipngrok = ipngrok.split(":")
                            ipngrok2 = socket.gethostbyname(str(ipngrok[0]))
                            ip_phishing = ipngrok2 + ":" + ipngrok[1]

                            archivo_ipp = open(ruta_archivo_ipp, "w+")
                            archivo_ipp.truncate(0)
                            archivo_ipp.write(str(ip_phishing))
                            archivo_ipp.close()

                            time.sleep(3)

                            os.system(comando_iniciar_consola)

                            print("\n" + blanco + "    [" + verde + "IP" + blanco + "] " + lverde + str(ip_phishing))

                        except Exception as error:
                            print("Error [1]" + str(error))

                    except:
                        if idioma == "es":
                            print("\n" + blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Error de conexión.")

                        elif idioma == "en":
                            print("\n" + blanco + "    [" + rojo + "-" + blanco + "]" + lrojo + " Connection error.")

                except:
                    if idioma == "es":
                        print("\n" + blanco + "    Usa: phishing [server]")
                        print("\n" + blanco + "    Para ver más informacion usa " + lcyan + "help-cmd phishing")
                        print("\n\n" + blanco + "    Servidores disponibles: " + verde + "mc.universocraft.com")

                    elif idioma == "en":
                        print("\n" + blanco + "    Usage: phishing [server]")
                        print("\n" + blanco + "    To see more information use " + lcyan + "help-cmd phishing")
                        print("\n\n" + blanco + "    Available servers: " + verde + "mc.universocraft.com")
                 
            elif comando == "help-cmd": # Comando para ver ayuda especifica
                try:
                    cmd = argumento[1].lower()
                    try:
                        if cmd == "server":
                            if idioma == "es":
                                print(blanco + "\n    Comando:" + blanco + " server " + lrojo + "[ip]")
                                print("\n    " + lrojo + "[ip] " + lverde + "→ " + blanco + "IP del servidor")
                                print("\n    Ejemplo: server mc.universocraft.com")

                            elif idioma == "en":
                                print(blanco + "\n    Command:" + blanco + " server " + lrojo + "[ip]")
                                print("\n    " + lrojo + "[ip] " + lverde + "→ " + blanco + "Server IP")
                                print("\n    Example: server mc.universocraft.com")

                        elif cmd == "player":
                            if idioma == "es":
                                print(blanco + "\n    Comando:" + blanco + " player " + lrojo + "[nombre]")
                                print("\n    " + lrojo + "[nombre] " + lverde + "→ " + blanco + "Nombre del jugador")
                                print("\n    Ejemplo: player Rulo")

                            elif idioma == "en":
                                print(blanco + "\n    Command:" + blanco + " player " + lrojo + "[name]")
                                print("\n    " + lrojo + "[ip] " + lverde + "→ " + blanco + "Player name")
                                print("\n    Example: player Rulo")

                        elif cmd == "scan-ports":
                            if idioma == "es":
                                print(blanco + "\n    Comando:" + blanco + " scan-ports " + lrojo + "[ip] [puertos] [y/n]")
                                print("\n    " + lrojo + "[ip] " + lverde + "→ " + blanco + "IP del servidor")
                                print("    " + lrojo + "[puertos] " + lverde + "→ " + blanco + "Rango de puertos")
                                print("    " + lrojo + "[y/n] " + lverde + "→ " + blanco + "Mostrar servidores apagados (Y = Si y N = No)")
                                print("\n    Ejemplo: scan-ports 127.0.0.1 25000-26000 y")

                            elif idioma == "en":
                                print(blanco + "\n    Command:" + blanco + " scan-ports " + lrojo + "[ip] [puertos] [y/n]")
                                print("\n    " + lrojo + "[ip] " + lverde + "→ " + blanco + "Server IP")
                                print("    " + lrojo + "[puertos] " + lverde + "→ " + blanco + "Port range")
                                print("    " + lrojo + "[y/n] " + lverde + "→ " + blanco + "Show shutdown servers (Y = Yes y N = No)")
                                print("\n    Example: scan-ports 127.0.0.1 25000-26000 y")

                        elif cmd == "scan-range":
                            if idioma == "es":
                                print(blanco + "\n    Comando:" + blanco + " scan-range " + lrojo + "[ip] [rango] [puertos] [y/n]")
                                print("\n    " + lrojo + "[ip] " + lverde + "→ " + blanco + "IP del servidor (Ejemplo 127.0.0)")
                                print("    " + lrojo + "[rango] " + lverde + "→ " + blanco + "Rango de IP (Ejemplo 1-150 o *)")
                                print("    " + lrojo + "[puertos] " + lverde + "→ " + blanco + "Rango de puertos (Ejemplo 25000-26000)")
                                print("    " + lrojo + "[y/n] " + lverde + "→ " + blanco + "Mostrar servidores apagados (Y = Si y N = No)")
                                print("\n    Ejemplo: scan-range 54.24.104 1-255 25565 y")

                            elif idioma == "en":
                                print(blanco + "\n    Command:" + blanco + " scan-range " + lrojo + "[ip] [ports] [y/n]")
                                print("\n    " + lrojo + "[ip] " + lverde + "→ " + blanco + "Server IP (Example 127.0.0)")
                                print("    " + lrojo + "[range] " + lverde + "→ " + blanco + "IP range (Example 1-150 o *)")
                                print("    " + lrojo + "[ports] " + lverde + "→ " + blanco + "Port range (Example 25000-26000)")
                                print("    " + lrojo + "[y/n] " + lverde + "→ " + blanco + "Show shutdown servers (Y = Yes y N = No)")
                                print("\n    Example: scan-range 54.24.104 1-255 25565 y")

                        elif cmd == "scan-host":
                            if idioma == "es":
                                print(blanco + "\n    Comando:" + blanco + " scan-host " + lrojo + "[host] [puertos] [y/n]")
                                print("\n    " + lrojo + "[host] " + lverde + "→ " + blanco + "Nombre del host")
                                print("    " + lrojo + "[puertos] " + lverde + "→ " + blanco + "Rango de puertos")
                                print("    " + lrojo + "[y/n] " + lverde + "→ " + blanco + "Mostrar servidores apagados (Y = Si y N = No)")
                                print("\n    Ejemplo: scan-host holy.gg 25000-26000 y")

                            elif idioma == "en":
                                print(blanco + "\n    Command:" + blanco + " scan-host " + lrojo + "[host] [ports] [y/n]")
                                print("\n    " + lrojo + "[host] " + lverde + "→ " + blanco + "Host name")
                                print("    " + lrojo + "[ports] " + lverde + "→ " + blanco + "Port range")
                                print("    " + lrojo + "[y/n] " + lverde + "→ " + blanco + "Show shutdown servers (Y = Yes y N = No)")
                                print("\n    Example: scan-host holy.gg 25000-26000 y")

                        elif cmd == "scan-subd":
                            if idioma == "es":
                                print(blanco + "\n    Comando:" + blanco + " scan-subd " + lrojo + "[dominio] [archivo]")
                                print("\n    " + lrojo + "[dominio] " + lverde + "→ " + blanco + "Dominio")
                                print("    " + lrojo + "[archivo] " + lverde + "→ " + blanco + "Nombre del archivo que contiene la lista de subdominios")
                                print("\n    Ejemplo: scan-subd google.com mcptool.txt")

                            elif idioma == "en":
                                print(blanco + "\n    Command:" + blanco + " scan-subd " + lrojo + "[domain] [file]")
                                print("\n    " + lrojo + "[domain] " + lverde + "→ " + blanco + "domain")    
                                print("    " + lrojo + "[file] " + lverde + "→ " + blanco + "Name of the file that contains the list of subdomains")
                                print("\n    Example: scan-subd google.com mcptool.txt")

                        elif cmd == "bungee":
                            if idioma == "es":
                                print(blanco + "\n    Comando:" + blanco + " bungee " + lrojo + "[ip:puerto]")
                                print("\n    " + lrojo + "[ip:puerto] " + lverde + "→ " + blanco + "IP y puerto")
                                print("\n    Ejemplo: bungee 127.0.0.1:25567")

                            elif idioma == "en":
                                print(blanco + "\n    Command:" + blanco + " bungee " + lrojo + "[ip:port]")
                                print("\n    " + lrojo + "[ip:port] " + lverde + "→ " + blanco + "IP y puerto")
                                print("\n    Example: bungee 127.0.0.1:25567")
                    
                        elif cmd == "phishing":
                            if idioma == "es":
                                print(blanco + "\n    Comando:" + blanco + " phishing " + lrojo + "[server]")
                                print("\n    " + lrojo + "[server] " + lverde + "→ " + blanco + "Nombre del servidor")
                                print("\n    Ejemplo: phishing mc.universocraft.com")

                            elif idioma == "en":
                                print(blanco + "\n    Command:" + blanco + " phishing " + lrojo + "[server]")
                                print("\n    " + lrojo + "[server] " + lverde + "→ " + blanco + "Server name")
                                print("\n    Example: phishing mc.universocraft.com")
                        
                        elif cmd == "clear":
                            if idioma == "es":
                                print("\n    Limpia la pantalla.")

                            elif idioma == "en":
                                print("\n    Clean the screen.")

                        elif cmd == "help-cmd":
                            if idioma == "es":
                                print("\n    ...")

                            elif idioma == "en":
                                print("\n    ...")
            
                        elif cmd == "help":
                            if idioma == "es":
                                print("\n    Muestra los comandos disponibles.")

                            elif idioma == "en":
                                print("\n    Shows available commands.")

                        elif cmd == "set-language":
                            if idioma == "es":
                                print(blanco + "\n    Comando:" + blanco + " set-language " + lrojo + "[idioma]")
                                print("\n    " + lrojo + "[idioma] " + lverde + "→ " + blanco + "Idioma")
                                print("\n    Ejemplo: set-language en")

                            elif idioma == "en":
                                print(blanco + "\n    Command:" + blanco + " set-language " + lrojo + "[language]")
                                print("\n    " + lrojo + "[language] " + lverde + "→ " + blanco + "Language")
                                print("\n    Example: set-language es")
                        
                        else:
                            if idioma == "es":
                                print("\n" + blanco + "    Usa: help-cmd [comando]")

                            elif idioma == "en":
                                print("\n" + blanco + "    Usage: help-cmd [command]")                         
                        
                    except:
                        if idioma == "es":
                            print("\n" + blanco + "    Usa: help-cmd [comando]")

                        elif idioma == "en":
                            print("\n" + blanco + "    Usage: help-cmd [command]")
                except:
                    if idioma == "es":
                        print("\n" + blanco + "    Usa: help-cmd [comando]")

                    elif idioma == "en":
                        print("\n" + blanco + "    Usage: help-cmd [command]")           

            elif comando == "set-language": # Comando para cambiar el idioma
                try:
                    idiomacmd = argumento[1].lower()

                    if idiomacmd == "es" or idiomacmd == "en":
                        pass

                    else:
                        print(ERROR_IDIOMAS)

                    try:
                        if idiomacmd == "es":
                            archivo_idioma_cmd = open("datos/idioma", "w+")
                            archivo_idioma_cmd.truncate(0)
                            archivo_idioma_cmd.write("es")
                            archivo_idioma_cmd.close()

                            print("\n" + blanco + "    [" + verde + "+" + blanco + "] " + lverde + "El idioma fue cambiado a Español.")

                        elif idiomacmd == "en":
                            archivo_idioma_cmd = open("datos/idioma", "w+")
                            archivo_idioma_cmd.truncate(0)
                            archivo_idioma_cmd.write("en")
                            archivo_idioma_cmd.close()

                            print("\n" + blanco + "    [" + verde + "+" + blanco + "] " + lverde + "The language was changed to English.")

                    except Exception as error:
                        print("Error [1]" + str(error))

                except:
                    if idioma == "es":
                        print("\n" + blanco + "    Usa: set-language [idioma]")
                        print("\n" + blanco + "    Para ver más informacion usa " + lcyan + "help-cmd set-language")
                        print("\n\n" + blanco + "    Idiomas disponibles: " + verde + "es" + lnegro + " - " + verde + "en")

                    elif idioma == "en":
                        print("\n" + blanco + "    Usage: set-language [language]")
                        print("\n" + blanco + "    To see more information use " + lcyan + "help-cmd set-language")
                        print("\n\n" + blanco + "    Languages available: " + verde + "es" + lnegro + " - " + verde + "en")
                                               
            else:
                if idioma == "es":
                    print("\n" + lnegro + "    [" + rojo + "-" + lnegro + "]" + lrojo + " Comando desconocido. Escribe help para ver los comandos disponibles.")

                elif idioma == "en":
                    print("\n" + lnegro + "    [" + rojo + "-" + lnegro + "]" + lrojo + " Unknown command. Type help to see the available commands.")       

        except:
            if idioma == "es":
                print("\n" + lnegro + "    [" + rojo + "-" + lnegro + "]" + lrojo + " Comando desconocido. Escribe help para ver los comandos disponibles.")

            elif idioma == "en":
                print("\n" + lnegro + "    [" + rojo + "-" + lnegro + "]" + lrojo + " Unknown command. Type help to see the available commands.")

verificar_nmap()
verificar_so()
menu()
