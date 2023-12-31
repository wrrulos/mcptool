const mineflayer = require('mineflayer');
const mccolors = require('minecraft-colors');
const {ProxyAgent} = require('proxy-agent');
const socks = require('socks').SocksClient;
const utils = require('./utils');
const fs = require('fs');

if (process.argv.length < 5) {
    utils.coloredText('Usage: node sendcmd.js <host> <port> <username> <version> <commandFile> <spaces> [<proxyFile>]');
    process.exit(1);
}

const host = process.argv[2];
const port = process.argv[3];
const username = process.argv[4];
const version = process.argv[5];
const commandFile = process.argv[6];
const spaces = process.argv[7];
const proxyFile = process.argv[8];
const commands = utils.getListOfPasswords(commandFile)
let index = 0;

if (commandFile === null) {
    utils.coloredText(`\n${getSpaces(spaces)}§f[§c#§f] §fThe entered command file is not valid.`);
    process.exit(1);
}

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

let settingsData = fs.readFileSync('config/sendcmd_config.json');
let settingsJson = JSON.parse(settingsData);
const reconnectDelay = settingsJson.reconnectDelay;
const commandDelay = settingsJson.commandDelay;

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
                        timeout: 5000,
                        destination: {
                            host: host,
                            port: parseInt(port)
                        }
                    }, (err, info) => {
                        if (err) {
                            utils.coloredText((`\n${getSpaces(spaces)}§f[§c#§f] §cThe proxy server the bot connected to did not respond. Trying to connect with another proxy..`))
                            sendBot();
                            return;
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
        utils.coloredText((`\n${getSpaces(spaces)}§f[§c#§f] §aThe bot has connected to the server.`));

        function executeCommand(index) {
            return new Promise((resolve) => {
                setTimeout(() => {
                    utils.coloredText(`\n${getSpaces(spaces)}§f[§c#§f] §fSending the command: §a${commands[index]}`);
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
                utils.coloredText(`\n${getSpaces(spaces)}§f[§c#§f] §fThe bot has finished sending all the commands.`);
                bot.quit();
                process.exit(1);
            }
        }

        executeNextCommand();
    })

    bot.on('kicked', (reason) => {
        const message = utils.getTextFromJSON(reason);

        if (message.length === 0) {
            let newReason = reason.replace(/"/g, '');
            utils.coloredText((`\n${getSpaces(spaces)}§f[§c#§f] §fThe bot was kicked from the server for the following reason: §c${newReason}`));
        } else {
            utils.coloredText((`\n${getSpaces(spaces)}§f[§c#§f] §fThe bot was kicked from the server for the following reason: §c${message}`));
        }

        bot.quit();
        setTimeout(() => {
            sendBot();
        }, reconnectDelay);
    })

    bot.on('error', (reason) => {
        utils.coloredText((`\n${getSpaces(spaces)}§f[§c#§f] §fThe bot was kicked from the server for the following reason: §cThe bot was forced to disconnect.`));
        bot.quit();
        setTimeout(() => {
            sendBot();
        }, reconnectDelay);
    })
}


function sendBot() {
    if (proxyFile) {
        const randomProxy = utils.getProxy(proxyFile);

        if (randomProxy) {
            utils.coloredText((`\n${getSpaces(spaces)}§f[§c#§f] §aSending the bot to the server.. §f§l(§d${randomProxy[0]}:${randomProxy[1]}§f§l)`));
            createBot(randomProxy);
        } else {
            utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] Invalid Proxy: ${proxyFile}`);
        }

    } else {
        utils.coloredText((`\n${getSpaces(spaces)}§f[§c#§f] §aSending the bot to the server.. §f§l(§cNo proxy§f§l)`));
        createBot();
    }
}

sendBot();

