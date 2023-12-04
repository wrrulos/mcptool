# Guía completa sobre los comandos de MCPTool

Lista de los comandos actuales de MCPTool.

- [Server](#server)
- [Uuid](#uuid)
- [IPInfo](#ipinfo)
- [DNSLookup](#dnslookup)
- [Shodan](#shodan)
- [WebSearch](#websearch)
- [Subdomains](#subdomains)
- [Scan](#scan)
- [Listening](#listening)
- [PlayerLogs](#playerlogs)
- [Resolver](#resolver)
- [FakeProxy](#fakeproxy)
- [Login](#login)
- [PinLogin](#pinlogin)
- [SendCMD](#sendcmd)
- [Kick](#kick)
- [KickAll](#kickall)
- [RconBrute](#rconbrute)
- [Checker](#checker)
- [Waterfall](#waterfall)
- [Velocity](#velocity)
- [Connect](#connect)
- [Rcon](#rcon)

- [Discord](#discord)

## Server
El comando **server** te permite obtener información acerca de un servidor de minecraft. Funciona en servidores Java Y Bedrock.

![Server](../images/commands/server.png)

Para usar este comando debe ingresar:
</br>
`server <ip:port/dominio>`

## Uuid
El comando **uuid** te permite obtener las uuid de un usuario de Minecraft.

![Uuid](../images/commands/uuid.png)

Para usar este comando debe ingresar:
</br>
`uuid <usuario>`

## IPInfo
El comando **ipinfo** te permite obtener información acerca de una dirección IP.

![IPInfo](../images/commands/ipinfo.png)

Para usar este comando debe ingresar:
</br>
`ipinfo <ip>`

## DNSLookup
El comando **dnslookup** te permite obtener los registros dns de un dominio en especifico.

![DnsLookup](../images/commands/dnslookup.png)

Para usar este comando debe ingresar:
</br>
`dnslookup <dominio>`

## Shodan
El comando **shodan** usa el buscador de Shodan para buscar servidores que contengan ciertos datos.

**¡IMPORTANTE!** Para usar este comando debe ingresar una clave api de Shodan en el archivo de configuración de MCPTool.

![Shodan](../images/commands/search.png)

Para usar este comando debe ingresar:
</br>
`shodan <datos>`

También puede ingresar varios datos en un solo comando para realizar multiples busquedas. Los datos deben estar separados por **---**. Ejemplo:
</br>
`shodan spigot 1.8.8 --- spigot 1.19`

## WebSearch
El comando **websearch** te permite buscar servidores de minecraft que contengan datos especificos en multiples páginas.

![WebSearch](../images/commands/websearch.png)

Para usar este comando debe ingresar:
</br>
`websearch <tag>`

## Scan
El comando **scan** te permite realizar un escaneo para buscar puertos abiertos donde se alojen servidores de Minecraft.

### **Rango de IP**
Puede ingresar una IP normal como **127.0.0.1**.

Pero también puedes ingresar un rango de IP, como por ejemplo: **127.0.0.1-255**

Los formatos válidos para los rangos de IP varían según el tipo de escaner que seleccione.

### **Rango de Puertos**
Puede ingresar un puerto normal como **25565**.

Pero también puedes ingresar un rango de puertos, como por ejemplo: **25560-25570**

Los formatos válidos para los rangos de puertos varían según el tipo de escaner que seleccione.

### **Escaner**.
Puedes realizar el escaneo utilizando diferentes escaners, esto se especifica en el argumento **method**

Lista de metodos:

- Nmap (0)
- Quboscanner (1)
- Masscan (2)

En el argumento **method** puede ingresar el nombre del escaner o su respectivo número.

![Scan2](../images/commands/scan_1.png)
</br>
![Scan1](../images/commands/scan_2.png)
</br>
![Scan3](../images/commands/scan_3.png)

Para usar este comando debe ingresar:
</br>
`scan <ip> <ports> <method>`

## Subdomains
El comando **subdomains** te permite obtener los subdominios de un dominio.

![Subdomains](../images/commands/subdomains.png)

Para usar este comando debe ingresar:
</br>
`subdomains <dominio> <subdomainsFile>`

## Checker
El comando **checker** te permite obtener los datos actuales de los servidores que se encuentren en una archivo de texto especificado. 

![Checker](../images/commands/checker.png)

Para usar este comando debe ingresar:
</b>
`checker <file>`

## Listening
El comando **listening** te permite obtener la lista de jugadores que se conectan al servidor, junto a sus uuids.

![Listening](../images/commands/listening.png)

Para usar este comando debe ingresar:
</br>
`listening <ip:port/dominio>`

## Playerlogs
El comando **playerlogs** es similar al comando *listening*, te permite obtener la fecha y hora de cuando se conectan y desconectan usuarios del servidor especificado, junto a sus uuids.

![Playerlogs](../images/commands/playerlogs.png)

Para usar este comando debe ingresar:
</br>
`playerlogs <ip:port/dominio>`

## Resolver
El comando **resolver** le permite obtener direcciones IP y subdominios vinculados al dominio especificado.

![Resolver](../images/commands/resolver.png)

Para usar este comando debe ingresar:
</br>
`resolver <dominio>`

## Waterfall
El comando **waterfall** crea un servidor proxy waterfall que redirecciona al servidor especificado. 

El servidor proxy viene con mi plugin *RBungeeExploit* por defecto. Este plugin te permite ejecutar los siguientes comandos:

- /set-uuid -> Cambia tu uuid.
- /connect -> Te conecta al servidor especificado.

![Waterfall](../images/commands/waterfall_1.png)
</br>
![Waterfall2](../images/commands/waterfall_2.png)
</br>
![Waterfall3](../images/commands/waterfall_3.png)

Para usar este comando debe ingresar:
</br>
`waterfall <ip:port/dominio>`

**NOTA** Se recomienda ingresar la ip y puerto del servidor.

## Velocity
El comando **velocity** crea un servidor proxy velocity que redirecciona al servidor especificado. 

El servidor proxy viene con mi plugin *MCPTool* por defecto. Este plugin te permite ejecutar los siguientes comandos:

- /username -> Cambia tu nombre de usuario.
- /uuid -> Cambia tu uuid.
- /connect -> Te conecta al servidor especificado.

![Velocity1](../images/commands/velocity_1.png)
</br>
![Velocity2](../images/commands/velocity_2.png)
</br>
![Velocity3](../images/commands/velocity_3.png)
</br>
![Velocity4](../images/commands/velocity_4.png)

Para usar este comando debe ingresar:
</br>
`velocity <ip:port/domain> <forwarding-mode>`

**NOTA** Se recomienda ingresar la ip y puerto del servidor.

## FakeProxy
El comando **fakeproxy** crea un servidor proxy velocity que redirecciona al servidor especificado y captura todos los datos. Los datos que guarda son: 

- Fecha y hora de cuando entran y salen los usuarios.
- Nombre del usuario y dirección IP.
- Comandos y mensajes enviados.

Además de guardar los datos, también te permite interactuar con los usuarios del proxy mediante comandos.

![FakeProxy](../images/commands/fakeproxy.png)
![FakeProxyServers](../images/commands/fakeproxy_server.png)
![FakeProxyPlugin](../images/commands/fakeproxy_commands.png)

Para usar este comando debe ingresar:
</br>
`fakeproxy <ip:port/domain> <forwarding-mode>`

**NOTA** Se recomienda ingresar la ip y puerto del servidor.

## Connect
El comando **connect** te permite conectarte a un servidor de minecraft mediante la terminal.

![Connect](../images/commands/connect.png)

Para usar este comando debe ingresar:
</br>
`connect <ip:puerto> <user> <version>`

## Rcon
El comando **rcon** te permite conectarte a un servidor de minecraft mediante rcon (solo si esta activado).

![Rcon](../images/commands/rcon.png)

Para usar este comando debe ingresar:
</br>
`rcon <ip:rconPort> <rconPassword>`

## RconBrute
El comando **rconbrute** te permite realizar un ataque de fuerza bruta al puerto rcon del servidor especificado para intentar adivinar la contraseña.

Para usar este comando debe ingresar:
</br>
`rconbrute <ip:rconPort> <passwordFile>`

## Login
El comando **login** te permite realizar un ataque de fuerza bruta a un usuario de minecraft dentro de un servidor no premium para intentar adivinar su contraseña. (/login)

**¡IMPORTANTE!** Te daré un breve resumen de como funciona el bot:

* Cuando el bot se conecta al servidor, se queda a la escucha de que aparezca alguno de los mensajes que se encuentran en el archivo de configuración **bruteforce_config** (*wordsToLogin*). </br></br> Luego de leer cualquiera de las palabras de esa lista, el bot ejecuta el comando para autenticarse y luego se queda a la escucha nuevamente, hasta que lea algunas de las palabras de (*wordsAtLogin*)

[!] Si el bot no prueba ninguna contraseña o si luego de probar una no hace nada más, es porque necesitas agregar más palabras en las listas correspondientes.

Para usar este comando debe ingresar:
</br>
`login <ip:port/dominio> <username> <version> <passwordFile>`

## PinLogin
El comando **pinlogin** te permite realizar un ataque de fuerza bruta a un usuario de minecraft dentro de un servidor que use el plugin *AdvancedLogin*, para intentar adivinar su contraseña.

![Alt text](../images/commands/pinlogin_plugin.png)

**NOTA** Este comando usa la misma logica que el comando **[login](#login)**, pero en vez de textos, son titulos.

Para usar este comando debe ingresar:
</br>
`pinlogin <ip:port/dominio> <username> <version> <digits>`

## Kick
El comando **kick** te permite conectar un bot con un nombre en especifico. Esto es para desconectarlo en el caso de que el servidor expulse a los jugadores que inician sesión desde otra úbicación.

Para usar este comando debe ingresar:
</br>
`kick <ip:port> <username> <version> <loop>`

**NOTA** En loop debe ingresar *y* o *n*.

## KickAll
El comando **kickall** te permite conectar bots con el nombre de cada jugador que se encuentra en el servidor. Esto es para desconectarlos en el caso de que el servidor expulse a los jugadores que inician sesión desde otra úbicación.

Para usar este comando debe ingresar:
</br>
`kickall <ip:port> <version> <loop>`

**NOTA** En loop debe ingresar *y* o *n*.

## SendCMD
El comando **sendcmd** te permite conectar un bot que enviara una lista de mensajes o comandos que se encuentran en el archivo de texto especificado.

Para usar este comando debe ingresar:
</br>
`sendcmd <ip:port> <username> <version> <file> <loop>`

**NOTA** En loop debe ingresar *y* o *n*.

## Language
El comando **language** te permite cambiar el idioma de la herramienta.

Lista de idiomas disponibles:

- Español (**es**)
- Ingles (**en**)
- Catalan (**cat**)
- Aleman (**de**)
- Frances (**fr**)
- Portugues (**pt**)
- Eslovaco (**sk**)
- Turco (**tr**)

Debe especificar la abreviatura del lenguaje, por ejemplo, **es**.

Para usar este comando debe ingresar:
</br>
`language <language>`

## Discord
El comando **discord** muestra el enlace de mi servidor de discord.

Para usar este comando debe ingresar:
</br>
`discord`
