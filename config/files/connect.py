import random
import os
import time

from javascript import require, On, Once, console
from argparse import ArgumentParser

mineflayer = require("mineflayer", "latest")
names = []

try:
    f = open("names.txt", "r+")
    content = f.readlines()
    f.close()

    for line in content:
        if "\n" in line:
            line = line.replace("\n", "")
        names.append(line)

    name = random.choice(names)


    def file(result):
        if result[0] == "{" and result[-1] == "}":
            result = result.replace(result[0], "").replace(result[-1], "").replace(result[1], "").replace(result[-2], "")

        if result[0] == '"' and result[-1] == '"':
            result = result.replace(result[0], "").replace(result[-1], "")

        try:
            f = open("connect.txt", "w+", encoding="utf8")
            f.write(result)
            f.close()

        except:
            f = open("connect.txt", "w+", encoding="unicode_escape")
            f.write(result)
            f.close()


    parser = ArgumentParser()
    parser.add_argument("-host", help="Host", required=True, action="store", dest="host")
    parser.add_argument("-p", help="Port", required=True, action="store", dest="port")
    args = parser.parse_args()

    host = args.host
    port = args.port

    bot = mineflayer.createBot({
    "host": host,
    "port": port,
    "username": name
    })


    @On(bot, "login")
    def login(this):
        file("MCPTool-OK")
        bot.quit()
        os._exit(0)


    @On(bot, "kicked")
    def kicked(this, reason, *a):
        file(reason)
        bot.quit()
        os._exit(0)


    time.sleep(5)
    file("MCPTool-TIMEOUT")
    os._exit(0)

except:
    pass