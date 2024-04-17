import Bot from "./bot.mjs";


class ServerResponse {
    constructor(host, port, username, version) {
        this.bot = new Bot(host, port, username, version);

        this.bot.on('login', () => {
            console.log('Connected');
            process.exit(0);
        })

        this.bot.on('disconnect', (reason) => {
            console.log(reason['reason']);
            process.exit(0);
        })

        this.bot.on('end', (reason) => {
            console.log(reason);
            process.exit(0);
        })

        this.bot.on('error', (error) => {
            console.log(error);
            process.exit(0);
        })

        setTimeout(() => {
            console.log('Timeout');
            process.exit(0);
        }, 10000);
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
