import socket

from mcstatus import JavaServer, BedrockServer
from typing import Union

from app.minecraft.server.server_data import JavaServerData


class MCServerData:
    def __init__(self, server: str) -> None:
        self.server = server
        self.platform = 'Java'
        #self.method = 'localhost'

    def get(self) -> dict:
        """
        Method to get data from the server locally 
        using the mcstatus library.
        """

        # Try to get the data from the Java server class
        data = self._get_server_data(JavaServer(self.server))

        # If the server is not a Java server, try to get the data
        # from the Bedrock server class
        if data is None:
            print(1)
            data = self._get_server_data(BedrockServer(self.server))

        # If the data is still None, return None
        if data is None:
            return None
        
        return data
    
    def _get_server_data(self, function: Union[JavaServer, BedrockServer]) -> dict:
        """
        Method to get the server data
        """

        try:
            data = function.status()

            if self.platform == 'Java':
                return JavaServerData(
                    ip_address=self.server,
                    port=25565
                )
            
            return data

        except (ConnectionRefusedError, TimeoutError, socket.gaierror):
            return None
            
        

        
    
