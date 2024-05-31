# Complete guide on MCPTool commands

List of current MCPTool commands.

- [Server](#server)
- [Uuid](#uuid)
- [IPInfo](#ipinfo)
- [DNSLookup](#dnslookup)
- [Subdomains](#subdomains)
- [Scan](#scan)
- [Listening](#listening)
- [FakeProxy](#fakeproxy)
- [Resolver](#resolver)
- [BruteAuth](#bruteauth)
- [SendCMD](#sendcmd)
- [Kick](#kick)
- [KickAll](#kickall)
- [BruteRcon](#brutercon)
- [Checker](#checker)
- [Connect](#connect)
- [Rcon](#rcon)

- [Discord](#discord)

## Server
The **server** command allows you to obtain information about a Minecraft server. Works on Java and Bedrock servers.

![Server](../img/commands/server.png)

To use this command you must enter:
</br>
`server <ip:port/domain>`

## Uuid
The **uuid** command allows you to get the uuids of a Minecraft user or premium user using their uuid

![Uuid1](../img/commands/uuid_1.png)
![Uuid2](../img/commands/uuid_2.png)


To use this command you must enter:
</br>
`uuid <username>`

## IPInfo
The **ipinfo** command allows you to obtain information about an IP address.

![IPInfo](../img/commands/ipinfo.png)

To use this command you must enter:
</br>
`ipinfo <ip>`

## DNSLookup
The **dnslookup** command allows you to obtain the DNS records for a specific domain.

![DnsLookup](../img/commands/dnslookup.png)

To use this command you must enter:
</br>
`dnslookup <domain>`

## Scan
The **scan** command allows you to perform a scan to look for open ports hosting Minecraft servers.

### **IP Range**
You can enter a normal IP like **127.0.0.1**.

But you can also enter an IP range, such as: **127.0.0.1-255**

Valid formats for IP ranges vary depending on the type of scanner you select.

### **Port Range**
You can enter a normal port like **25565**.

But you can also enter a variety of ports, such as: **25560-25570**

Valid formats for port ranges vary depending on the type of scanner you select.

### **Scanner**.
You can perform the scan using different scanners, this is specified in the **method** argument

List of methods:

- Nmap (nmap)
- Quboscanner (qubo)
- Masscan (masscan)
- Python Sockets (py)

In the **method** argument you can enter the name of the scanner or its respective number.

![Scan](../img/commands/scan.png)

To use this command you must enter:
</br>
`scan <ip> <ports> <method>`

## Subdomains
The **subdomains** command allows you to get the subdomains of a domain.

![Subdomains](../img/commands/subdomains.png)

To use this command you must enter:
</br>
`subdomains <domain> <subdomainsFile>`

## Checker
The **checker** command allows you to obtain the current data from the servers located in a specific text file.

![Checker](../img/commands/checker.png)

To use this command you must enter:
</b>
`checker <file>`

## Listening
The **listening** command allows you to get the list of players connecting to the server, along with their uuids.

![Listening](../img/commands/listening.png)

To use this command you must enter:
</br>
`listening <ip:port>`

## Resolver
The **resolver** command allows you to obtain IP addresses and subdomains linked to the specified domain.

![Resolver](../img/commands/resolver.png)

To use this command you must enter:
</br>
`resolver <domain>`

## Proxy
The **proxy** command creates a proxy server that redirects to the specified server.

### Waterfall Mode:
The proxy server comes with my *RBungeeExploit* plugin by default. This plugin allows you to run the following commands:

- /set-uuid -> Change your uuid.
- /connect -> Connects you to the specified server.

![Waterfall](../img/commands/waterfall_1.png)
</br>
![Waterfall2](../img/commands/waterfall_2.png)
</br>
![Waterfall3](../img/commands/waterfall_3.png)

### Velocity Mode:
The proxy server comes with my *MCPTool* plugin by default. This plugin allows you to run the following commands:

- /username -> Change your username.
- /uuid -> Change your uuid.
- /connect -> Connects you to the specified server.

![Velocity1](../img/commands/velocity_1.png)
</br>
![Velocity2](../img/commands/velocity_2.png)
</br>
![Velocity3](../img/commands/velocity_3.png)
</br>
![Velocity4](../img/commands/velocity_4.png)


To use this command you must enter:
</br>
`proxy <ip:port> <proxy-type>`

## Fake proxy
The **fakeproxy** command creates a speed proxy server that redirects to the specified server and captures all data. The data it saves is:

- Date and time of entry and exit of users.
- Username and IP address.
- Commands and messages sent.

In addition to saving data, it also allows you to interact with proxy users using commands.

![FakeProxy](../img/commands/fakeproxy.png)
![FakeProxyServers](../img/commands/fakeproxy_server.png)
![FakeProxyPlugin](../img/commands/fakeproxy_commands.png)

To use this command you must enter:
</br>
`fakeproxy <ip:port> <forwarding-mode>`

### **IMPORTANT** - By default, it only creates a local proxy; to expose your port you can use services like [ngrok](https://ngrok.com/).

## Connect
The **connect** command allows you to connect to a Minecraft server using the terminal.

![Connect](../img/commands/connect.png)

To use this command you must enter:
</br>
`connect <ip:port> <version> <user>`

## Rcon
The **rcon** command allows you to connect to a Minecraft server using rcon (only if enabled).

![Rcon](../img/commands/rcon.png)

To use this command you must enter:
</br>
`rcon <ip:rconPort> <rconPassword>`

## BruteRcon
The **brutercon ** command allows you to perform a brute force attack on the rcon port of the specified server to attempt to guess the password.

To use this command you must enter:
</br>
`rconbrute <ip:rconPort> <passwordFile>`

## Bruteauth
The **Bruteauth** command allows you to perform a brute force attack on a Minecraft user within a non-premium server to try to guess their password. (/login)

**IMPORTANT!** I will give you a brief summary of how the bot works:

* When the bot connects to the server, it listens for any of the messages found in the **bruteforce_config** (*wordsToLogin*) configuration file. </br></br> After reading any of the words in that list, the bot runs the command to authenticate itself and then listens again, until it reads some of the words in (*wordsAtLogin*)

[!] If the bot doesn't try any passwords or if after trying one it doesn't do anything else, it's because you need to add more words to the corresponding lists.

To use this command you must enter:
</br>
`bruteauth <ip:port> <version> <username> <passwordFile>`

## Kick
The **kick** command allows you to connect a bot with a specific name. This is to disconnect you in case the server kicks players who log in from another location.

To use this command you must enter:
</br>
`kick <ip:port> <version> <username> <loop>`

**NOTE** In loop you must enter *y* or *n*.

## KickAll
The **kickall** command allows you to connect bots with the name of each player found on the server. This is to disconnect them in case the server kicks players who log in from another location.

To use this command you must enter:
</br>
`kickall <ip:port> <version> <loop>`

**NOTE** In loop you must enter *y* or *n*.

## SendCMD
The **sendcmd** command allows you to connect a bot that will send a list of messages or commands found in the specified text file.

To use this command you must enter:
</br>
`sendcmd <ip:port> <version> <username> <file>`

## Language
The **language** command allows you to change the language of the tool.

List of available languages:

- English (**en**)
- Turkish (**tr**)

You must specify the language abbreviation, for example **es**.

To use this command you must enter:
</br>
`language <language>`

## Discord
The **discord** command shows the link for my discord server.

To use this command you must enter:
</br>
`discord`
