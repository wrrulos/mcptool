# How to install MCPTool

- [Install dependencies](#dependencies)
  - [Python](#python)
  - [NodeJS](#nodejs)
  - [Nmap](#nmap)
  - [Ngork](#ngrok)
  - [Python Modules](#python-modules)
  - [NodeJS Modules](#nodejs-modules)


## Dependencies

For the tool to work correctly you must install all the necessary dependencies.

## Python

To install Python3 you have to download the latest version on its official page. https://www.python.org/downloads/
Be sure to add PIP to the command line on install!

## NodeJS

To install NodeJS you have to download the latest version (recommended) on its official page. https://nodejs.org/es/

## Nmap

To install Nmap you have to download the latest version on its official page. https://nmap.org/download.html

## Ngrok

To install Ngrok first you have to go to the official page and create an account. https://ngrok.com/
After that, download the latest version and move the downloaded file to MCPTool folder. https://ngrok.com/download 
Finally, open a terminal in the MCPTool folder and it will bind the ngrok account token. (The token appears on the page). https://dashboard.ngrok.com/get-started/setup

<img src="https://i.imgur.com/S9w22Vw.png">

## Python Modules

After installing Python you will need to install the modules that MCPTool needs to work. 
For this start a terminal in the MCPTool folder and use the command python -m pip install -r requirements

[!] COMMAND NOT FOUND

If the terminal does not detect the command, it is because there was an error with the installation or simply python is using another variable on your computer. 
Try the following commands or reinstall python:

- python3 -m pip install -r requirements
- py -m pip install -r requirements
- py3 -m pip install -r requirements

If the python variable on your system is not 'python' open the configuration file and change the value of the following option to the python variable.

<img src="https://i.imgur.com/aTbEvW4.png">

## NodeJS Modules

After installing NodeJS, you will need to install the modules that MCPTool needs to work.
For this, start a terminal in the MCPTool folder and run the following commands:

 - npm install mineflayer
 - npm install minecraft-colors
 - npm install proxy-agent
 - npm install socks
 - npm install readline

## ONLY ON WINDOWS (OPTIONAL)

If you are using a version of Windows lower than Windows 11, you are probably using the classic terminal of this operating system (the cmd).
What is the problem with using the cmd? Well, the problem is that the new versions of MCPTool contain characters that this terminal does not support.

How to solve it? You have two options

## Windows Terminal

You can download 'Windows Terminal' in the microsoft store and start the tool from there.

<img src="https://i.imgur.com/L6RLv2y.png">

## Edit the configuration file

If you want to continue using the cmd you can go to the MCPTool configuration file and change the value of the "TYPE_OF_BANNERS" option from 1 to 2. By changing this option MCPTool shows other types of banners with characters that the cmd supports.

<img src="https://i.imgur.com/AUjPj2W.png"

