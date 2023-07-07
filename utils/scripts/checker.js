const mineflayer = require('mineflayer');
const {ProxyAgent} = require('proxy-agent');
const socks = require('socks').SocksClient;
const utils = require('./utils');

if (process.argv.length < 4) {
    utils.coloredText('Usage: node checker.js <host> <port> <version> [<proxyFile>]');
    process.exit(1);
}

const username = utils.getUsername('utils/otherfiles/usernames.txt')
const host = process.argv[2];
const port = process.argv[3];
const version = process.argv[4];
const proxyFile = process.argv[5]

function createBot(proxy=null) {
    let bot;

    try {
        if (proxy) {
            bot = mineflayer.createBot({
                connect: client => {
                    socks.createConnection({
                        proxy: {
                            host: proxy[0],
                            port: proxy[1],
                            type: 5
                        },
                        command: 'connect',
                        destination: {
                            host: host,
                            port: parseInt(port)
                        }
                    }, (err, info) => {
                        if (err) {
                            utils.coloredText('§cProxy Error');
                            utils.coloredText(err)
                            return
                        }
    
                        client.setSocket(info.socket)
                        client.emit('connect')
                    })
                },
    
                agent: new ProxyAgent({ protocol: 'socks5:', host: proxy[0], port: proxy[1] }),
                username: username,
                fakeHost: host,
                version: version,
                hideErrors: true,
            })
        } else {
            bot = mineflayer.createBot({
                host: host,
                fakeHost: host,
                port: port,
                username: username,
                version: version,
                hideErrors: true
            })
        }
    } catch (error) {
        if (error.message.includes('is not supported')) {
            const version = error.message.match(/\d+\.\d+\.\d+/)[0];
            utils.coloredText(`§4Version §c${version} §4is not currently supported.`);
        } 

        else if (error.message.includes('unsupported protocol version:')) {
            const protocol = error.message.match(/\d+/)[0];
            utils.coloredText(`§4Protocol §c${protocol} §4is not supported`);
        }

        else {
            utils.coloredText('§4Error');
        }

        process.exit(1);
    }
    
    bot.on('login', () => {
        utils.coloredText('§aConnected');
        bot.quit()
        process.exit(1);
    })

    bot.on('kicked', (reason) => {
        const message = utils.getTextFromJSON(reason);
        if (message.length === 0) {
            utils.coloredText(reason);
        } else {
            utils.coloredText(message);
        }

        bot.quit()
        process.exit(1);
    })

    bot.on('error', (_) => {
        utils.coloredText('§cTimeout');
        bot.quit()
        process.exit(1);
    })

    setTimeout(() => {
        utils.coloredText('§cTimeout');
        bot.quit();
        process.exit(1);
    }, 10000);
}

if (proxyFile) {
    const randomProxy = utils.getProxy(proxyFile);

    if (randomProxy) {
        createBot(randomProxy);
    } else {
        utils.coloredText('§cProxy Error');
    }
    
} else {
    createBot();
}
