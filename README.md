# 🧨  MCPTool v1.1

<h3> Pentesting tool for Minecraft </h3>
<br/>
</br>
<p align="center">
<img src="https://github.com/wrrulos/Imagenes-Github/blob/main/MCPTool/MCPTool.png" title="MCPTool">
</p>
<br/>

# 🛠 Features

* See information of a server
* View player information
* Port scanning
* Range scan
* Scanning of nodes of a hosting
* Subdomain scan
* Create a local bungee
* Create a fake server (phishing)

## 💻 Supported operating systems:

* ✅ Windows (8, 8.1, 10 and 11)
* ✅ Linux

# 🔧 Installation 

* Install Nmap
* Install Python 3.
* Create an account at https://ngrok.com/
* Download Ngrok and connect your account with the token.
* Move ngrok to the MCPTool folder.
* Run MCPTool.py

# 🕹 Run

* Run MCPTool.py 

## 📸 Screenshots

<img src="https://github.com/wrrulos/Imagenes-Github/blob/main/MCPTool/1.PNG.jpg">
<img src="https://github.com/wrrulos/Imagenes-Github/blob/main/MCPTool/2.PNG.jpg">
<img src="https://github.com/wrrulos/Imagenes-Github/blob/main/MCPTool/3.PNG.jpg">

## 📝 Commands guide

```bash
[*] server (Shows information about a server)
$ server [ip]

# [ip] server IP

$ Example: server mc.universocraft.com

[*] player (Shows information about a player)
$ player [name]

# [name] Player name

$ Example: player Rulo

[*] scan-ports
$ scan-ports [ip] [ports] [y / n]

# [ip] server IP
# [ports] Port range
# [y / n] Show shutdown servers (Y = Yes and N = No)

$ Example: scan-ports 127.0.0.1 25000-26000 y

[*] scan-range (Scans the range of an IP)
$ scan-range [ip] [range] [ports] [y / n]

# [ip] server IP
# [range] IP range
# [ports] Port range
# [y / n] Show shutdown servers (Y = Yes and N = No)

$ Example: scan-range 127.0.0 1-255 25565 y

[*] scan-host (Scans the nodes of a host)
$ scan-host [host] [ports] [y / n]

# [host] Host name
# [ports] Port range
# [y / n] Show shutdown servers (Y = Yes and N = No)

$ Example: scan-host holy.gg 25000-26000 y
[*] scan-subd (Scans the subdomains of a domain)
$ scan-subd [domain] [file]

# [domain] Domain
# [file] Name of the file that contains the list of subdomains // NOTE: You can add a custom list in / config / subdomains

$ Example: scan-subd google.com mcptool.txt

[*] bungee (Create a local bungee)
$ bungee [ip: port]

# [ip: port] IP and port

$ Example: bungee 127.0.0.1:25567

[*] phishing (Create a fake server to capture passwords)
$ phishing [server]

# [server] Server name

$ Example: phishing mc.universocraft.com

[*] clear (Clears the tool screen)
$ clear

[*] help (Show command list)
$ help
```

## 🎞 Video 
[![Watch the video](https://youtu.be/)](https://youtu.be/9m7KNd9EHBI)

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

 
