# FAQ

Este documento contiene una lista de respuestas a preguntas frecuentes.

### MCPTool se cierra al iniciar la herramienta.
Esto sucede porque necesitas instalar los módulos de Python. Puedes hacerlo a través del script **setup.py**.

### Los servidores proxy no están funcionando.
Si los servidores proxy, ya sean Bungee, Velocity o FakeProxy, no están funcionando, es probable que sea debido a la necesidad de Java 17 o una versión superior.

### ¿Cómo evito que MCPTool busque actualizaciones?
Anteriormente, podías cambiar un valor en el archivo de configuración, pero ahora, para omitir las actualizaciones de MCPTool, debes presionar Ctrl+C cuando la herramienta notifique que está buscando una nueva versión. También puedes omitir las actualizaciones del proxy cambiando el valor '"updateProxy": true' a false en el archivo de configuración. No se recomienda, ya que podría generar incompatibilidad si se lanza una nueva versión de Minecraft.

### El método Scan o Masscan no funciona en Linux o Termux.
Esto se debe a que Masscan y el comando Nmap por defecto requieren permisos de administrador (sudo).

Si quieres usar el comando Nmap sin necesidad de permisos de administrador, puedes eliminar el argumento -sS del archivo config/config.json. Al hacerlo, Nmap utilizará un escaneo diferente, como el escaneo TCP Connect (-sT), que no requiere privilegios de root.

### Error (Missing NodeJS Modules!)
Se debe a que falta instalar los módulos de NodeJS para poder ejecutar los scripts que controlan los bots en MCPTool.

### El comando Shodan no funciona correctamente a pesar de ingresar una clave de API válida.

El problema que estás experimentando probablemente se deba a que tu clave de API de Shodan no tiene acceso a las funcionalidades de búsqueda. Es posible que necesites una clave de API con privilegios más amplios para poder realizar búsquedas.
