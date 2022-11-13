// Script created for MCPTool @wrrulos
// node Connect.js <host> <port> <name> <version> [<proxyHost>] [<proxyPort>]

const mineflayer = require('mineflayer')
const socks = require('socks').SocksClient
const ProxyAgent = require('proxy-agent')
const readline = require('readline');
const fs = require('fs');

if (process.argv.length < 6 || process.argv.length > 9) {
  console.log('Usage : node Connect.js <host> <port> <name> <version> [<proxyHost>] [<proxyPort>]')
  process.exit(1)
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});


const proxyHost = process.argv[7]
const proxyPort = process.argv[8]

if (proxyHost == null) {
  var client = mineflayer.createBot({
  host: process.argv[2],
  port: parseInt(process.argv[3]),
  username: process.argv[4],
  version: process.argv[5],
});
} else {
  var client = mineflayer.createBot({
    connect: client => {
      socks.createConnection({
        proxy: {
          host: proxyHost,
          port: parseInt(proxyPort),
          type: 5
        },
        command: 'connect',
        destination: {
          host: process.argv[2],
          port: parseInt(process.argv[3])
        }
      }, (err, info) => {
        if (err) {
          console.log(err)
          return
        }
  
        client.setSocket(info.socket)
        client.emit('connect')
      })
    },
    agent: new ProxyAgent({ protocol: 'socks5:', host: proxyHost, port: proxyPort }),
    username: process.argv[4],
    version: process.argv[5],
  })
}

client.on("message",(toAnsi)=>{
  var msg = toAnsi.toAnsi()
  console.log('   ', msg)

  rl.question('', function (command) {

    if (command == '--help') {
      console.log('help-message')
    }

    else if (command == '--exit') {
      process.kill(process.pid)
    }

    else {
      client.chat(command)
    }
      
  });
});

client.on('login', () => { console.log('    [#] The bot connected to the server successfully. \n    Use the --help command to see the available commands.\n\n') })  // This message will be displayed if the bot enters the server
client.on('kicked', (reason) => {  fs.writeFileSync(process.argv[6], reason), process.kill(process.pid) })  //
client.on('error', function (error) { console.log('\n  [#] Client Error', error), process.kill(process.pid) })
