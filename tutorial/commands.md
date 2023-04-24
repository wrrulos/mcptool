
# Command Guide | MCPTool

- [Commands](#commands)
   - [Authme](#authme)
   - [Bungee](#bungee)
   - [Checker](#checker)
   - [Connect](#Connect)
   - [Discord](#Discord)
   - [Dnslookup](#dnslookup)
   - [Host](#host)
   - [IPInfo](#ipinfo)
   - [kick](#kick)
   - [kickall](#kickall)
   - [Language](#language)
   - [listening](#listening)
   - [Player](#player)
   - [poisoning](#poisoning)
   - [rcon](#rcon)
   - [rconnect](#rconnect)
   - [scan](#scan)
   - [search](#search)
   - [sendcmd](#sendcmd)
   - [server](#server)

# Commands

Thats a list with all the commands that MCPTool has. 
Parameters syntaxis:
`<paramenter> - <type> - <what it does>`


## Authme

This command allows you to ForceBrute a login plugin. 
Usage: `authme <ip:port> <wordlist> [proxy]`

Parameters:
 - `ip:port - string - the IP from the server` 
 - `wordlist - string - the wordlist. For example, rockyou.txt`
 - `proxy - float - a proxy to join the bot socks5`
## Bungee

With the bungee command you can create a proxy that connects to a direct ip 
Usage: `bungee <ip:port>`

Parameters:
 - `ip:port - string - the IP from the server` 
 
###   In-game commands:
   - `/set-uuid <uuid> - changes your UUID`
   - `/connect <ip:port> - connects you to a server`

## Checker

Mass check servers status in a file
Usage: `checker <file> <bot> [proxy]`

Parameters:
  - `file - string - the file with the servers`
  - `bot - boolean - value that decides whether to send a bot or not`
  - `proxy - float - a proxy to join the bot socks5`

## Connect

Mass check servers starus in a file
Usage: `checker <file> <bot> [proxy]`

Parameters:
  - `ip:port - string - the IP from the server` 
  - `username - string - the username`
  - `protocol - integer - the Ninecraft protocol version. Search in google for more info`

## Discord

Shows the Discord. You need a description for that?
Usage: `discord`

## Dnslookup

Get the dns records of the domain
Usage: `dnslookup <domain>`

Parameters:
  - `domain - string - the server domain (should be a cname)` 

## Host

Host's command allows you to scan nodes from a hosting
Usage: `host <hostname> <ports> <method> <bot> [proxy]`

Parameters:
 - `hostname- string - the hostname` 
 - `port - string - a number array? example: "1-65535" will scan from port 1 to port 65535`
 - `method - string - it can be or "nmap" or "quboscanner" ("quboscanner" is recommended)`
 - `bot - boolean - value that decides whether to send a bot or not`  
 - `proxy - float - a proxy to join the bot socks5`

## IPInfo

It shows info about an IP
Usage: `ipinfo <ip>`

Parameters:
  - `ip - string - the IP` 

## kick

Kicks the player (dosn't works in Bungecord)
Usage: `kick <ip:port> <protocol> <user> <loop> [proxy]`

Parameters:
 - `ip:port - string - the IP from the server` 
 - `protocol - integer - the Ninecraft protocol version. Search in google for more info`
 - `user - string - the user that you want to kick`
 - `loop - boolean - if you want to kick the player in loop`
 - `proxy - float - a proxy to join the bot socks5`
 - 
## kickall

Kicks all the players (dosn't works in Bungecord)
Usage: `kick <ip:port> <protocol> <loop> [proxy]`

Parameters:
 - `ip:port - string - the IP from the server` 
 - `protocol - integer - the Ninecraft protocol version. Search in google for more info`
 - `loop - boolean - if you want to kick the player in loop`
 - `proxy - float - a proxy to join the bot socks5`

## language

Changes MCPTool's language
Usage: `language <language>`

Parameters:
 - `ip:port - string - "spanish" or "english"` 

## listening

Save all players that joins/leaves the server
Usage: `listening <ip:port/domain>`

Parameters:
 - `ip:port/domain - string - the ip or the domain` 

## Player

Gets the information from the specified player
Usage: `player <username>`

Parameters:
 - `username - string - the users username` 


## Poisoning

Creates a bait server (Like phishing but in minecraft) and opens it using ngrok
Usage: `poisoning <ip:port/domain>`

Parameters:
 - `ip:port/domain - string - the ip or the domain to copy` 


## rcon

Forcebrutes a rcon server
Usage: `rcon <ip:port> <wordlist> [delay]`

Parameters:
 - `ip:port - string - the IP from the server` 
 - `wordlist - string - the wordlist. For example, rockyou.txt`
 - `delay - integer/float - the delay between every password`


## rconnect

This command connects to the RCON port of a server and allows you to enter commands
Usage: `rcon <ip:port> <password>`

Parameters:
 - `ip:port - string - the IP from the server` 
 - `password - string - the rcon server password. If you don't know it you can use "rcon" command`


## scan

This command allows you to ForceBrute a login plugin. 
Usage: `scan <ip> <ports> <method> <bot> [proxy]`

Parameters:
 - `hostname- string - the hostname` 
 - `port - string - a number array? example: "1-65535" will scan from port 1 to port 65535`
 - `method - string - it can be or "nmap" or "quboscanner" ("quboscanner" is recommended)`
 - `bot - boolean - value that decides whether to send a bot or not`  
 - `proxy - float - a proxy to join the bot socks5`

## search

Use the Shodan search engine to search for IP addresses that have port 25565 open and then check if they are from Minecraft, to finally show it on the screen.
Usage: `search [data]`

Parameters:
 - `data - string - data that will be used for search servers` 


## sendcmd

Mass executes commands set in a file
Usage: `checker <file> <bot> [proxy]`

Parameters:
 - `ip:port - string - the server ip` 
 - `username - string - the username`
 - `protocol - integer - the Ninecraft protocol version. Search in google for more info`
 - `file - string - the file with the commands`
 - `proxy - float - a proxy to join the bot socks5` 


## server

Gets information about the specified server
Usage: `server <ip:port>`

Parameters:
 - `ip:port - string - server's ip` 

