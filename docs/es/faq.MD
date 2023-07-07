# FAQ

Este documento contiene una lista de respuestas a preguntas frecuentes.

### MCPTool se cierra al inicar la herramienta.
Esto se debe a que necesita instalar los módulos de Python. Puede hacerlo a través del script **setup.py**.

### Los servidores proxys no funcionan.
Si los servidores proxy, ya sean Bungee, Velocity o FakeProxy, no funcionan, es debido a que se requiere una versión de Java 17 o superior.

### El metodo Scan o Masscan no funcioan en Linux o termux.
Esto se debe a que masscan y el comando de nmap que viene por defecto requieren permisos de administrador (sudo).

Si deseas utilizar el comando de nmap sin necesidad de permisos de administrador, puedes eliminar el argumento -sS del archivo de configuración config/config.json. Al hacerlo, nmap utilizará un escaneo diferente, como el escaneo TCP Connect (-sT), que no requiere privilegios de root.

### El comando Search no está funcionando correctamente a pesar de haber ingresado una clave de API válida.

El problema que estás experimentando se debe a que tu clave de API de Shodan no tiene acceso a las funcionalidades de búsqueda. Es posible que necesites una clave de API con privilegios más amplios para poder realizar búsquedas.