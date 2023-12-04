#!/bin/bash
python_var='python3'

# Install Python 3.
sudo apt install python3-pip -y
sudo apt install python3-venv -y

# Install NodeJS.
sudo apt install nodejs npm -y

# Install Java 17.
sudo apt install openjdk-17-jdk openjdk-17-jre -y

# Install Nmap.
sudo apt-get install nmap -y

# Start the virtual environment to install the modules.
$python_var -m venv .env
source .env/bin/activate

# Install modules.
pip install -r requirements.txt

# Stops the virtual environment.
deactivate

# Install the NodeJS modules.
npm install mineflayer minecraft-colors proxy-agent readline socks
