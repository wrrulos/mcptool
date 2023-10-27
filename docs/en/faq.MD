# FAQ

This document contains a list of answers to frequently asked questions.

### MCPTool closes when starting the tool.
This is because you need to install the Python modules. You can do this through the **setup.py** script.

### Proxy servers are not working.
If the proxy servers, whether Bungee, Velocity or FakeProxy, do not work, it is because a version of Java 17 or higher is required.

### The Scan or Masscan method does not work on Linux or termux.
This is because masscan and the default nmap command require administrator (sudo) permissions.

If you want to use the nmap command without requiring administrator permissions, you can remove the -sS argument from the config/config.json configuration file. When you do this, nmap will use a different scan, such as the TCP Connect (-sT) scan, which does not require root privileges.

### The Shodan command does not work correctly despite entering a valid API key.

The issue you are experiencing is because your Shodan API key does not have access to search capabilities. You may need an API key with broader privileges to be able to search.