import fs from "fs";
import path from "path";
import mccolors from "minecraft-colors";

import { BotMineflayer } from "./bot.mjs";
import Utilities from "./utilities.mjs";

if (process.argv.length < 7) {
  console.log(
    "Usage: node brute_auth.mjs <host> <port> <username> <version> <commandsFile> <spaces>"
  );
  process.exit(1);
}

const host = process.argv[2];
const port = parseInt(process.argv[3]);
const username = process.argv[4];
const version = process.argv[5];
const commandsFile = process.argv[6];
let spaces = process.argv[7];

// Check if the spaces argument is defined
if (spaces === undefined) {
  spaces = 4;
}

spaces = " ".repeat(spaces);

// Read commands from file
const commands = Utilities.read_file(commandsFile);

// Get the path of the MCPTool folder
const mcptoolPath = Utilities.get_mcptool_path();

// Read the configuration file
const configPath = path.join(mcptoolPath, "sendcmd_settings.json");
const configContent = fs.readFileSync(configPath);

// Parse the configuration file and get the settings
const settings = JSON.parse(configContent);

let reconnectDelay = settings.reconnectDelay;
let commandDelay = settings.commandDelay;

if (reconnectDelay === undefined) {
  reconnectDelay = 5000;
}

if (commandDelay === undefined) {
    commandDelay = 500;
}

// Index of the command
let index = 0;
let bot = null;

class SendCMD {
  constructor(host, port, username, version) {
    try {
      this.bot = new BotMineflayer(host, port, username, version);
      bot = this.bot.bot;

      this.bot.on("login", () => {
        console.log(
          mccolors.translateColors(
            `\n${spaces}§f[§c#§f] §aThe bot has connected to the server.`
          )
        );

        function executeCommand(index) {
            return new Promise((resolve) => {
                setTimeout(() => {
                    console.log(mccolors.translateColors(`\n${spaces}§f[§c#§f] §fSending the command: §a${commands[index]}`));
                    bot.chat(commands[index]);
                    resolve();
                }, commandDelay);
            });
        }

        function executeNextCommand() {
            if (index < commands.length) {
                executeCommand(index)
                    .then(() => {
                        index += 1;
                        executeNextCommand();
                    });
            } else {
                console.log(mccolors.translateColors(`\n${spaces}§f[§c#§f] §fThe bot has finished sending all the commands.`));
                bot.quit();
                process.exit(1);
            }
        }

        executeNextCommand();
      });

      this.bot.on("kicked", (reason) => {
        // Get the message from the JSON
        const message = Utilities.getTextFromJSON(reason);

        if (message.length === 0) {
          const newReason = reason.replace(/"/g, "");
          console.log(
            mccolors.translateColors(
              `\n${spaces}§f[§c#§f] §fThe bot was kicked from the server for the following reason: §c${newReason}`
            )
          );
        } else {
          console.log(
            mccolors.translateColors(
              `\n${spaces}§f[§c#§f] §fThe bot was kicked from the server for the following reason: §c${message}`
            )
          );
        }

        // Kill the bot and reconnect
        this.bot.quit();
        setTimeout(() => {
          new SendCMD(host, port, username, version);
        }, reconnectDelay);
      });

      this.bot.on("error", (error) => {
        console.log(
          mccolors.translateColors(
            `\n${spaces}§f[§c#§f] §fThe bot was kicked from the server for the following reason: §cThe bot was forced to disconnect.`
          )
        );

        // Kill the bot and reconnect
        this.bot.quit();
        setTimeout(() => {
          new SendCMD(host, port, username, version);
        }, reconnectDelay);
      });
    } catch (error) {
      Utilities.error_handler(error);
      process.exit(0);
    }
  }
}

new SendCMD(host, port, username, version);
