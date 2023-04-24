const mccolors = require('minecraft-colors')
const mineflayer = require('mineflayer');
const ProxyAgent = require('proxy-agent');
const socks = require('socks').SocksClient
const readline = require('readline');
const proxy = require('proxy-agent');
const fs = require('fs');
const path = require('path');

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
const botFileNotFound = lang_json.commands.connect.BOT_FILE_NOT_FOUND
const proxyTimeout = lang_json.other_messages.PROXY_TIMEOUT
const exit = lang_json.commands.connect.EXIT

function readFile(commandFile) {
  let commands = []

  try {
    const fileContent1 = fs.readFileSync(commandFile, 'utf8')
    const content = fileContent1.split('\n');
  
    for (word of content) {
      word = word.replace('\r', '')
      commands.push(word)
    }

    return commands;
  } catch (err) {
    return 'Error'
  }
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
              console.log(mccolors.translateColors(`\n    §f[§c#§f] §c${proxyTimeout}\n`))
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
    input()
  })

  bot.on('message', (toAnsi)=>{
    var msg = toAnsi.toAnsi()
    console.log(`    ${msg}`)
  })

  bot.on('error', (err) => {
    err = replaceWords(err)
    bot.quit()
    console.log(mccolors.translateColors(`\n    §f[§c#§f] §fError: ${err}\n`))
    console.log(mccolors.translateColors(`\n    §f[§c#§f] ${exit}`))
  })

  bot.on('kicked', reason => {
    reason = replaceWords(reason)
    bot.quit()
    console.log(mccolors.translateColors(`\n    §f[§c#§f] §f${botExpelled}§c${reason}\n`))
    console.log(mccolors.translateColors(`    §f[§c#§f] ${exit}`))
  })

  async function complete (str) {
    try {
      const matches = await bot.tabComplete(str)
      const matchStrings = matches.map(match => match.match)
      const matchString = matchStrings.join(', ')
      console.log(mccolors.translateColors(matchString))
    } catch (err) {
      console.log(err.message)
    }
  }

  function input() {
    rl.question('', function (command) {
      const words = command.split(' ');
  
      if (words[0] == '.help') {
        console.log('.file [file]')
      }
  
      else if (words[0] == '.tab') {
        complete(words.slice(1).join(' '))
      }
  
      else if (words[0] == '.file') {
        const commands = readFile(`files/${words[1]}`)
  
        if (Array.isArray(commands)) {
          let counter = 0
          for (const command of commands) {
            setTimeout(() => {
              bot.chat(command)
            }, counter * 1000)
            counter++;
          }
        } else {
          console.log(mccolors.translateColors(`\n    §f[§c#§f] ${botFileNotFound}\n`))
        }
      }
  
      else if (words[0] == '.exit') {
        bot.quit()
        console.log(mccolors.translateColors(`\n    §f[§c#§f] ${exit}\n`))
        rl.close()
        return;
      }
  
      else {
        bot.chat(command)
      }
  
      input(); 
    });
  }
}

createBot()
