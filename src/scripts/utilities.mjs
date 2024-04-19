class Utilities {
    static error_handler(error) {      
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