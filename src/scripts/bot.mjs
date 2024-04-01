import mc from 'minecraft-protocol';


class Bot {
    constructor(host, port, username, version) {
        this.bot = mc.createClient({
            host: host,
            port: port,
            username: username,
            version: version
        });
    }

    on(event, callback) {
        this.bot.on(event, callback);
    }

    end() {
        this.bot.end();
    }
}

export default Bot;