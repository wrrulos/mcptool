# MCPTool Installation Guide

#### MCPTool is programmed in Python but also utilizes other applications for certain functions.

#### To use MCPTool, you need to install the following:

- Python 3
- NodeJS (Recommended)
- Java 17 or higher (Recommended)
- Nmap (Optional)
- Masscan (Optional)
- Ngrok (Optional)

</br>

# Option 1: Automatic Installation

## Linux

`chmod +x install.sh`

`sudo ./install.sh`

## Windows

`install.bat`

# Option 2: Manual Installation

## Linux

⚠️ *The package manager may vary depending on your distribution.*

#### Installing Python 3

`sudo apt install python3-pip -y`

#### Installing the Virtual Environment Manager (Recommended)

`sudo apt install python3-venv -y`

#### Installing NodeJS (Recommended)

`sudo apt install nodejs npm -y`

#### Installing Java 17 (Recommended)

`sudo apt install openjdk-17-jdk openjdk-17-jre -y`

#### Installing Nmap (Optional)

`sudo apt-get install nmap`

#### Installing Modules

[Module Installation Guide](#2-creating-a-virtual-environment)

## Windows

#### Installing Python 3

`https://www.python.org/downloads/`

#### ***(!) Recommended Version:*** https://www.python.org/downloads/release/python-31010/

#### Installing NodeJS (*Install the recommended version*)

`https://nodejs.org/`

#### Installing Java 17

`https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html`

#### Installing Nmap

`https://nmap.org/download.html`

#### Installing Modules

[Module Installation Guide](#2-creating-a-virtual-environment)

## Module Installation Guide

### Installing Python 3 modules

### **1. Normal Installation**

`python -m pip install -r requirements.txt` 

### **2. Creating a virtual environment**

#### Linux:

`sudo apt install python3-venv -y`

`python3 -m venv .env`

`source .env/bin/activate`

`pip install -r requirements.txt`

#### Windows

`python -m venv .env`

`.env\Scripts\activate`

`pip install -r requirements.txt`

### Installing NodeJS modules

`npm install mineflayer minecraft-colors proxy-agent readline socks`
