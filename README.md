# 🧨  MCPTool v1.0

<h3> Herramienta de pentesting para Minecraft </h3>
<br/>
</br>
<p align="center">
<img src="https://github.com/wrrulos/Imagenes-Github/blob/main/MCPTool/MCPTool.png" title="MCPTool">
</p>
<br/>

# 🛠 Caracteristicas

* Ver informacion de un servidor
* Ver informacion de un jugador
* Escaneo de puertos
* Escaneo de rango
* Escaneo de nodos de un hosting
* Escaneo de subdominios
* Crear un bungee local
* Crear un servidor falso (phishing)
* La herramienta cuenta con su version en Español y Ingles

## 💻 Sistemas Operativos compatibles:

* ✅ Windows (8, 8.1 y 10)
* ❌ Linux

# 🔧 Instalación 

* Instalar Nmap
* Instalar Python 3.
* Crear una cuenta en https://ngrok.com/
* Descargar Ngrok y conectar tu cuenta con el token.
* Mover ngrok.exe a la carpeta de MCPTool.
* Ejecutar Dependencias.bat para instalar las dependencias.

# 🕹 Ejecutar

* Ejecutar MCPTool.py 

## 📸 Screenshots

<img src="https://github.com/wrrulos/MCPTool/blob/main/images/Help.PNG">

## 📝 Guia de comandos

```bash
[*] server (Muestra información de un servidor)
$ server [ip]

# [ip] IP del servidor

$ Ejemplo: server mc.universocraft.com

[*] player (Muestra informacion de un jugador)
$ player [nombre]

# [nombre] Nombre del jugador

$ Ejemplo: player Rulo

[*] scan-ports (Escanea los puertos de una IP)
$ scan-ports [ip] [puertos] [y/n]

# [ip] IP del servidor
# [puertos] Rango de puertos
# [y/n] Mostrar servidores apagados (Y = Si y N = No)

$ Ejemplo: scan-ports 127.0.0.1 25000-26000 y

[*] scan-range (Escanea el rango de una IP)
$ scan-range [ip] [rango] [puertos]

# [ip] IP del servidor
# [rango] Rango de IP
# [puertos] Rango de puertos

$ Ejemplo: scan-range 127.0.0 1-255 25565 y

[*] scan-host (Escanea los nodos de un host)
$ scan-host [host] [puertos] [y/n]

# [host] Nombre del host
# [puertos] Rango de puertos 
# [y/n] Mostrar servidores apagados (Y = Si y N = No)

$ Ejemplo: scan-host holy.gg 25000-26000 y

[*] scan-subd (Escanea los subdominios de un dominio)
$ scan-subd [dominio] [archivo]

# [dominio] Dominio
# [archivo] Nombre del archivo que contiene la lista de subdominios // NOTA: Puedes agregar una lista personalizada en /config/subdominios

$ Ejemplo: scan-subd google.com mcptool.txt

[*] bungee (Crea un bungee local)
$ bungee [ip:port]

# [ip:port] IP y puerto

$ Ejemplo: bungee 127.0.0.1:25567

[*] phishing (Crea un servidor falso para capturar contraseñas)
$ phishing [server]

# [server] Nombre del servidor

$ Ejemplo: phishing mc.universocraft.com

[*] set-language (Cambia el idioma de la herramienta)
$ set-language [idioma]

# [idioma] Idioma

$ Ejemplo: set-language en

[*] clear (Limpia la pantalla de la herramienta)
$ clear

[*] help-cmd (Muestra ayuda especifica sobre un comando)
$ help-cmd [comando]

# [comando] Comando

$ Ejemplo: help-cmd scan-ports

[*] help (Muestra la lista de comandos)
$ help
```

## 🎞 Video 

<p> No disponible.</p>

## Licencia 

MIT License

Copyright (c) 2020 Pedro Vega

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

 
