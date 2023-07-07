from utils.minecraft.server_data import GetDataFromMinecraftServer


def active_server(ip):
    server_data = GetDataFromMinecraftServer(server=ip)
    data = server_data.get_information()

    if data is not None:
        return True

    return False
