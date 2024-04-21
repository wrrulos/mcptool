import mc from "minecraft-protocol";
import mc2 from "mineflayer";

class Bot {
  constructor(host, port, username, version) {
    this.bot = mc.createClient({
      host: host,
      port: port,
      username: username,
      version: version,
    });
  }

  on(event, callback) {
    this.bot.on(event, callback);
  }

  end() {
    this.bot.end();
  }
}

class BotMineflayer {
  constructor(host, port, username, version) {
    this.bot = mc2.createBot({
      host: host,
      port: port,
      username: username,
      version: version,
      fakeHost: host,
    });
  }

  on(event, callback) {
    this.bot.on(event, callback);
  }

  end() {
    this.bot.end();
  }

  chat(message) {
    this.bot.chat(message);
  }

  quit() {
    this.bot.quit();
  }
}

export { BotMineflayer, Bot };
