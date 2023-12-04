# Guía de instalación de MCPTool

#### MCPTool está programado en Python, pero también utiliza otras aplicaciones para ciertas funciones.

#### Para usar MCPTool, debes instalar lo siguiente:

- Python 3
- NodeJS (Recomendado)
- Java 17 o superior (Recomendado)
- Nmap (Opcional)
- Masscan (Opcional)
- Ngrok (Opcional)

</br>

# Opción 1: Instalación automática

## Linux

`chmod +x install.sh`

`sudo ./install.sh`

## Windows

`install.bat`

# Opción 2: Instalación manual

## Linux

⚠️ *El gestor de paquetes puede variar según tu distribución.*

#### Instalación de Python 3

`sudo apt install python3-pip -y`

#### Instalación de gestor de entornos virtuales (Recomendado)

`sudo apt install python3-venv -y`

#### Instalación de NodeJS (Recomendado)

`sudo apt install nodejs npm -y`

#### Instalación de Java 17 (Recomendado)

`sudo apt install openjdk-17-jdk openjdk-17-jre -y`

#### Instalación de Nmap (Opcional)

`sudo apt-get install nmap`

#### Instalación de Módulos

[Guía de instalación de Módulos](#2-crear-un-entorno-virtual)

## Windows

#### Instalación de Python 3

`https://www.python.org/downloads/`

#### ***(!) Versión recomendada:*** https://www.python.org/downloads/release/python-31010/

#### Instalación de NodeJS (*Debes instalar la versión recomendada*)

`https://nodejs.org/`

#### Instalación de Java 17

`https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html`

#### Instalación de Nmap

`https://nmap.org/download.html`

#### Instalación de Módulos

[Guía de instalación de Módulos](#2-crear-un-entorno-virtual)

## Guía de Instalación de Módulos

### Instalación de modulos de Python 3

### **1. Instalacion normal**

`python -m pip install -r requirements.txt` 

### **2. Crear un entorno virtual**

#### Linux:

`sudo apt install python3-venv -y`

`python3 -m venv .env`

`source .env/bin/activate`

`pip install -r requirements.txt`

#### Windows

`python -m venv .env`

`.env\Scripts\activate`

`pip install -r requirements.txt`

### Instalación de módulos de NodeJS.

`npm install mineflayer minecraft-colors proxy-agent readline socks`
