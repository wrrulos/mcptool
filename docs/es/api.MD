
# Guía de APIs dentro de MCPTool.

Las APIs desempeñan un papel fundamental en MCPTool al permitir la consulta y obtención de datos relacionados con un servidor de Minecraft. En la actualidad, contamos con las siguientes APIs disponibles:

- [localhost](#localhost)
- [mcsrvstat.us](#mcsrvstat.us)
- [mcstatus.io](#mcstatus.io)

# Cambiar API
Si deseas modificar la API utilizada por MCPTool, simplemente dirígete al archivo de configuración ubicado en `./config/config.json` y actualiza el campo 'api' con el nombre de la API que deseas emplear. 

## Localhost
El método "localhost" implementa una API local mediante Flask. Esta API local permite el envío de solicitudes GET con el propósito de obtener información acerca de los servidores de Minecraft.

## MCSrvstat.us
El método "mcsrvstat.us" utiliza la API proporcionada por el sitio web https://mcsrvstat.us/ para obtener información sobre los servidores de Minecraft.

## MCStatus.io
El método "mcstatus.io" utiliza la API proporcionada por el sitio web https://mcstatus.io/ para obtener información sobre los servidores de Minecraft.
