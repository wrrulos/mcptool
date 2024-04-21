import { Bot } from "./bot.mjs";
import Utilities from "./utilities.mjs"


class BruteAuth {
    constructor(host, port, username, version, passwords) {
        try {
            this.bot = new Bot(host, port, username, version);

            this.bot.on('login', () => {
                console.log('Connected');
                //process.exit(0);
            })

            this.bot.on('chat', (packet) => {
                console.log(packet)
                const jsonMsg = JSON.parse(packet.message);
                console.log(1, jsonMsg)
                console.log(jsonMsg.text);
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
