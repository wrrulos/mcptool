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
const lang = process.argv[6]
const proxyHost = process.argv[7];
const proxyPort = process.argv[8];
let lang_data = fs.readFileSync(`settings/lang/${lang}.json`);
let lang_json = JSON.parse(lang_data);
const proxyTimeout = lang_json.other_messages.PROXY_TIMEOUT
const bot_connected = lang_json.commands.kick.BOT_CONNECTED
const bot_expelled = lang_json.commands.kick.BOT_EXPELLED

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
              console.log(mccolors.translateColors(`§c${proxyTimeout}`))
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
    console.log(mccolors.translateColors(`\n    §f[§c#§f] ${bot_connected.replace('[0]', username)}`))
    bot.quit()
    process.exit(1);
  })

  bot.on('error', (err) => {
    console.log(mccolors.translateColors(`\n    §f[§c#§f] §c${err}`))
    bot.quit()
    process.exit(1);
  })

  bot.on('kicked', reason => {
    reason = replaceWords(reason)
    console.log(mccolors.translateColors(`\n    §f[§c#§f] ${bot_expelled.replace('[0]', username)}${reason}`))
    bot.quit()
    process.exit(1);
  })
}

createBot()
