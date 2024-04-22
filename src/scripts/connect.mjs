import fs from "fs";
import path from "path";
import mccolors from "minecraft-colors";
import readline from "readline";

import { BotMineflayer } from "./bot.mjs";
import Utilities from "./utilities.mjs";

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

if (process.argv.length < 6) {
  console.log(
    "Usage: node brute_auth.mjs <host> <port> <username> <version> <spaces>"
  );
  process.exit(1);
}

const host = process.argv[2];
const port = parseInt(process.argv[3]);
const username = process.argv[4];
const version = process.argv[5];
let spaces = process.argv[6];

// Check if the spaces argument is defined
if (spaces === undefined) {
  spaces = 4;
}

spaces = " ".repeat(spaces);

// Bot instance
let bot = undefined;

// Words array
let words = [];

// Help message with the commands
const helpMessage = `
${spaces}§f[§c#§f] §f§lList of available commands (§cBETA§f§l):

${spaces}§a§l.help §7§l- §f§lListShow this help message.
${spaces}§a§l.move §b§l<movement> §7§l- §f§lExecute a movement of the bot. (forward, back, left, right, jump, sprint, sneak)
${spaces}§a§l.serverip §7§l- §f§lShow the server IP.
${spaces}§a§l.players §7§l- §f§lShow information about all players connected to the server.
${spaces}§a§l.plugins §7§l- §f§lShows the server plugins. (Using the / tab)
`;
/* 
Commands that are not yet implemented:

${spaces}§a§l.file §b§l<file> §7§l- §f§lSend a list of messages/commands that get from the specified file
${spaces}§a§l.seen §b§l<file> §f§lGets the IP addresses of users by using the /seen command. (You must specify a file containing the list of players)
${spaces}§a§l.litebans §7§l- §f§lSave the litebans database (only if it is vulnerable).
${spaces}§a§l.baltop §b§l<pages> §7§l- §f§lGets the list of players obtained on the /baltop.
*/

// Commands to view plugins
const commandsToViewPlugins = [
  "/bukkit:version ",
  "/version ",
  "/bukkit:about ",
  "/about ",
  "/bukkit:ver ",
  "/ver ",
];

class Connect {
  constructor(host, port, username, version) {
    try {
      this.bot = new BotMineflayer(host, port, username, version);
      bot = this.bot.bot; // Save the bot instance to a global variable

      this.bot.on("login", () => {
        console.log(
          mccolors.translateColors(
            `\n${spaces}§f[§c#§f] §aThe bot has connected to the server.`
          )
        );
      });

      this.bot.on("message", (message) => {
        let serverMessage = message.toAnsi();
        console.log(`${spaces}${serverMessage}`);
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

        // Kill the bot and exit
        this.bot.quit();
        process.exit(0);
      });

      this.bot.on("error", (error) => {
        console.log(
          mccolors.translateColors(
            `\n${spaces}§f[§c#§f] §fThe bot was kicked from the server for the following reason: §cThe bot was forced to disconnect.`
          )
        );

        // Kill the bot and exit
        this.bot.quit();
        process.exit(0);
      });
    } catch (error) {
      Utilities.error_handler(error, spaces, true);
      process.exit(0);
    }
  }
}

class CommandManager {
  static enterCommand() {
    rl.question("", (text) => {
      words = text.split(" ");
      const command = words.shift();

      if (command === "exit") {
        console.log(
          mccolors.translateColors(`\n${spaces}§f[§c#§f] §cExiting the bot.`)
        );
        process.exit(0);
      }

      if (bot === undefined) {
        console.log(
          mccolors.translateColors(
            `\n${spaces}§f[§c#§f] §cThe bot is not connected to the server.`
          )
        );
        this.enterCommand();
        return;
      }

      if (commands.hasOwnProperty(command)) {
        commands[command]();
      } else {
        try {
          bot.chat(command);
        } catch (error) {}
      }

      this.enterCommand();
    });
  }

  static helpCommand() {
    console.log(mccolors.translateColors(helpMessage));
  }

  static moveCommand() {
    if (words.length === 0) {
      console.log(
        mccolors.translateColors(
          `\n${spaces}§f[§c#§f] §cYou must specify a movement. (forward, back, left, right, jump, sprint, sneak)`
        )
      );
      return;
    }

    const movement = words[0];

    if (
      !["forward", "back", "left", "right", "jump", "sprint", "sneak"].includes(
        movement
      )
    ) {
      console.log(
        mccolors.translateColors(`\n${spaces}§f[§c#§f] §cInvalid movement.`)
      );
      return;
    }

    if (bot.getControlState(movement)) {
      console.log(mccolors.translateColors(`\n${spaces}§f[§c#§f] §cStopping the movement.`));
      bot.setControlState(movement, false);
    } else {
      console.log(mccolors.translateColors(`\n${spaces}§f[§c#§f] §aMoving the bot ${movement}.`));
      bot.setControlState(movement, true);
    }
  }

  static serverIpCommand() {
    console.log(
      mccolors.translateColors(
        `\n${spaces}§f[§c#§f] §aServer IP: ${host}:${port}`
      )
    );
  }

  static playersCommand() {
    // Get the players on the server
    const playersObject = bot.players;
    console.log(
      mccolors.translateColors(
        `\n${spaces}§f[§c#§f] List of connected players:\n`
      )
    );

    Object.keys(playersObject).forEach(function (key) {
      console.log(
        mccolors.translateColors(
          `${spaces}§f§l${playersObject[key].username} §7(§b${playersObject[key].uuid}§7) §a${playersObject[key].ping}ms§r`
        )
      );
    });
  }

  static pluginsCommand() {
    // Get the players on the server
    const playersObject = bot.players;
    // Players and plugins arrays
    let players = [];
    let plugins = [];

    console.log(mccolors.translateColors(`\n${spaces}§f[§c#§f] §fTrying to get the server plugins...`));

    Object.keys(playersObject).forEach(function (key) {
      players.push(playersObject[key].username);
    });

    setTimeout(async () => {
      for (let i = 0; i < commandsToViewPlugins.length; i++) {
        await new Promise((resolve) => {
          let output = Utilities.get_tab(
            bot,
            commandsToViewPlugins[i],
            spaces,
            true
          );

          output.then((outputList) => {
            if (outputList.length >= 1) {
              outputList.forEach((match) => {
                if (!plugins.includes(match) && !players.includes(match)) {
                  plugins.push(match);
                }
              });
            }

            resolve();
          });
        });
      }

      if (plugins.length >= 1) {
        plugins = plugins.join("§f§l, §a§l");
        console.log(
          mccolors.translateColors(`\n${spaces}§f[§c#§f] §fPlugins: §a${plugins}`)
        );
      } else {
        console.log(
          mccolors.translateColors(
            `\n${spaces}§f[§c#§f] §aThere are no plugins installed on the server. (Or the bot does not have permission to view them)`
          )
        );
      }
    }, 100);
  }
}

// Commands object with the commands
const commands = {
  ".help": CommandManager.helpCommand,
  ".move": CommandManager.moveCommand,
  ".serverip": CommandManager.serverIpCommand,
  ".players": CommandManager.playersCommand,
  ".plugins": CommandManager.pluginsCommand,
};

// Enter the command loop and connect to the server
CommandManager.enterCommand();
new Connect(host, port, username, version);
