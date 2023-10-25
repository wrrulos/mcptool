const mineflayer = require('mineflayer');
const {ProxyAgent} = require('proxy-agent');
const socks = require('socks').SocksClient;
const utils = require('./utils');

if (process.argv.length < 4) {
    utils.coloredText('Usage: node kick.js <host> <port> <username> <version> [<proxyFile>]');
    process.exit(1);
}

const host = process.argv[2];
const port = process.argv[3];
const username = process.argv[4];
const version = process.argv[5];
const spaces = process.argv[6];
const proxyFile = process.argv[7]

if (proxyFile) {
    proxyTest = utils.getListOfPasswords(proxyFile)

    if (proxyTest === null) {
        utils.coloredText(`\n${getSpaces(spaces)}§f[§c#§f] §fThe entered proxy file (§c${proxyFile}§f) is not valid.`);
        process.exit(1);
    }
}

function getSpaces(spaces) {
    return ' '.repeat(spaces);
}


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
            utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] §cIncompatible Minecraft version: Version §c§l${version} §cis not currently supported.`)
        }

        else if (error.message.includes('unsupported protocol version:')) {
            try {
                protocol = error.message.match(/\d+/)['input'].split(': ')[1]
                
            } catch {
                protocol = error.message.match(/\d+/);
            }
            
            if (protocol != null) {
                utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] §cIncompatible Minecraft version: Protocol §c§l${protocol} §cis not supported`)
            } else {
                utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] §cIncompatible Minecraft version: Protocol is not supported`)
            }
        }

        else {
            utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] §4Error`)
        }

        process.exit(1);
    }

    bot.on('login', () => {
        utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] §aThe user ${username} was successfully kicked from the server.`);
        bot.quit()
        process.exit(1);
    })

    bot.on('kicked', (reason) => {
        const message = utils.getTextFromJSON(reason);
        if (message.length === 0) {
            utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] The bot was unable to connect to the server due to the following reason: ${reason}`);
        } else {
            utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] The bot was unable to connect to the server due to the following reason: ${message.replace(/\s{2,}/g, ' ').replace(/\n/g, ' ')}`);
        }

        bot.quit()
        process.exit(1);
    })

    bot.on('error', (_) => {
        utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] The bot was unable to connect to the server due to the following reason: ${_}`);
        bot.quit()
        process.exit(1);
    })

    setTimeout(() => {
        utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] The bot was unable to connect to the server due to the following reason: §cTimeout`);
        bot.quit();
        process.exit(1);
    }, 10000);
}

if (proxyFile) {
    const randomProxy = utils.getProxy(proxyFile);

    if (randomProxy) {
        createBot(randomProxy);
    } else {
        utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] Invalid Proxy: ${proxyFile}`);
    }

} else {
    createBot();
}
