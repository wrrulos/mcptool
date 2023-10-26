const fs = require('fs');
const mccolors = require('minecraft-colors')


function getTextFromJSON(json) {
  let obj = null;

  try {
    obj = JSON.parse(json);
  } catch (_) {
    return null;
  }

  let text = '';

  function processExtra(extra) {
      if (Array.isArray(extra)) {
          extra.forEach((item) => {

          if (item.text) {
              text += item.text;
          }

          if (item.translate) {
              text += item.translate;
          }

          if (item.extra) {
              processExtra(item.extra);
          }

          if (item.hasOwnProperty('with')) {
              text += getTextFromJSON(JSON.stringify(item.with));
          }
      });

      } else if (extra.text) {
          text = extra.text;
      } else if (extra.translate) {
          text = extra.translate;
      }
    }

    if (Array.isArray(obj.extra)) {
        processExtra(obj.extra);
    } else if (obj.text) {
        text = obj.text;
    } else if (obj.translate) {
        text = obj.translate;
    }

    return text.trim();
}

function coloredText(text) {
    console.log(mccolors.translateColors(text));
}

function checkLogsDirectory(directory) {
    const logsDir = directory;
  
    if (!fs.existsSync(logsDir)) {
        fs.mkdirSync(logsDir, { recursive: true });
    }
}

function generateFilename(name) {
    const date = new Date();
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear().toString();
    const hour = date.getHours().toString().padStart(2, '0');
    const minute = date.getMinutes().toString().padStart(2, '0');
    const second = date.getSeconds().toString().padStart(2, '0');
    const filename = `${name}_${day}-${month}-${year}_${hour}.${minute}.${second}.txt`;

    if (fs.existsSync(filename)) {
        return generateFilename();
    }

    return filename;
}

function readFile(commandFile) {
    try {
        const fileContent = fs.readFileSync(commandFile, 'utf8');
        return fileContent.split(/\r?\n/).map(word => word.trim());
    } catch (err) {
        return null;
    }
}

function getMessages(file) {
    try {        
        const messagesFile = fs.readFileSync(file, 'utf8');
        const messagesList = messagesFile.split('\r\n');

        if (messagesList.length >= 1) {
            return messagesList;
        }
                
        return null;
    } catch(_) {console.log(_);}
    return null;
}


function getProxy(file) {
    try {        
        const proxyFile = fs.readFileSync(file, 'utf8');
        const proxyList = proxyFile.split('\r\n');

        if (proxyList.length >= 1) {
            let randomProxy = proxyList[Math.floor(Math.random() * proxyList.length)].replace(/\s+/g, '');
            randomProxy = randomProxy.split(':');
            return [randomProxy[0], parseInt(randomProxy[1])];
        }
                
        return null;
    } catch(_) {}
    return null;
}


function getUsername(file) {
    try {        
        const usernameFile = fs.readFileSync(file, 'utf8');
        const usernameList = usernameFile.split('\r\n');

        if (usernameList.length >= 1) {
            return usernameList[Math.floor(Math.random() * usernameList.length)].replace(/\s+/g, '')
        }
                
        return null;
    } catch(_) {}
    return null;
}


function getListOfPasswords(file){
    try {
        const passwordFile = fs.readFileSync(file, 'utf8');
        const passwordList = passwordFile.split('\r\n');

        if (passwordList.length >= 1) {
            return passwordList;
        }

        return null;
    } catch (_) {
        return null;
    }
}


async function tab(bot, text, returnResults=false) {
    try {
        let matches = await bot.tabComplete(text);

        if (typeof (matches) === 'object') {
            matches = matches.map(obj => obj.match);
        }
        
        if (returnResults === true) {
            return matches;
        }

        matches = matches.join(', ');
        coloredText(matches);
        
    } catch (err) {}
}

module.exports = {
    getTextFromJSON: getTextFromJSON,
    getMessages: getMessages,
    coloredText: coloredText,
    checkLogsDirectory: checkLogsDirectory,
    generateFilename: generateFilename,
    readFile: readFile,
    getListOfPasswords: getListOfPasswords,
    getUsername: getUsername,
    getProxy: getProxy,
    tab: tab
}