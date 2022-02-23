# 🧨  MCPTool v2.2

<h3> Pentesting tool for Minecraft </h3>
<br/>
</br>
<p align="center">
<img src="https://github.com/wrrulos/Imagenes-Github/blob/main/MCPTool/Logo.png" title="MCPTool">
</p>

### This project was created for educational purposes and should not be used in environments without legal authorization.

# 🛠 Features

* See information of a server
* View player information
* Port scanning
* QuboScanner
* Scanning of nodes of a hosting
* Create a local bungee
* Listening command
* Checker
* Show mods on this server.
* MITM Attack (poisoning)

## 💻 Supported operating systems:

* ✅ Windows (8, 8.1, 10 and 11)
* ✅ Linux

# 🔧 Installation 

```bash
# Install Nmap (https://nmap.org/)
# Install Python 3 (https://www.python.org/)
# Install NodeJS (https://nodejs.org/es/)

# Clone the repository (Or download it from the web in the "Code button and download zip")
$ git clone https://github.com/wrrulos/MCPTool

# Go into the MCPTool folder
$ cd MCPTool

# Create an ngrok account (https://ngrok.com/)
# Download Ngrok and connect your account with the token.
# Move ngrok to the MCPTool folder.

# Install the requirements
$ python3 -m pip install -r requirements.txt
$ npm install mineflayer
$ npm install process

```

# 🕹 Usage

```bash
$ python3 MCPTool.py
```

## 📝 Commands guide

```bash

[*] server 
Shows information of the specified server

$ server [ip]

# [ip] Server IP

$ Example: server mc.universocraft.com


[*] player 
Shows information of the specified player

$ player [name]

# [name] Player name

$ Example: player Rulo


[*] scan
Scan the ports of the specified IP (You can also scan an IP range)

$ scan [ip] [ports] 

# [ip] IP
# [ports] Port range

$ Example: scan 127.0.0.1 25000-26000


[*] qubo
Scan the ports of the specified IP using quboscanner (You can also scan a range of IPs)

$ qubo [ip] [ports] [th] [ti]

# [ip] IP
# [ports] Port range
# [th] Threads
# [ti] Timeout

$ Example: qubo 127.0.0.1 25000-26000 500 1500


[*] host 
This command scans all nodes of the specified hosting.
$ host [host] [ports] 

# [host] Host name
# [ports] Port range

$ Example: host holyhosting 25000-26000
  
  
[*] mods
This command displays the mods on a Forge server.

$ mods [ip:port]

# [ip:port] IP and port

$ Example: mods 127.0.0.1:25567


[*] checker
This command scans the servers found in a file

$ checker [file]

# [file] File location

$ Example: checker C:\Users\Rulo\Documents\Scan.txt


[*] bot [ip:port]
Check if the server can be entered using a bot

# [ip:port] IP and port

$ Example: bot mc.ecuacraft.com


[*] bungee 
Create a local bungee.

$ bungee [ip:port]

# [ip:port] IP and port

$ Example: bungee 127.0.0.1:25567

NOTE: The Bungeecord comes with my RBungeeExploit plugin which has the following commands:

  - /connect [ip:port] This command sends you to the specified server
  - /set-uuid [uuid] This command changes your UUID to the specified uuid.  
  
  
[*] listening
This command shows the players connected within the server

$ listening [ip:port]

# [ip:port] IP and port

$ Example: listening 127.0.0.1:25567

  
  
[*] poisoning 
Create a proxy connection that redirects to a server and captures commands. (Only works with non-premium users)

$ poisoning [ip]

# [ip] Server IP

$ Example: poisoning mc.universocraft.com


[*] clear (Clears the tool screen)
$ clear

[*] help (Show command list)
$ help
```

## 📸 Screenshots

<img src="https://github.com/wrrulos/Imagenes-Github/blob/main/MCPTool/Load.png">
<img src="https://github.com/wrrulos/Imagenes-Github/blob/main/MCPTool/Banner.png">
<img src="https://github.com/wrrulos/Imagenes-Github/blob/main/MCPTool/Help.png">

## 🎞 Video 
[![Watch the video](https://github.com/wrrulos/Imagenes-Github/blob/main/MCPTool/Load.png)](https://youtu.be/WW_LVJOBltc)

## Licencia 

MIT License

Copyright (c) 2021 Pedro Vega

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

 
