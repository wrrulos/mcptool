import fs from "fs";
import os from "os";
import path from "path";
import mccolors from "minecraft-colors";


class Utilities {
  static read_file(file) {
    /**
     * Method to read a file and return its content
     *
     * @param {string} file Path of the file to read
     * @returns {string[]} Content of the file
     * @throws {Error} If the file is not found
     */

    if (!fs.existsSync(file)) {
      console.log(`§cFile not found: §c§l${file}`);
      process.exit(1);
    }

    const data = fs.readFileSync(file, "utf8");
    const content = data.split("\n");
    return content;
  }

  static get_mcptool_path() {
    /**
     * Method to get the path of the MCPTool folder
     * and create it if it doesn't exist
     *
     * @returns {string} Path of the MCPTool folder
     */

    let mcptool_path;

    if (process.platform === "win32") {
      mcptool_path = path.join(os.homedir(), "AppData", "Roaming", "MCPTool");
    } else {
      mcptool_path = path.join(os.homedir(), ".config", "mcptool");
    }

    try {
      fs.accessSync(mcptool_path);
    } catch (error) {
      fs.mkdirSync(mcptool_path, { recursive: true });
    }

    return mcptool_path;
  }

  static getTextFromJSON(json) {
    let obj = null;

    try {
      obj = JSON.parse(json);
    } catch (_) {
      return null;
    }

    let text = "";

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

          if (item.hasOwnProperty("with")) {
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

  static error_handler(error, spaces = "", color = false) {
    /**
     * Method to handle errors in Minecraft connections
     *
     * @param {Error} error Error object
     */

    let protocol = null;

    if (error.message.includes("is not supported")) {
      const version = error.message.match(/\d+\.\d+\.\d+/)[0];

      if (color) {
        console.log(
          mccolors.translateColors(
            `\n${spaces}§f[§c#§f] §cIncompatible Minecraft version: Version §c§l${version} §cis not currently supported.`
          )
        );
        return;
      }

      console.log(
        `§cIncompatible Minecraft version: Version §c§l${version} §cis not currently supported.`
      );
    } else if (error.message.includes("unsupported protocol version:")) {
      try {
        protocol = error.message.match(/\d+/)["input"].split(": ")[1];
      } catch {
        protocol = error.message.match(/\d+/);
      }

      if (protocol != null) {
        if (color) {
          console.log(
            mccolors.translateColors(
              `\n${spaces}§f[§c#§f] §cIncompatible Minecraft version: Protocol §c§l${protocol} §cis not supported`
            )
          );

          return;
        }

        console.log(
          `§cIncompatible Minecraft version: Protocol §c§l${protocol} §cis not supported`
        );
      } else {
        if (color) {
          console.log(
            mccolors.translateColors(
              `\n${spaces}§f[§c#§f] §cIncompatible Minecraft version: Protocol is not supported`
            )
          );

          return;
        }

        console.log(
          `§cIncompatible Minecraft version: Protocol is not supported`
        );
      }
    } else {
      console.log(`§4Error`);
    }
  }

  static async get_tab(bot, text, spaces, returnResults = false) {
    /**
     * Method to get tab completion results
     *
     * @param {bot} bot Bot object
     * @param {string} text Text to tab complete
     * @param {string} spaces Spaces to add to the start of the message
     * @param {boolean} returnResults If the results should be returned
     * @returns {string[]} Tab completion results
     * @throws {Error} If the tab completion fails
     */

    try {
      // Get the tab completion results
      let matches = await bot.tabComplete(text);

      // If the results should be returned, return them
      if (returnResults === true) {
        return matches;
      }

      // If the results should not be returned, print them
      matches = matches.join(", ");
      console.log(mccolors.translateColors(`\n${spaces}§f[§c#§f] §a${matches}`));
    } catch (err) {
      if (returnResults) {
        return [];
      }
    }
  }
}

export default Utilities;
