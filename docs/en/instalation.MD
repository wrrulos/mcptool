# MCPTool Installation Guide

#### MCPTool is programmed in Python and NodeJS, but also uses other applications for certain functions. To use MCPTool you must install the following:

* Python 3
* NodeJS (Recommended)
* Java 17 or higher. (Recommended)
* Nmap (Optional)
*Masscan (Optional)
* Ngrok (Optional)

</br>

# Automatic installation
Run **python setup.py**. (Note that the python variable may vary depending on your system)

### DEBUG mode

If you want to run **setup.py** in debug mode, you must add the following parameter: *--debug*

![Alt ​​text](../images/setup-debug.png)

# Manual installation.

## ⚫ Python 3

## Windows

To install *Python 3* on **Windows** you must download the latest version from its official website: https://www.python.org/

# Recommended version: https://www.python.org/downloads/release/python-31010/

## Linux

You can install python3 using the **apt** package manager.

`sudo apt install python3-pip`

## Termux

`pkg install python3`

</br>

## ⚫ NodeJS


**IMPORTANT!** You must install the recommended version of NodeJS.

## Windows

To install *NodeJS* on **Windows** you must download the latest version from its official website: https://nodejs.org/es/

## Linux

You can install nodejs using the **apt** package manager.

`sudo apt install nodejs -y`
`sudo apt install npm -y`

## Termux

`pkg install nodejs -y`

</br>

## ⚫ Java 17

## Windows

To install *Java 17* on **Windows** you must download the latest version from its official website: https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html

## Linux

You can install java using the **apt** package manager.

`sudo apt install openjdk-17-jdk openjdk-17-jre`

## Termux

`pkg install openjdk-17 -y`

</br>

## ⚫ Nmap

## Windows

To install *Nmap* on **Windows** you must download the latest version from its official website: https://nmap.org/download.html

## Linux

You can install nmap using the **apt** package manager.

`sudo apt-get install nmap`

## Termux

`pkg install nmap -y`

</br>

## ⚫ Ngrok

## Windows

To install *Ngrok* on **Windows** you must download the latest version from its official website: https://ngrok.com/download

## Linux

You can install ngrok using the **apt** package manager.

`curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok`

## Termux

`pkg update && pkg upgrade -y | pkg install zip wget -y | wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip | unzip ngrok-stable-linux-arm.zip | chmod +x ngrok`

</br>

## ⚫ Masscan
https://github.com/robertdavidgraham/masscan
