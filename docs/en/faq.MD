# FAQ

This document contains a list of answers to frequently asked questions.

### MCPTool shuts down when starting the tool.
This happens because you need to install the Python modules. You can do this through the **setup.py** script.

### Proxy servers are not working.
If proxy servers, whether Bungee, Velocity, or FakeProxy, are not functioning, it's likely due to the requirement of Java 17 or higher.

### How do I prevent MCPTool from checking for updates?
Previously, you could change a value in the configuration file, but now, to skip MCPTool updates, you should press Ctrl+C when the tool notifies that it's checking for a new version. You can also skip proxy updates by changing the value '"updateProxy": true' to false in the configuration file. This isn't recommended as it might lead to incompatibility if a new Minecraft version is released.

### The Scan or Masscan method doesn't work in Linux or Termux.
This is because Masscan and the default Nmap command require administrator permissions (sudo).

If you want to use the Nmap command without needing administrator permissions, you can remove the -sS argument from the config/config.json file. By doing this, Nmap will use a different scan, like TCP Connect (-sT), which doesn't require root privileges.

### Error (Missing NodeJS Modules!)
This is because the NodeJS modules need to be installed in order to run the scripts that control the bots in MCPTool.

### The Shodan command isn't functioning correctly despite entering a valid API key.

The issue you're facing is likely due to your Shodan API key lacking access to search functionalities. You might need an API key with broader privileges to conduct searches.
