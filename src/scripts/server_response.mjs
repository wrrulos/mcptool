import Bot from "./bot.mjs";


class ServerResponse {
    constructor(host, port, username, version) {
        this.bot = new Bot(host, port, username, version);

        this.bot.on('connect', () => {
            console.log('Connected');
            process.exit(0);
        })

        this.bot.on('disconnect', (reason) => {
            console.log('Kicked for:', reason);
            process.exit(0);
        })

        this.bot.on('end', (reason) => {
            console.log('Connection closed', reason);
            process.exit(0);
        })
    }
}


if (process.argv.length < 5) {
    console.log('Usage: node server_response.mjs <host> <port> <username> <version>');
    process.exit(1);
}

const host = process.argv[2];
const port = parseInt(process.argv[3]);
const username = process.argv[4];
const version = process.argv[5];
new ServerResponse(host, port, username, version);
