# Script created for MCPTool
# @wrrulos

def skip_0on():
    while True:
        skip = input("\n     Do you want to skip the servers that have no players connected? yes/no -> ")

        if skip.lower() == "y" or skip.lower() == "yes":
            return True

        elif skip.lower() == "n" or skip.lower() == "no":
            return False

        else:
            continue


def specific_version():
    while True:
        version = input("\n     Do you want to put a specific version for the bot? (Example: 1.8) y/n: ")

        if version.lower() == "y" or version.lower() == "yes":
            version = input("\n     Write the version: ")
            return version

        elif version.lower() == "n" or version.lower() == "no":
            version = None
            return version

        else:
            continue


def specific_name():
    while True:
        name = input("\n     Do you want to put a specific name for the bot? (Example: Rulo_MCPT) y/n: ")

        if name.lower() == "y" or name.lower() == "yes":
            name = input("\n     Write the name: ")
            return name

        elif name.lower() == "n" or name.lower() == "no":
            name = None
            return name

        else:
            continue
