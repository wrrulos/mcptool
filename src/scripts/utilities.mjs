import fs from 'fs';
import os from 'os';
import path from 'path';


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

        const data = fs.readFileSync(file, 'utf8');
        const content = data.split('\n');
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

        if (process.platform === 'win32') {
            mcptool_path = path.join(os.homedir(), 'AppData', 'Roaming', 'MCPTool');
        } else {
            mcptool_path = path.join(os.homedir(), '.config', 'mcptool');
        }
    
        try {
            fs.accessSync(mcptool_path);
        } catch (error) {
            fs.mkdirSync(mcptool_path, { recursive: true });
        }
    
        return mcptool_path;
    } 

    static error_handler(error) {
        /**
         * Method to handle errors in Minecraft connections
         * 
         * @param {Error} error Error object
         */

        let protocol = null;
          
        if (error.message.includes('is not supported')) {
            const version = error.message.match(/\d+\.\d+\.\d+/)[0];
            console.log(`§cIncompatible Minecraft version: Version §c§l${version} §cis not currently supported.`)
        }

        else if (error.message.includes('unsupported protocol version:')) {
            try {
                protocol = error.message.match(/\d+/)['input'].split(': ')[1]
                
            } catch {
                protocol = error.message.match(/\d+/);
            }
            
            if (protocol != null) {
                console.log(`§cIncompatible Minecraft version: Protocol §c§l${protocol} §cis not supported`)
            } else {
                console.log(`§cIncompatible Minecraft version: Protocol is not supported`)
            }
        }

        else {
            console.log(`§4Error`)
        }
    }
}

export default Utilities;