import fs from 'fs';
import path from 'path';

import { BotMineflayer } from "./bot.mjs";
import Utilities from "./utilities.mjs"


// Get the path of the MCPTool folder
const mcptoolPath = Utilities.get_mcptool_path();
// Read the configuration file
const configPath = path.join(mcptoolPath, 'bruteforce_settings.json');
const configContent = fs.readFileSync(configPath);

// Parse the configuration file and get the settings
const settings = JSON.parse(configContent);

let loginCommand = settings.bruteauth.loginCommand;
let reconnectDelay = settings.bruteauth.reconnect;
let wordsToLogin = settings.bruteauth.wordsToLogin;
let wordsAtLogin = settings.bruteauth.wordsAtLogin;

// Check if the settings are defined
if (loginCommand === undefined) {
    loginCommand = 'login';
}

if (reconnectDelay === undefined) {
    reconnectDelay = 5000;
}

if (wordsToLogin === undefined) {
    wordsToLogin = ['wrong password!', 'login failed!', '/login'];
}

if (wordsAtLogin === undefined) {
    wordsAtLogin = ['successful login', 'successfully logged in.', 'logueado', 'el sistema de logeo ha sido todo un', 'cuenta iniciada correctamente'];
}


class BruteAuth {
    constructor(host, port, username, version, passwords) {
        try {
            this.bot = new BotMineflayer(host, port, username, version);

            this.bot.on('login', () => {
                console.log('Connected');
                console.log(loginCommand)
                //process.exit(0);
            })

            this.bot.on('message', (message) => {
                let serverMessage = message.toString().toLowerCase();

                console.log(serverMessage);
            })

            this.bot.on('disconnect', (reason) => {
                console.log(reason['reason']);
                process.exit(0);
            })

            this.bot.on('end', (reason) => {
                console.log('&4&l*Timeout');  // This is a error reference
                process.exit(0);
            })

            this.bot.on('error', (error) => {
                Utilities.error_handler(error);
                process.exit(0);
            })

            setTimeout(() => {
                console.log('&c&lTimeout');
                //process.exit(0);
            }, 10000);

        } catch (error) {
            Utilities.error_handler(error);
            process.exit(0);
        }
    }
}

if (process.argv.length < 6) {
    console.log('Usage: node server_response.mjs <host> <port> <username> <version> <passwordFile>');
    process.exit(1);
}

const host = process.argv[2];
const port = parseInt(process.argv[3]);
const username = process.argv[4];
const version = process.argv[5];
const passwordFile = process.argv[6];

// Read passwords from file
const passwords = Utilities.read_file(passwordFile);

new BruteAuth(host, port, username, version, passwords);
