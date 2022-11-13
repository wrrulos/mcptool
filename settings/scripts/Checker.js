// Script created for MCPTool @wrrulos
// node Checker.js <host> <port> <name> <version> [<proxyHost>] [<proxyPort>]

const mineflayer = require('mineflayer')
const socks = require('socks').SocksClient
const ProxyAgent = require('proxy-agent')

if (process.argv.length < 6 || process.argv.length > 8) {
  console.log('Usage : node Checker.js <host> <port> <name> <version> [<proxyHost>] [<proxyPort>]')
  process.exit(1)
}

const proxyHost = process.argv[6]
const proxyPort = process.argv[7]

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

client.on('login', () => { console.log('_-Login-_'), process.kill(process.pid)})  // This message will be displayed if the bot enters the server
client.on('disconnect', function (packet) { console.log(packet.reason), process.kill(process.pid) })  // Disconnect
client.on('kicked', (reason) => {  console.log(reason), process.kill(process.pid) })  //
client.on('end', function (reason) { console.log('_-Connection lost-_', reason), process.kill(process.pid) })
client.on('error', function (error) { console.log('_-Client Error-_', error), process.kill(process.pid) })

setTimeout(() => { console.log('_-Timeout-_'), process.kill(process.pid) }, 10000);  // Timeout
