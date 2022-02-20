import random
import os
import subprocess
import time
import traceback

from mc_replace_text import mc_replace_text_mccolors, mc_replace_text_json
from colorama import Fore, init
from javascript import require, On, Once, console
from argparse import ArgumentParser

# Script created for MCPTool
# @wrrulos

process = require("process", "latest")
mineflayer = require("mineflayer", "latest")

DEBUG = False

positions = ["forward", "back", "left", "right", "jump", "sneak"]
connected = False
disconnected = False

red = Fore.RED
lred = Fore.LIGHTRED_EX
black = Fore.BLACK
lblack = Fore.LIGHTBLACK_EX
white = Fore.WHITE
lwhite = Fore.LIGHTWHITE_EX
green = Fore.GREEN
lgreen = Fore.LIGHTGREEN_EX
cyan = Fore.CYAN
lcyan = Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lmagenta = Fore.LIGHTMAGENTA_EX
yellow = Fore.YELLOW
lyellow = Fore.LIGHTYELLOW_EX
blue = Fore.BLUE
lblue = Fore.LIGHTBLUE_EX
reset = Fore.RESET

help_message = f"""
╔═════════════════════════╦══════════════════════════╗                          
║  Command list           ║    Description           ║
║                         ║                          ║
║ .msg [message]          ║ Send message to a server ║
║ .move [location] [time] ║ Move the bot             ║
║ .tp [location]          ║ Teleport the bot         ║
║ .disconnect             ║ Disconnect the bot       ║
╚═════════════════════════╩══════════════════════════╝\n"""

init()


def taskkill(node):
    subprocess.run(f"taskkill /f /im {node} >nul 2>&1", stdout=subprocess.PIPE, shell=True)


def get_name():
    names = []
    try:
        f = open("names.txt", "r+")

    except:
        f = open("config/files/names.txt", "r+")

    lines = f.readlines()
    f.close()
    for line in lines:
        if not line == "" or not line == " ":
            if "\n" in line:
                line = line.replace("\n", "")

            names.append(line)

    return random.choice(names)


def check(cmd, host, port, version, name):
    global MCPTool

    if name is None:
        if os.path.isfile("names.txt"):
            name = get_name()

        elif os.path.isfile("config/files/names.txt"):
            name = get_name()

        else:
            print("File names.txt not found!")
            os._exit(0)

    try:
        if version is None:
            bot = mineflayer.createBot({"host": host, "port": port, "username": name})

        else:
            bot = mineflayer.createBot({"host": host, "port": port, "username": name, "version": version})

        @On(bot, "kicked")
        def kicked(this, reason, *args):
            if cmd == "check":
                if MCPTool:
                    print(f"{white}{reason}")

                else:
                    reason = mc_replace_text_json(reason)
                    reason = mc_replace_text_mccolors(reason)
                    print(f"\n{lred}Disconnected: {white}{reason}{reset}")

            elif cmd == "kick":
                if MCPTool:
                    print(reason)

            elif cmd == "kickall-mcptool":
                if MCPTool:
                    print(reason)

            bot.quit()
            taskkill(process.pid)
            os._exit(0)

        @On(bot, "login")
        def login(this):
            global MCPTool
            if cmd == "check":
                if MCPTool:
                    print(f"{lgreen}OK{white}")

                else:
                    print(f"\n{lgreen}Connected.{reset}")

            elif cmd == "block":
                if MCPTool:
                    pass

            else:
                if MCPTool:
                    print(f"     {lblack}[{lred}KI{white}CK{lblack}] {white}Kicking the player {lgreen}{name}{white}")

                else:
                    print(f"\n{white}The user {lgreen}{name} {white}has been kicked.{reset}")

            bot.quit()
            taskkill(process.pid)
            os._exit(0)

        time.sleep(5)
        if MCPTool:
            print("Timeout")

        else:
            print(f"{lred}Timeout..{white}")

        bot.quit()
        taskkill(process.pid)
        os._exit(0)

    except:
        try:
            bot.quit()
        except:
            pass

        taskkill(process.pid)
        os._exit(0)


def connect(host, port, version, name):
    global connected, disconnected

    if name is None:
        if os.path.isfile("names.txt"):
            name = get_name()

        elif os.path.isfile("config/files/names.txt"):
            name = get_name()

        else:
            print("File names.txt not found!")
            os._exit(0)

    try:
        if version is None:
            bot = mineflayer.createBot({"host": host, "port": port, "username": name})

        else:
            bot = mineflayer.createBot({"host": host, "port": port, "username": name, "version": version})

        @On(bot, "kicked")
        def kicked(this, reason, *args):
            reason = mc_replace_text_json(reason)
            reason = mc_replace_text_mccolors(reason)
            print(f"\n{lred}Disconnected: {reason}{lwhite}")
            bot.quit()
            taskkill(process.pid)
            os._exit(0)

        @On(bot, "end")
        def end(*args):
            bot.quit()
            if MCPTool:
                taskkill(process.pid)

            os._exit(0)

        @On(bot, 'message')
        def handle_message(this, message, *args):
            if not len(str(message)) == 356:
                print(f"{message.toAnsi()}")

        @On(bot, "login")
        def login(this):
            global connected
            connected = True
            print(f"\n{lgreen}Bot connected! \n{white}Connecting to chat..{reset}\n")

        time.sleep(5)
        if connected:
            print(f"\n{lgreen}Chat connected! Use {lcyan}.help{lgreen} to view commands.{white}\n")
            while True:
                argument = input().split()

                if len(argument) == 0:
                    print("Unknown commannd. Use .help")
                    continue

                try:
                    command = argument[0]

                    if command.lower() == f".msg":
                        try:
                            _ = argument[1]
                            message = argument
                            message[0] = message[0].replace(".msg", "")
                            message = " ".join(message)
                            message = message[1:]
                            bot.chat(message)

                        except IndexError:
                            print("Usage .msg [message]")

                        except Exception as e:
                            if DEBUG:
                                print(f"     [DEBUG] Exception (.msg): {e} \n\n{traceback.format_exc()}")

                    elif command.lower() == ".move":
                        try:
                            position = argument[1].lower()
                            time_to_move = argument[2]
                            if position in positions:
                                if time_to_move.isdecimal():
                                    bot.setControlState(position, True)
                                    if position == "forward" or position == "back":
                                        print(f"Moving the bot back for {time_to_move} seconds")

                                    elif position == "left" or position == "right":
                                        print(f"Moving the bot to the {position} for {time_to_move} seconds")

                                    elif position == "jump":
                                        print(f"Making the bot jump for {time_to_move} seconds")

                                    time.sleep(int(time_to_move))
                                    bot.clearControlStates()

                                else:
                                    print("Set a valid time!")
                            else:
                                print("Write a valid move! (forward, back, left, right, jump)")

                        except IndexError:
                            print("Usage .move [position] [time]")

                        except Exception as e:
                            if DEBUG:
                                print(f"     [DEBUG] Exception (.msg): {e} \n\n{traceback.format_exc()}")

                    elif command.lower() == ".tp":
                        try:
                            location = argument[1].lower()

                            if location == "x":
                                bot.entity.position.x += 10

                            elif location == "y":
                                bot.entity.position.y += 10

                            else:
                                print("Write a valid location! (x, y)")

                        except IndexError:
                            print("Usage .tp [location]")

                        except Exception as e:
                            if DEBUG:
                                print(f"     [DEBUG] Exception (.msg): {e} \n\n{traceback.format_exc()}")

                    elif command.lower() == ".disconnect":
                        bot.quit()
                        taskkill(process.pid)
                        os._exit(0)

                    elif command.lower() == ".help":
                        print(help_message)

                    else:
                        print("Unknown commannd. Use .help")

                except KeyboardInterrupt:
                    bot.quit()
                    taskkill(process.pid)
                    os._exit(0)

                except:
                    pass

        else:
            if not disconnected:
                print("ERROR: Timeout")

            bot.quit()
            taskkill(process.pid)
            os._exit(0)

    except Exception as e:
        if DEBUG:
            print(f"{traceback.format_exc()}")
        pass

    except KeyboardInterrupt:
        try:
            bot.quit()
            taskkill(process.pid)

        except:
            pass

        os._exit(0)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-host", help="Host", required=True, action="store", dest="host")
    parser.add_argument("-p", help="Port", required=True, action="store", dest="port")
    parser.add_argument("-m", help="Mode", required=True, action="store", dest="mode")
    parser.add_argument("-v", help="Version", required=False, action="store", dest="version")
    parser.add_argument("-n", help="Name", required=False, action="store", dest="name")
    parser.add_argument("-mcptool", help="MCPTool Mode", required=False, default=False, dest="mcptool", action="store_true")
    args = parser.parse_args()

    MCPTool = args.mcptool

    if args.mode == "connect":
        connect(args.host, args.port, args.version, args.name)

    elif args.mode == "check":
        check("check", args.host, args.port, args.version, None)

    elif args.mode == "kick":
        check("kick", args.host, args.port, args.version, args.name)

    elif args.mode == "kickall-mcptool":
        check("kickall-mcptool", args.host, args.port, args.version, args.name)

    elif args.mode == "block":
        check("block", args.host, args.port, args.version, args.name)

    else:
        print("Enter a valid mode!")
